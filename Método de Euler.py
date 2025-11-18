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

# --- 3. Las Funciones del "Entrevistador" ---

def get_numerical_input(prompt):
    """
    Esta función es un "portero". Pide un número y no te deja pasar 
    hasta que escribas un número válido.
    """
    while True: # Se queda preguntando una y otra vez...
        try:
            # Intenta convertir tu respuesta en un número (con decimales).
            return float(input(prompt))
        except ValueError:
            # Si escribes "hola" en lugar de "5", te dice "inválido" y vuelve a preguntar.
            print("Eso no es un número. Intenta de nuevo.")

def get_user_input():
    """
    Esta función es el "entrevistador". Habla contigo y reúne
    todos los datos necesarios para resolver el problema.
    """
    
    # Imprime el mensaje de bienvenida
    print("="*50)
    print("  SOLUCIONADOR DE EDOs POR MÉTODO DE EULER  ")
    print("="*50)
    print("Puedes usar funciones como: math.sin, math.cos, math.sqrt, math.pi, etc.")
    print("Recuerda que 'potencia' se escribe con ** (ej. x**2).\n")

    # 1. Pregunta por la ecuación (la EDO)
    f_func = None
    while f_func is None: # Repite la pregunta hasta que la fórmula esté bien escrita
        f_str = input("Introduce la EDO dy/dx = f(x, y): ")
        f_func = create_function(f_str, ['x', 'y']) # Llama al "traductor"
        
    # 2. Pregunta por los números iniciales
    x0 = get_numerical_input("Introduce el valor inicial x0:      ")
    y0 = get_numerical_input("Introduce el valor inicial y0 (y(x0)): ")
    h = get_numerical_input("Introduce el tamaño de paso (h):     ")
    x_final = get_numerical_input("Introduce el valor final de x:       ")
    
    # 3. Pregunta (opcional) por la respuesta "real"
    g_func = None
    has_analitica = input("\n¿Tienes la solución 'real' (analítica) para comparar? (s/n): ").lower().strip()
    if has_analitica == 's':
        while g_func is None: # Repite hasta que la fórmula esté bien escrita
            g_str = input("Introduce la solución g(x) =       ")
            g_func = create_function(g_str, ['x']) # Llama al "traductor"
    
    # Al final, empaqueta todas tus respuestas y las devuelve.
    return f_func, g_func, x0, y0, h, x_final

