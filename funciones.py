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

    return param_data



