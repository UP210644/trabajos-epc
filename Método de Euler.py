# --- 1. Importaciones" ---

import math  # Trae la "calculadora científica" (para seno, coseno, raíz, pi, etc.)
import numpy as np  # Trae una "calculadora avanzada" para listas (la usaremos para la gráfica)
import matplotlib.pyplot as plt  # Trae el "equipo de dibujo" (para hacer la gráfica)
import sys  # Trae el "interruptor de emergencia" (para poder parar el programa con Ctrl+C)


# --- 2. El "Traductor de Ecuaciones" Seguro ---

# Esta es la "lista de invitados" de las matemáticas que permitimos.
# Es una medida de seguridad para que el programa solo pueda "hablar" de matemáticas.
ALLOWED_FUNCTIONS = {
    k: v for k, v in math.__dict__.items() if not k.startswith('_')
}
ALLOWED_FUNCTIONS['abs'] = abs  # Permitimos el valor absoluto
ALLOWED_FUNCTIONS['pow'] = pow  # Permitimos las potencias

def create_function(expr_str, var_names):
    """
    Toma un texto (ej. "x**2") y lo convierte en una orden matemática
    real que la computadora entiende (una "función").
    """
    try:
        # "Intenta" hacer lo siguiente:
        
        # Aquí "traducimos" el texto a una función.
        # Lo hacemos en una "habitación segura":
        #  {"__builtins__": {}} -> Le quitamos todos los "juguetes" peligrosos de Python.
        #  ALLOWED_FUNCTIONS  -> Le damos solo la "lista de invitados" de matemáticas.
        func = eval(
            f"lambda {','.join(var_names)}: {expr_str}",
            {"__builtins__": {}},
            ALLOWED_FUNCTIONS
        )
        
        # Hacemos una prueba rápida (con x=1, y=1) para ver si la fórmula está bien escrita.
        test_args = [1] * len(var_names)
        func(*test_args)
        
        # Si todo salió bien, devolvemos la función lista para usarse.
        return func
        
    except Exception as e:
        # Si la "traducción" falla (ej. falta un paréntesis), atrapa el error aquí.
        print(f"\n--- ERROR: No entendí esa fórmula: '{expr_str}' ---")
        print(f"Revisa si está bien escrita (ej. 'x**2', 'math.sin(y)').\n")
        return None # Devuelve "nada" para que el programa sepa que falló.

