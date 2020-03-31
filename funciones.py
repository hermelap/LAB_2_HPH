# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - para procesamiento de datos
# -- mantiene: Hermela Peña
# -- repositorio: https://github.com/hermelap/LAB_2_HPH
# -- ------------------------------------------------------------------------------------ -- #

import pandas as pd
import numpy as np


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
    param_archivo : str : con info de historicos
    Returns
    ------
    df_data : pd.Dataframe : con inforamcion contenida en archivo leido

    Debugging
    -----
    param_archivo = 'archivo_oanda.xlsx'

    """
    ## tranformar a minusculas
    inst = param_ins.replace('-', '')

    # lista de pips por instrumento
    pips_inst = {'usdmxn': 10000, 'eurusd': 10000}

    return pips_inst[inst]


def f_columnas_tiempos(param_data):
    """
    Parameters
    ------------
    param_archivo : str : close y open time
    Returns diferencia entre el open y el close time
    ------
    df_data : pd.Dataframe : con inforamcion contenida en archivo leido

    Debugging
    -----
    param_archivo = 'archivo_oanda.xlsx'

    """

    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])

    param_data['tiempo'] = [(param_data.loc[i, 'closetime'] - param_data.loc[i, 'opentime']).delta / 1e9
                            for i in range(0, len(param_data['closetime']))]

    return param_data


def f_columnas_pips(param_data):
    """
    Parameters
    ------------
    param_archivo : str : transformaciones de pips
    Returns valor acumulado de los pips
    ------
    df_data : pd.Dataframe : con inforamcion contenida en archivo leido

    Debugging
    -----
    param_archivo = 'archivo_oanda.xlsx'

    """
    param_data['pips'] = [

    compras = np.where(param_data['type'] == 'buy')[0]
    param_data['pips'][compras] = (param_data['closeprice'][compras]) - \
                                  (param_data['openprice'][compras])

    ventas = np.where(param_data['type'] == 'sell')[0]
    param_data['pips'][ventas] = (param_data['openprice'][ventas]) - \
                                 (param_data['closeprice'][ventas])
    ]

    # calcular los pips acumulados de perdidas o ganancias
    param_data['pips_acum'] = param_data['pips'].cumsum()

    # calcular la ganancia o perdida acumulada de la cuenta
    param_data['profit_acm'] = param_data['profit'].cumsum()

    # calcular el capital acumulado por operacion
    param_data['capital_acm'] = 0
    param_data['capital_acm'][0] = init_invest + param_data['profit'][0]
    for i in range(1, len(param_data.index)):
        param_data['capital_acm'][i] = param_data['capital_acm'][i - 1] + param_data['profit'][i]

    return param_data

def f_estadisticas_ba(param_data):
    """

    :param param_data: Dataframe conteniendo las operaciones realizadas en la cuenta
    :return: Diccionario conteniendo 2 dataframes:
                1. Concentrado de las estadisticas basicas de la cuenta
                2. ranking de los activos utilizados (% de ganadas/perdidas por cada activo utilizado)

    Debugging
    --------
    param_data = datos
    """

    # lista
    medidas = np.array(['Ops totales',
                        'Ganadoras',
                        'Ganadoras_c',
                        'Ganadoras_v',
                        'Perdedoras',
                        'Perdedoras_c',
                        'Perdedoras_v',
                        'Media (Profit)',
                        'Media (Pips)',
                        'r_efectividad',
                        'r_proporcion',
                        'r_efectividad_c',
                        'r_efectividad_v'])

    # lista de descripciones de dataframe de las columnas de arriba

    descripciones = np.array(['Operaciones totales',
                              'Operaciones ganadoras',
                              'Operaciones ganadoras de compra',
                              'Operaciones ganadoras de venta',
                              'Operaciones perdedoras',
                              'Operaciones perdedoras de compra',
                              'Operaciones perdedoras de venta',
                              'Mediana de profit de operaciones',
                              'Mediana de pips de operaciones',
                              'Operaciones Totales Vs Ganadoras Totales',
                              'Ganadoras Totales Vs Perdedoras Totales',
                              'Totales Vs Ganadoras Compras',
                              'Totales Vs Ganadoras Ventas'])

    # crear el dataframe
    df_1_tabla = pd.DataFrame(columns=['medidas', 'valor'],
                              index=np.array([i for i in range(0, len(medidas))]))
    # Llenar las medidas
    df_1_tabla['medidas'] = [medidas[i] for i in range(0, len(df_1_tabla.index))]

    # Llenar las descripciones
    df_1_tabla['descripcion'] = [descripciones[i] for i in range(0, len(df_1_tabla.index))]

    # llenado de informacion
    df_1_tabla.loc[0, 'valor'] = len(param_data.index)
    df_1_tabla.loc[1, 'valor'] = sum(1 for i in param_data.index if param_data.loc[i, 'profit'] >= 0)
    df_1_tabla.loc[2, 'valor'] = sum(1 for i in param_data.index if param_data.loc[i, 'profit'] >= 0 and
                                     param_data.loc[i, 'type'] == 'buy')
    df_1_tabla.loc[3, 'valor'] = sum(1 for i in param_data.index if param_data.loc[i, 'profit'] >= 0 and
                                     param_data.loc[i, 'type'] == 'sell')
    df_1_tabla.loc[4, 'valor'] = sum(1 for i in param_data.index if param_data.loc[i, 'profit'] < 0)
    df_1_tabla.loc[5, 'valor'] = sum(1 for i in param_data.index if param_data.loc[i, 'profit'] < 0 and
                                     param_data.loc[i, 'type'] == 'buy')
    df_1_tabla.loc[6, 'valor'] = sum(1 for i in param_data.index if param_data.loc[i, 'profit'] < 0 and
                                     param_data.loc[i, 'type'] == 'sell')
