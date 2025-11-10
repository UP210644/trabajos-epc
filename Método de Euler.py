import numpy as np
import matplotlib.pyplot as plt

def metodo_euler(f, x0, y0, h, x_final):
    """
    Resuelve una EDO de primer orden y' = f(x, y) usando el Método de Euler.

    Parámetros:
    f: La función (EDO) que define la pendiente, f(x, y).
    x0: Condición inicial para x.
    y0: Condición inicial para y (es decir, y(x0) = y0).
    h: Tamaño del paso.
    x_final: Valor final de x hasta donde se quiere la aproximación.

    Retorna:
    (list, list): Dos listas, una con los valores de x y otra con los
                  valores aproximados de y.
    """
    
    x_puntos = [x0]
    y_puntos = [y0]

    # Calculamos el número de pasos necesarios
    n_pasos = int(round((x_final - x0) / h))

    x = x0
    y = y0
