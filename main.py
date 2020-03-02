
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: main.py - flujo principal del proyecto
# -- mantiene: Hermela Peña
# -- repositorio: https://github.com/hermelap/LAB_2_HPH
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn

df_data = fn.f_leer_archivo(param_archivo='archivo_oanda.xlsx')
fn.f_pip_size(param_ins = 'usdmxn')
datos = fn.f_columnas_datos(param_data=datos)
