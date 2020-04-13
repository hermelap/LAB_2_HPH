Soy estudiante de octavo semestre de Ingeniería Financiera en el ITESO y para la clase de Microestructura y Sistemas de Trading realizamos este laboratorio que tiene como propósito el analizar el desempeño de una cuenta de trading, utilizando distintas herramientas como lo son, las medidas de atribución del desempeño, estadísticas básicas, y los sesgos cognitivos del trader.
Mi correo para cualquier duda es if708598@iteso.mx

LAB_2_HPH  notebook: Descripción del proyecto con código

main.py : Código principal del proyecto

funciones.py : Funciones para la ejecución de los calculos

visualizaciones.py : Funciones para graficar

Datos.py : Datos extras para el funcionamiento (token de Oanda)

Explicacion del código: 

Empezamos importando las librerías y el archivo que vamos a analizar.

Creamos el data frame con las fechas, montos y conversión a pips, para poder empezar con los cálculos de las estadísticas básicas y el ranking de los activos.

Después empezamos con las medidas de atribución al desempeño (MAD), se calculó el promedio de los rendimientos logarítmicos de los profits acumulados, calculamos el DrawDown y DrawUp.

Posteriormente pasamos a la propuesta, diseño y calculo de una función para evidenciar la presencia de sesgos congnitivos en el trader.

La ultima parte, fue graficar el ranking de los activos en una gráfica de pastel, graficar el DrawDown y DrawUp en una gráfica de línea y por último graficar el Disposition Effect en una grafica de barras.
