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
    # Bucle principal del método
    for i in range(n_pasos):
        # Aplicamos la fórmula de Euler:
        # y_nuevo = y_actual + h * f(x_actual, y_actual)
        y_nuevo = y + h * f(x, y)
        
        # Avanzamos al siguiente punto x
        x = x + h

        # Actualizamos 'y' para la siguiente iteración
        y = y_nuevo

        # Guardamos los resultados (redondeamos 'x' para evitar errores de flotante)
        x_puntos.append(round(x, 5)) 
        y_puntos.append(y)

    return x_puntos, y_puntos

# -----------------------------------------------------------------
# --- CONFIGURACIÓN DEL PROBLEMA (BASADO EN EL VIDEO) ---
# -----------------------------------------------------------------

# 1. Definimos la EDO del video: y