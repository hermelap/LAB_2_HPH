# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - para procesamiento de datos
# -- mantiene: Hermela Peña
# -- repositorio: https://github.com/hermelap/LAB_2_HPH
# -- ------------------------------------------------------------------------------------ -- #

import pandas as pd

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

    df_data.columns = [list(df_data.columns)[i].lower()
                       for i in range(0, len(df_data.columns))]

   # Asegurar que ciertas columnas son del tipo numerico
   #Cambiar tipo de dato en columnas a numerico

    numcols = ['s/l', 't/p', 'commission', 'openprice', 'closeprice', 'profit', 'size', 'swap', 'taxes', 'order']
    df_data[numcols] = df_data[numcols].apply(pd.to_numeric)


    return df_data

    def f_pip_size(param_ins):

    #tranformar a minusculas
    inst =  param_ins.lower('-', '')

    #lista de pips por instrumento
    pips_inst = ('usdjpy': 100, 'gbpjpy': 100)

    return pips_inst[inst]

def f_columnas_datos(param_data):

    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])

    param_data['tiempo'] = [(param_data.loc[i, 'closetime'] - param_data.loc[i, 'opentime']).delta/1e9
         for i in range(0, len(param_data['closetime']))]

    return 1

