# --- 1. Importaciones ---

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

# --- 4. El "Motor de Cálculo" (Método de Euler) ---

def metodo_euler(f, x0, y0, h, x_final):
    """
    Este es el "motor de cálculo". Hace todo el trabajo pesado de Euler
    y te va mostrando la tabla de resultados.
    """
    
    # Calcula cuántos "pasos" necesita dar para llegar del inicio al final.
    n_pasos = int(round(abs(x_final - x0) / h))
    
    if n_pasos == 0 and x0 != x_final:
        print("Error: El tamaño de paso 'h' es demasiado grande.")
        return [], [] # Devuelve listas vacías
        
    # Prepara las "hojas" donde anotará los resultados de 'x' e 'y'.
    x_valores = [0.0] * (n_pasos + 1)
    y_valores = [0.0] * (n_pasos + 1)
    
    # Escribe el primer punto (tu punto de partida) en las hojas.
    x_valores[0] = x0
    y_valores[0] = y0
    
    # Dibuja la parte de arriba de la tabla de resultados.
    print("\n--- Calculando con Método de Euler ---")
    print("--------------------------------------")
    print(f"| {'Paso':<4} | {'x':<10} | {'y (aprox)':<18} |")
    print("--------------------------------------")
    print(f"| {0:<4} | {x0:<10.4f} | {y0:<18.6f} |")

    # Ahora, repite el cálculo para cada "paso" que necesita dar.
    for i in range(n_pasos):
        x_i = x_valores[i] # Mira dónde está parado actualmente en 'x'
        y_i = y_valores[i] # Mira dónde está parado actualmente en 'y'
        
        # Esta es la fórmula mágica de Euler:
        # y_nuevo = y_actual + (tamaño_paso * inclinación)
        try:
            # 1. Calcula la "inclinación" (pendiente) usando tu ecuación.
            pendiente = f(x_i, y_i)
        except (ValueError, ZeroDivisionError) as e:
            # Si algo sale mal (ej. ¡dividir por cero!), se detiene de forma segura.
            print(f"¡Error en el paso {i+1}! No se puede calcular f({x_i}, {y_i}). Detalle: {e}")
            print("El cálculo se detendrá.")
            return x_valores[:i+1], y_valores[:i+1] # Devuelve lo que alcanzó a calcular
            
        # 2. Calcula dónde estará el siguiente punto 'y'.
        y_siguiente = y_i + h * pendiente 
        
        # 3. Anota los nuevos puntos 'x' e 'y' en las hojas.
        # (Calculamos 'x' así para que no acumule errores de decimales)
        x_valores[i+1] = x0 + (i + 1) * h 
        y_valores[i+1] = y_siguiente
        
        # Escribe esta nueva fila de resultados en la pantalla.
        print(f"| {i+1:<4} | {x_valores[i+1]:<10.4f} | {y_siguiente:<18.6f} |")
        
    print("--------------------------------------")
    print("Cálculo completado.")
    
    # Cuando termina, entrega las "hojas" con todos los resultados.
    return x_valores, y_valores

# --- 5. El "Artista" (Dibujante de Gráficas) ---

def plot_results(x_euler, y_euler, g_func, x0, x_final, h):
    """
    Este es el "artista". Toma los resultados del "motor de cálculo"
    y los dibuja en una gráfica bonita.
    """
    if not x_euler: # Si no hay nada que dibujar (porque hubo un error antes)
        print("No hay datos para dibujar.")
        return

    # Saca un "lienzo" en blanco para dibujar.
    plt.figure(figsize=(10, 6))
    
    # 1. Dibuja la solución de Euler (la aproximada)
    # 'bo--' significa: 'b' (azul), 'o' (puntos), '--' (línea discontinua).
    plt.plot(x_euler, y_euler, 'bo--', label=f'Solución de Euler (h={h})')
    
    # 2. Si hay una solución "real" (analítica), también la dibuja para comparar
    if g_func is not None:
        # Crea muchos puntos entre x0 y x_final para que la curva se vea suave.
        x_analitica = np.linspace(x0, x_final, 1000)
        try:
            # Calcula la solución "real" para todos esos puntos.
            y_analitica = [g_func(x) for x in x_analitica]
            # La dibuja con una línea roja continua.
            plt.plot(x_analitica, y_analitica, 'r-', label='Solución analítica')
        except Exception as e:
            print(f"Error al dibujar la solución analítica: {e}")
    
    # 3. Le pone títulos y etiquetas a la gráfica
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Comparación: Método de Euler vs Solución Analítica')
    plt.legend() # Muestra la "leyenda" (qué color es qué línea)
    plt.grid(True) # Pone una "rejilla" para que sea más fácil leer los valores
    
    # 4. Muestra la gráfica en pantalla
    plt.show()

# --- 6. La Función "Jefe" (Main) ---

def main():
    """
    Esta es la función "jefe". Coordina a todas las demás funciones
    para resolver el problema completo.
    """
    try:
        # 1. El "entrevistador" habla contigo y reúne los datos
        f_func, g_func, x0, y0, h, x_final = get_user_input()
        
        # 2. El "motor de cálculo" hace todo el trabajo pesado
        x_euler, y_euler = metodo_euler(f_func, x0, y0, h, x_final)
        
        # 3. El "artista" dibuja los resultados
        if x_euler:  # Solo si hay resultados que dibujar
            plot_results(x_euler, y_euler, g_func, x0, x_final, h)
        
        # 4. Muestra un resumen final
        print("\n--- Resumen Final ---")
        print(f"Punto inicial: ({x0}, {y0})")
        print(f"Punto final calculado: ({x_euler[-1]:.4f}, {y_euler[-1]:.6f})" if x_euler else "No se pudo calcular")
        print(f"Tamaño de paso usado: {h}")
        print(f"Número de pasos: {len(x_euler)-1 if x_euler else 0}")
        
        if g_func is not None and x_euler:
            try:
                # Si hay solución "real", calcula qué tan cerca estuvimos
                y_real = g_func(x_euler[-1])
                error = abs(y_euler[-1] - y_real)
                print(f"Valor real en x_final: {y_real:.6f}")
                print(f"Error absoluto: {error:.6f}")
            except Exception as e:
                print(f"No se pudo calcular el error: {e}")
        
    except KeyboardInterrupt:
        # Si presionas Ctrl+C, el programa se detiene elegantemente
        print("\n\nPrograma interrumpido por el usuario. ¡Hasta luego!")
    except Exception as e:
        # Si algo sale muy mal, muestra el error en lugar de que el programa "explote"
        print(f"\nOcurrió un error inesperado: {e}")
        print("Por favor, revisa tus datos e intenta de nuevo.")

# --- 7. El "Punto de Inicio" ---

if __name__ == "__main__":
    # Esto significa: "Si alguien ejecuta este archivo directamente 
    # (no lo está usando como una 'pieza' de otro programa), 
    # entonces ejecuta la función main()."
    main()
