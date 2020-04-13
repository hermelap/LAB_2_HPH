# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - para procesamiento de datos
# -- mantiene: Hermela Peña
# -- repositorio: https://github.com/hermelap/LAB_2_HPH
# -- ------------------------------------------------------------------------------------ -- #
# -- En esta parte se importan las librerias necesarias
import pandas as pd  # esta libreria nos ayuda a crear los Dataframes
import numpy as np  # esta libreria nos permite utilizar matrices y vectores
import statistics  # Libreria de estadisticas básicas
from datetime import timedelta  # diferencia entre datos tipo tiempo
from oandapyV20 import API  # conexion con broker OANDA
import oandapyV20.endpoints.instruments as instruments  # informacion de precios historicos
from datos import token
import visualizaciones as vs


# -- ------------------------------------------------FUNCION: leer archivo de entrada#

def f_leer_archivo(param_archivo):
    """
    Parameters
    ------------
    param_archivo : str : nombre de archivo a leer
    Returns
    ------
    df_data : pd.Dataframe : con inforamcion contenida en archivo leido

    Debugging
    -----
    param_archivo = 'archivo_tradeview_1.xlsx'

    """
    df_data = pd.read_excel('Archivos/' + param_archivo, sheet_name='Hoja1')
    df_data = df_data[df_data.type != 'balance']

    df_data.columns = [list(df_data.columns)[i].lower()
                       for i in range(0, len(df_data.columns))]

    # Asegurar que ciertas columnas son del tipo numerico
    # Cambiar tipo de dato en columnas a numerico

    numcols = ['s/l', 't/p', 'commission', 'openprice', 'closeprice', 'profit', 'size', 'swap', 'taxes', 'order']
    df_data[numcols] = df_data[numcols].apply(pd.to_numeric)

    df_data = df_data.reset_index()

    return df_data


def f_pip_size(param_ins):
    """
    Parameters
    ------------

    param_ins : str : con info de historicos
    Returns
    ------
    df_data : pd.Dataframe : con inforamcion contenida en archivo leido

    Debugging
    -----
    param_data = df_data

    """
    # Eliminar -2 de los tickers
    inst = param_ins.replace('-2', '')

    # lista de pips por ticker
    pips_inst = {'usdmxn': 10000, 'eurusd': 10000, 'usdjpy': 100, 'eurjpy': 100, 'audusd': 10000, 'gbpusd': 10000,
                 'usdchf': 10000, 'audjpy': 100, 'euraud': 10000, 'eurgbp': 10000, 'gbpjpy': 100, 'usdcad': 10000,
                 'audcad': 10000, 'eurcad': 10000, 'gbpaud': 10000, 'usdhkd': 10000, 'gbphkd': 10000, 'cadhkd': 10000,
                 'xauusd': 10, 'btcusd': 1}

    return pips_inst[inst] #cantidad de pips


def f_columnas_tiempos(param_data):
    """

    Parameters
    ----------
    param_data: dataframe de informacion de la cuenta

    Returns: Mismo dataframe convirtiendo fechas a tiempo de pandas
    -------
    Debugging
    -------
    param_data = df_data

    """
    # convierte tiempos a timestamp
    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])

    param_data['tiempo'] = [(param_data.loc[i, 'closetime'] - param_data.loc[i, 'opentime']).delta / 1e9
                            for i in range(0, len(param_data['closetime']))]

    return param_data


def f_columnas_pips(param_data):
    """

    Parameters
    ----------
    param_data: DataFrame

    Returns: Mismo dataframe com calculos de capital y pips
    -------

    Debugging
    -----
    param_data = df_data

    """

    # Calcular pips entre apertura y cierre de operaciones
    for i in range(0, len(param_data['openprice'])):
        if param_data.loc[i, "type"] == "sell":
            param_data.loc[i, "pips"] = (param_data.loc[i, "openprice"] - param_data.loc[i, "closeprice"]) * \
                                        f_pip_size(param_data.loc[i, "symbol"])
        else:
            param_data.loc[i, "pips"] = (param_data.loc[i, "closeprice"] - param_data.loc[i, "openprice"]) * \
                                        f_pip_size(param_data.loc[i, "symbol"])

    # Se calculan los pips acumulados (perdidas o ganancias)
    param_data['pips_acm'] = param_data['pips'].cumsum()

    # Ganacia o perdida acumulada
    param_data['profit_acm'] = param_data['profit'].cumsum()

    # Se calcula el capital acumulado
    inversion_inicial = 5000
    for i in range(0, len(param_data.index)):
        param_data.loc[i, 'capital_acum'] = param_data['profit_acm'][i] + inversion_inicial

    return param_data


def f_estadisticas_ba(param_data):
    """

    Parameters
    ----------
    param_data

    Returns
    -------
    Diccionario con estadisticas y ranking

    Debugging
    ------
    param_data = df_data

    """
    # lista de estadisticas
    medidas = np.array(['Ops totales', 'Ganadoras', 'Ganadoras_c', 'Ganadoras_v', 'Perdedoras', 'Perdedoras_c',
                        'Perdedoras_v', 'Media (Profit)', 'Media (Pips)', 'r_efectividad', 'r_proporcion',
                        'r_efectividad_c', 'r_efectividad_v'])

    # lista de descripciones de dataframe de las columnas de arriba

    descripciones = np.array(['Operaciones totales', 'Operaciones ganadoras', 'Operaciones ganadoras de compra',
                              'Operaciones ganadoras de venta', 'Operaciones perdedoras',
                              'Operaciones perdedoras de compra', 'Operaciones perdedoras de venta',
                              'Mediana de profit de operaciones', 'Mediana de pips de operaciones',
                              'Operaciones Totales Vs Ganadoras Totales', 'Ganadoras Totales Vs Perdedoras Totales',
                              'Totales Vs Ganadoras Compras', 'Totales Vs Ganadoras Ventas'])

    # Crear el dataframe
    df_1_tabla = pd.DataFrame(columns=['medidas', 'valor', 'descripcion'])

    # Llenar información
    for i in range(0, len(medidas)):
        df_1_tabla = df_1_tabla.append({'medidas': medidas[i], 'valor': 0, 'descripcion': descripciones},
                                       ignore_index=True)

    # Operaciones totales
    df_1_tabla.loc[0, 'valor'] = len(param_data['profit'])

    # Calcular ganadoras y perdedoras
    ganadoras = 0
    ganadoras_c = 0
    ganadoras_v = 0
    perdedoras = 0
    perdedoras_c = 0
    perdedoras_v = 0
    for i in range(0, len(param_data.index)):
        if param_data.loc[i, 'profit'] >= 0:
            ganadoras = ganadoras + 1
        if param_data.loc[i, 'profit'] >= 0 and param_data.loc[i, 'type'] == 'buy':
            ganadoras_c = ganadoras_c + 1
        if param_data.loc[i, 'profit'] >= 0 and param_data.loc[i, 'type'] == 'sell':
            ganadoras_v = ganadoras_v + 1
        if param_data.loc[i, 'profit'] < 0:
            perdedoras = perdedoras + 1
        if param_data.loc[i, 'profit'] < 0 and param_data.loc[i, 'type'] == 'buy':
            perdedoras_c = perdedoras_c + 1
        if param_data.loc[i, 'profit'] < 0 and param_data.loc[i, 'type'] == 'sell':
            perdedoras_v = perdedoras_v + 1

    # asignar los valores al dataframe
    df_1_tabla.loc[1, 'valor'] = ganadoras
    df_1_tabla.loc[2, 'valor'] = ganadoras_c
    df_1_tabla.loc[3, 'valor'] = ganadoras_v
    df_1_tabla.loc[4, 'valor'] = perdedoras
    df_1_tabla.loc[5, 'valor'] = perdedoras_c
    df_1_tabla.loc[6, 'valor'] = perdedoras_v

    # Medias
    df_1_tabla.loc[7, 'valor'] = np.round(statistics.median(param_data["profit"]), 3)
    df_1_tabla.loc[8, 'valor'] = np.round(statistics.median(param_data["pips"]), 0)

    # Efectividad
    df_1_tabla.loc[9, 'valor'] = np.round(df_1_tabla["valor"][0] / df_1_tabla["valor"][1], 2)
    df_1_tabla.loc[11, 'valor'] = np.round(df_1_tabla["valor"][0] / df_1_tabla["valor"][2], 2)
    df_1_tabla.loc[12, 'valor'] = np.round(df_1_tabla["valor"][0] / df_1_tabla["valor"][3], 2)

    # Proporcion
    df_1_tabla.loc[10, 'valor'] = np.round(df_1_tabla["valor"][1] / df_1_tabla["valor"][4], 2)

    # Parte 2 -----------

    # Conseguir tickers utilizados
    simbolos = np.unique(param_data["symbol"])

    # Crear dataframe
    df_2_ranking = pd.DataFrame(simbolos, columns=["symbol"])
    df_2_ranking["rank"] = 0
    i = 0
    for sim in simbolos:
        totales = 0
        ganadas = 0
        for x in range(0, len(param_data.index)):
            if param_data["profit"][x] >= 0 and param_data["symbol"][x] == sim:
                ganadas = ganadas + 1
            if param_data["symbol"][x] == sim:
                totales = totales + 1
        df_2_ranking["rank"][i] = str(np.round(ganadas / totales * 100, 2)) + "%"
        i = i + 1

    # Crear el diccionario final
    diccionario = {
        "df_1_tabla": df_1_tabla,
        "df_2_ranking": df_2_ranking
    }

    return diccionario # Diccionario con las estadisticas basicas y el ranking de los tickers


#  En esta parte se Calculan Medidas de Atribución al Desempeño

def f_profit_diario(param_data):
    """

    Parameters
    ----------
    param_data: es un dataframe con los datos de la cuenta

    Returns
    -------
    regresa un dataframe con los movimientos diarios

    debugging
    -------
    param_data = df_data
    """

    diario = param_data[['closetime', 'profit']]
    diario.index = diario['closetime']
    diario = diario.resample('d').sum()  # se suman los profits intradia
    diario = diario.reset_index()
    diario['profit_acm_d'] = diario['profit'].cumsum() + 5000  # suma de capital acumulado
    diario.rename(columns={'closetime': 'timestamp', 'profit': 'profit_d', 'profit_acm_d': 'profit_acm_d'},
                  inplace=True)
    return diario


def f_estadisticas_mad(param_data):
    """

    Parameters
    ----------
    param_data

    Returns
    -------

    Debugging
    ------
    param_data = df_data
    """

    # Lista
    medidasAD = np.array(['Sharpe', 'sortino_c', 'sortino_v', 'drawndown_capi', 'drawup_capi', 'information_r'])

    # lista de las descripciones
    descripcionesMAD = np.array(['Sharpe Ratio', 'Sortino Ratio para Posiciones  de Compra',
                                 'Sortino Ratio para Posiciones de Venta', 'DrawDown de Capital', 'DrawUp de Capital',
                                 'Information Ratio'])

    # Dataframe de estadisticas mad
    valores_mad = pd.DataFrame(columns=['metrica', 'valor', 'descripcion'])

    # meter medidas y descripciones
    for i in range(0, len(medidasAD)):
        valores_mad = valores_mad.append({'metrica': medidasAD[i], 'valor': 0, 'descripcion': descripcionesMAD[i]},
                                         ignore_index=True)

    # MAD

    # sharpe ratio
    valores_diarios = f_profit_diario(param_data=param_data)
    rendimientos = np.log(valores_diarios['profit_acm_d'] / valores_diarios['profit_acm_d'].shift())
    volatilidad = rendimientos.std()
    rendimientio_portafolio = rendimientos.sum()
    valores_mad.loc[0, 'valor'] = (rendimientio_portafolio - 0.08 / 300) / volatilidad

    # Sortino_c
    valores_diarios_compra = f_profit_diario(param_data[param_data['type'] == 'buy'])
    rendimientos_compra = np.log(
        valores_diarios_compra['profit_acm_d'] / valores_diarios_compra['profit_acm_d'].shift())
    rendimientio_portafolio_compra = rendimientos_compra.sum()
    para_std = []
    for i in range(0, len(rendimientos_compra)):
        if rendimientos_compra[i] < 0.3 / 300:
            para_std.append(rendimientos_compra[i])
    volatilidad_compra = np.std(para_std)
    valores_mad.loc[1, 'valor'] = (rendimientio_portafolio_compra - 0.3 / 300) / volatilidad_compra

    # Sortino_v
    valores_diarios_venta = f_profit_diario(param_data[param_data['type'] == 'sell'])
    rendimientos_venta = np.log(valores_diarios_venta['profit_acm_d'] / valores_diarios_venta['profit_acm_d'].shift())
    rendimientio_portafolio_venta = rendimientos_venta.sum()
    para_std = []
    for i in range(0, len(rendimientos_venta)):
        if rendimientos_venta[i] < 0.3 / 300:
            para_std.append(rendimientos_venta[i])
    volatilidad_venta = np.std(para_std)
    valores_mad.loc[2, 'valor'] = (rendimientio_portafolio_venta - 0.3 / 300) / volatilidad_venta

    # DrawDown
    draw_down_maximo = 0
    maximo = valores_diarios.loc[0, 'profit_acm_d']
    inicio = valores_diarios.loc[0, 'timestamp']
    fin = valores_diarios.loc[0, 'timestamp']
    for i in range(0, len(valores_diarios['timestamp'])):
        if valores_diarios.loc[i, 'profit_acm_d'] > maximo and fin <= inicio:
            inicio = valores_diarios.loc[i, 'timestamp']
            maximo = valores_diarios.loc[i, 'profit_acm_d']
        draw_down = maximo - valores_diarios.loc[i, 'profit_acm_d']
        if draw_down > draw_down_maximo:
            fin = valores_diarios.loc[i, 'timestamp']
            draw_down_maximo = draw_down
    drawdown_capi = str(inicio) + ' ' + str(fin) + ' ' + str(draw_down_maximo)

    valores_mad.loc[3, 'valor'] = drawdown_capi

    # DrawUp
    draw_up_maximo = 0
    minimo = valores_diarios.loc[0, 'profit_acm_d']
    inicio = valores_diarios.loc[0, 'timestamp']
    fin = valores_diarios.loc[0, 'profit_acm_d']
    for i in range(0, len(valores_diarios['timestamp'])):
        if valores_diarios.loc[i, 'profit_acm_d'] < minimo:
            inicio = valores_diarios.loc[i, 'timestamp']
            minimo = valores_diarios.loc[i, 'profit_acm_d']
        draw_up = valores_diarios.loc[i, 'profit_acm_d'] - minimo
        if draw_up > draw_up_maximo:
            fin = valores_diarios.loc[i, 'timestamp']
            draw_up_maximo = draw_up
    drawup_capi = str(inicio) + ' ' + str(fin) + ' ' + str(draw_up_maximo)

    valores_mad.loc[4, 'valor'] = drawup_capi

    # Informacion_r
    inicio = param_data.loc[0, 'opentime']
    fin = param_data['closetime'].iloc[-1]
    datos_benchmark = f_precios_masivos(p0_fini=inicio, p1_ffin=fin, p2_gran="D", p3_inst="SPX500_USD", p4_oatk=token,
                                        p5_ginc=4900)
    datos_benchmark['rendimientos'] = np.log(datos_benchmark['Close'] / datos_benchmark['Close'].shift())

    error_std = (rendimientos - datos_benchmark['rendimientos']).std()
    rendimiento_benchmark = np.sum(datos_benchmark['rendimientos'])
    informacion_r = (rendimientio_portafolio - rendimiento_benchmark) / error_std
    valores_mad.loc[5, 'valor'] = informacion_r

    return valores_mad #regresa las estadisticas de MAD


def f_precios_masivos(p0_fini, p1_ffin, p2_gran, p3_inst, p4_oatk, p5_ginc):
    """
    Funcion para descargar precios historicos masivos de OANDA

    Parameters
    ----------
    p0_fini
    p1_ffin
    p2_gran
    p3_inst
    p4_oatk
    p5_ginc
    Returns
    -------
    dc_precios
    Debugging
    ---------
    """

    def f_datetime_range_fx(p0_start, p1_end, p2_inc, p3_delta):
        """
        Parameters
        ----------
        p0_start
        p1_end
        p2_inc
        p3_delta
        Returns
        -------
        ls_resultado
        Debugging
        ---------
        """

        ls_result = []
        nxt = p0_start

        while nxt <= p1_end:
            ls_result.append(nxt)
            if p3_delta == 'minutes':
                nxt += timedelta(minutes=p2_inc)
            elif p3_delta == 'hours':
                nxt += timedelta(hours=p2_inc)
            elif p3_delta == 'days':
                nxt += timedelta(days=p2_inc)

        return ls_result

    # inicializar api de OANDA

    api = API(access_token=p4_oatk)

    gn = {'S30': 30, 'S10': 10, 'S5': 5, 'M1': 60, 'M5': 60 * 5, 'M15': 60 * 15,
          'M30': 60 * 30, 'H1': 60 * 60, 'H4': 60 * 60 * 4, 'H8': 60 * 60 * 8,
          'D': 60 * 60 * 24, 'W': 60 * 60 * 24 * 7, 'M': 60 * 60 * 24 * 7 * 4}

    # -- para el caso donde con 1 peticion se cubran las 2 fechas
    if int((p1_ffin - p0_fini).total_seconds() / gn[p2_gran]) < 4999:

        # Fecha inicial y fecha final
        f1 = p0_fini.strftime('%Y-%m-%dT%H:%M:%S')
        f2 = p1_ffin.strftime('%Y-%m-%dT%H:%M:%S')

        # Parametros pra la peticion de precios
        params = {"granularity": p2_gran, "price": "M", "dailyAlignment": 16, "from": f1,
                  "to": f2}

        # Ejecutar la peticion de precios
        a1_req1 = instruments.InstrumentsCandles(instrument=p3_inst, params=params)
        a1_hist = api.request(a1_req1)

        # Para debuging
        # print(f1 + ' y ' + f2)
        lista = list()

        # Acomodar las llaves
        for i in range(len(a1_hist['candles']) - 1):
            lista.append({'TimeStamp': a1_hist['candles'][i]['time'],
                          'Open': a1_hist['candles'][i]['mid']['o'],
                          'High': a1_hist['candles'][i]['mid']['h'],
                          'Low': a1_hist['candles'][i]['mid']['l'],
                          'Close': a1_hist['candles'][i]['mid']['c']})

        # Acomodar en un data frame
        r_df_final = pd.DataFrame(lista)
        r_df_final = r_df_final[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
        r_df_final['TimeStamp'] = pd.to_datetime(r_df_final['TimeStamp'])
        r_df_final['Open'] = pd.to_numeric(r_df_final['Open'], errors='coerce')
        r_df_final['High'] = pd.to_numeric(r_df_final['High'], errors='coerce')
        r_df_final['Low'] = pd.to_numeric(r_df_final['Low'], errors='coerce')
        r_df_final['Close'] = pd.to_numeric(r_df_final['Close'], errors='coerce')

        return r_df_final

    # -- para el caso donde se construyen fechas secuenciales
    else:

        # hacer series de fechas e iteraciones para pedir todos los precios
        fechas = f_datetime_range_fx(p0_start=p0_fini, p1_end=p1_ffin, p2_inc=p5_ginc,
                                     p3_delta='minutes')

        # Lista para ir guardando los data frames
        lista_df = list()

        for n_fecha in range(0, len(fechas) - 1):

            # Fecha inicial y fecha final
            f1 = fechas[n_fecha].strftime('%Y-%m-%dT%H:%M:%S')
            f2 = fechas[n_fecha + 1].strftime('%Y-%m-%dT%H:%M:%S')

            # Parametros pra la peticion de precios
            params = {"granularity": p2_gran, "price": "M", "dailyAlignment": 16, "from": f1,
                      "to": f2}

            # Ejecutar la peticion de precios
            a1_req1 = instruments.InstrumentsCandles(instrument=p3_inst, params=params)
            a1_hist = api.request(a1_req1)

            # Para debuging
            print(f1 + ' y ' + f2)
            lista = list()

            # Acomodar las llaves
            for i in range(len(a1_hist['candles']) - 1):
                lista.append({'TimeStamp': a1_hist['candles'][i]['time'],
                              'Open': a1_hist['candles'][i]['mid']['o'],
                              'High': a1_hist['candles'][i]['mid']['h'],
                              'Low': a1_hist['candles'][i]['mid']['l'],
                              'Close': a1_hist['candles'][i]['mid']['c']})

            # Acomodar en un data frame
            pd_hist = pd.DataFrame(lista)
            pd_hist = pd_hist[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
            pd_hist['TimeStamp'] = pd.to_datetime(pd_hist['TimeStamp'])

            # Ir guardando resultados en una lista
            lista_df.append(pd_hist)

        # Concatenar todas las listas
        r_df_final = pd.concat([lista_df[i] for i in range(0, len(lista_df))])

        # resetear index en dataframe resultante porque guarda los indices del dataframe pasado
        r_df_final = r_df_final.reset_index(drop=True)
        r_df_final['Open'] = pd.to_numeric(r_df_final['Open'], errors='coerce')
        r_df_final['High'] = pd.to_numeric(r_df_final['High'], errors='coerce')
        r_df_final['Low'] = pd.to_numeric(r_df_final['Low'], errors='coerce')
        r_df_final['Close'] = pd.to_numeric(r_df_final['Close'], errors='coerce')

        return r_df_final


# Parte 4, En esta parte se identifica el sesgo cognitivo del trader
def f_be_de(param_data):
    """

    Parameters
    ----------
    param_data

    Returns
    -------
    Diccionario con el sesgo congnitivo

    Debbuging
    -------
    param_data = df_data

    """
    # Sacar si la operacion fue ganadora o perdedora
    param_data['status'] = 'ganadora'
    for i in range(0, len(param_data['status'])):
        if param_data['profit'].loc[i] < 0:
            param_data['status'].loc[i] = 'perdedora'

    # ratios
    param_data['ratio_ganadoras'] = 0
    param_data['ratio_perdedoras'] = 0
    for i in range(0, len(param_data['profit'])):
        if param_data['status'].loc[i] == 'ganadora':
            param_data['ratio_ganadoras'].loc[i] = param_data['profit'].loc[i] / param_data['capital_acum'].loc[i] * 100
        else:
            param_data['ratio_perdedoras'].loc[i] = param_data['profit'].loc[i] / param_data['capital_acum'].loc[
                i] * 100

    # df de operaciones ganadas y df de operaciones perdidas
    ganadoras = param_data[param_data['status'] == "ganadora"].reset_index()
    perdedoras = param_data[param_data['status'] == "perdedora"].reset_index()

    # inicializar variables
    ocurrencias = 0
    status_quo = 0
    aversion_perdida = 0
    sensibilidad_decreciente = 0

    # DataFrame estadisticas
    estadisticas = pd.DataFrame(columns=['ocurrencias', 'status_quo', 'aversion_perdida', 'sensibilidad_decreciente'])

    # Crear diccionario
    parte_4 = {'ocurrencias': {'ocurrencias': ocurrencias}, 'resultados': estadisticas}

    # Sesgos cognitivos
    for i in range(0, len(ganadoras['status'])):
        ganadora = ganadoras.loc[i]
        for j in range(0, len(perdedoras['status'])):
            perdedora = perdedoras.loc[j]
            if perdedora['opentime'] < ganadora['closetime'] < perdedora['closetime']:
                ocurrencias = ocurrencias + 1
                nombre = 'ocurrencia_' + str(ocurrencias)
                fecha_ganadora = ganadora['closetime']  # cierre operacion ganadora que tiene el sesgo
                parte_4['ocurrencias'][nombre] = {'timestamp': fecha_ganadora, 'operaciones': {'ganadora': {
                    'instrumento': ganadora['symbol'], 'volumen': ganadora['size'], 'sentido': ganadora['type'],
                    'capital_ganadora': ganadora['profit']}, 'perdedora': {'instrumento': perdedora['symbol'],
                                                                           'volumen': perdedora['size'],
                                                                           'sentido': perdedora['type'],
                                                                           'capital_ganadora': perdedora['profit']}},
                                                      'ratio_cp_capital_acm': perdedora['ratio_perdedoras'],
                                                      'ratio_cg_capital_acm': ganadora['ratio_ganadoras'],
                                                      'ratio_cp_cg': perdedora['profit'] / ganadora['profit']
                                                      }
                if np.abs(perdedora['profit'] / perdedora['capital_acum']) < ganadora['profit'] / ganadora[
                    'capital_acum']:
                    status_quo = status_quo + 1
                if np.abs(perdedora['profit'] / ganadora['profit']) > 1.5:
                    aversion_perdida = aversion_perdida + 1
                if ganadoras['capital_acum'].iloc[i-1] > ganadoras['capital_acum'].iloc[i] and \
                        np.abs(perdedoras['profit'].iloc[i-1] / ganadoras['profit'].iloc[i]) > 1.5 and \
                        (ganadoras['profit'].iloc[i-1] > ganadoras['profit'].iloc[i] or
                         perdedoras['profit'].iloc[i-1] > perdedoras['profit'].iloc[i]):
                    sensibilidad_decreciente = sensibilidad_decreciente + 1

    parte_4['ocurrencias']['ocurrencias'] = ocurrencias
    parte_4['resultados'] = parte_4['resultados'].append({'ocurrencias': ocurrencias,
                                                                  'status_quo': status_quo / ocurrencias * 100,
                                                                  'aversion_perdida': aversion_perdida / ocurrencias * 100,
                                                                  'sensibilidad_decreciente': 'no'},
                                                                 ignore_index=True)

    if ganadoras['capital_acum'].iloc[-1] > ganadoras['capital_acum'].iloc[0] and \
            np.abs(perdedoras['profit'].min() / ganadoras['profit'].max()) > 1.5 and \
            (ganadoras['profit'].iloc[-1] > ganadoras['profit'].iloc[0] or
             perdedoras['profit'].iloc[-1] > perdedoras['profit'].iloc[0]):
        parte_4['resultados']['sensibilidad_decreciente'][0] = 'si'

    vs.barra(status_quo=status_quo, aversion_riesgo=aversion_perdida, sensibilidad_decreciente=sensibilidad_decreciente)
    return parte_4 #Se regresa el diccionario con el sesgo cognitivo y sus estadisticas
