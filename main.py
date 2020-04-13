# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: main.py - flujo principal del proyecto
# -- mantiene: Hermela Peña
# -- repositorio: https://github.com/hermelap/LAB_2_HPH
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn
import visualizaciones as vs

df_data = fn.f_leer_archivo(param_archivo='archivo_tradeview_1.xlsx')
fn.f_pip_size(param_ins='usdmxn')
df_data = fn.f_columnas_tiempos(param_data=df_data)
df_data = fn.f_columnas_pips(param_data=df_data)
df_estadisticas_ba = fn.f_estadisticas_ba(param_data=df_data)
df_profit_diario = fn.f_profit_diario(param_data=df_data)
df_estadisticas_mad = fn.f_estadisticas_mad(param_data=df_data)
sesgo = fn.f_be_de(df_data)
grafica_1 = vs.pastel(diccionario=df_estadisticas_ba) # Grafica de pastel ranking
grafica_2 = vs.linea(datos=df_profit_diario, estadisticos=df_estadisticas_mad) # Grafica de DrawDown y DrawUp
