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