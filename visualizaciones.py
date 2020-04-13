# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: visualizaciones.py - para graficar datos
# -- mantiene: Hermela Peña
# -- repositorio: https://github.com/hermelap/LAB_2_HPH
# -- ------------------------------------------------------------------------------------ -- #

import numpy as np
from plotly import graph_objs as go
import plotly.io as pio
import pandas as pd

pio.renderers.default = 'browser'


def pastel(diccionario):
    def porcentaje_a_decimal(v):
        return float(v.strip('%')) / 100

    def maximo(array):
        mayor = np.argmax(array)
        sacar = np.zeros_like(array)
        sacar[mayor] = 0.25
        return sacar

    tickers = np.array(diccionario['df_2_ranking']['symbol'])
    valores = []
    for x in diccionario['df_2_ranking']['rank']:
        valores.append(porcentaje_a_decimal(x))
    grafica = go.Figure(go.Pie(labels=tickers, values=valores, pull=maximo(valores)))
    grafica.update_layout(title_text='Grafica 1 Ranking')
    grafica.show()

    return grafica


def linea(datos, estadisticos):
    """

    Parameters
    ----------
    datos: datos diarios
    estadisticos: estadisticas de medidas de atribucion al desempeño

    Returns
    -------
    grafica de linea con draw down y draw up

    Debugging
    ------
    datos = df_data
    estadisticos = df_estadisticos_mad

    """

    datos.index = datos['timestamp']
    grafica = go.Figure(go.Scatter(x=datos['timestamp'], y=datos['profit_acm_d'], marker_color='Black'))

    # Calcular linea de draw down
    inicio = pd.to_datetime(estadisticos['valor'].loc[3].split()[0])
    fin = pd.to_datetime(estadisticos['valor'].loc[3].split()[2])
    valor_inicial = datos['profit_acm_d'][inicio]
    valor_final = datos['profit_acm_d'][fin]
    grafica.add_shape(type='line', x0=inicio, x1=fin, y0=valor_inicial, y1=valor_final,
                      line=dict(color='Red', dash='dot'))

    # Calcular linea de draw up
    inicio = pd.to_datetime(estadisticos['valor'].loc[4].split()[0])
    fin = pd.to_datetime(estadisticos['valor'].loc[4].split()[2])
    valor_inicial = datos['profit_acm_d'][inicio]
    valor_final = datos['profit_acm_d'][fin]
    grafica.add_shape(type='line', x0=inicio, x1=fin, y0=valor_inicial, y1=valor_final,
                      line=dict(color='Green', dash='dot'))
    grafica.update_layout(title_text='Gráfica 2: DrawDown y DrawUp')
    grafica.show()

    return grafica


def barra(status_quo, aversion_riesgo, sensibilidad_decreciente):
    """

    Parameters
    ----------
    status_quo
    aversion_riesgo
    sensibilidad_decreciente

    Returns
    -------
    grafica

    Debugging
    -----
    status_quo = 1
    aversion_riesgo = 1
    sensibilidad_decreciente = 1


    """
    grafica = go.Figure(go.Bar(x=['status_quo', 'aversion_perdida', 'sensibilidad_decreciente'],
                               y=[status_quo, aversion_riesgo, sensibilidad_decreciente]))
    grafica.update_layout(title_text='Gráfica 3: Disposition Effect')
    grafica.show()
