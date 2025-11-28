# --- 1. Librerías necesarias ---
# Estas son herramientas que necesitamos para que el programa funcione

import math  # Contiene funciones matemáticas como seno, coseno, raíz cuadrada, etc.
import numpy as np  # Nos ayuda a trabajar con listas de números de manera eficiente
import matplotlib.pyplot as plt  # Nos permite crear gráficas para visualizar los resultados
import sys  # Nos da herramientas del sistema, como poder parar el programa


# --- 2. Conversor seguro de ecuaciones ---
# Esta sección convierte las fórmulas que escribes en funciones que la computadora puede usar

# Creamos una lista de operaciones matemáticas permitidas para mantener seguridad
# Solo permitimos cálculos matemáticos, nada que pueda dañar el sistema
ALLOWED_FUNCTIONS = {
    k: v for k, v in math.__dict__.items() if not k.startswith('_')
}
ALLOWED_FUNCTIONS['abs'] = abs  # Añadimos la función de valor absoluto
ALLOWED_FUNCTIONS['pow'] = pow  # Añadimos la función de potencias

def create_function(expr_str, var_names):
    """
    Convierte un texto como "x**2" en una función que la computadora puede usar.
    Es como crear una calculadora personalizada según la fórmula que escribiste.
    """
    try:
        # Intentamos crear la función paso a paso
        
        # Convertimos tu texto en una función matemática real
        # Usamos medidas de seguridad para evitar comandos peligrosos:
        # - Bloqueamos acceso a funciones del sistema que podrían ser peligrosas
        # - Solo permitimos las operaciones matemáticas de nuestra lista segura
        func = eval(
            f"lambda {','.join(var_names)}: {expr_str}",
            {"__builtins__": {}},
            ALLOWED_FUNCTIONS
        )
        
        # Probamos la función con números sencillos para verificar que funciona
        # Es como probar una máquina nueva antes de usarla en serio
        test_args = [1] * len(var_names)
        func(*test_args)
        
        # Si llegamos aquí, la función se creó correctamente
        return func
        
    except Exception as e:
        # Si hubo algún error en la fórmula, informamos al usuario qué salió mal
        print(f"\n--- ERROR: No pude entender esta fórmula: '{expr_str}' ---")
        print(f"Revisa que esté bien escrita. Ejemplos: 'x**2', 'math.sin(y)', 'x*y + 5'\n")
        return None # Devolvemos 'nada' para indicar que falló

# --- 3. Funciones para obtener datos del usuario ---

def get_numerical_input(prompt):
    """
    Pide un número al usuario y verifica que sea válido.
    Si el usuario escribe algo que no es un número, le pide que lo intente de nuevo.
    No se detiene hasta recibir un número correcto.
    """
    while True: # Repite hasta conseguir un número válido
        try:
            # Intenta convertir la respuesta del usuario en un número decimal
            return float(input(prompt))
        except ValueError:
            # Si la conversión falla (porque escribió letras), pide intentar otra vez
            print("Por favor ingresa un número válido (ejemplo: 5, 3.14, -2.5)")

def get_user_input():
    """
    Recopila toda la información necesaria del usuario para resolver el problema.
    Hace todas las preguntas necesarias y verifica que las respuestas sean válidas.
    """
    
    # Muestra el título y las instrucciones al usuario
    print("="*50)
    print("  SOLUCIONADOR DE ECUACIONES DIFERENCIALES  ")
    print("="*50)
    print("Puedes usar funciones como: math.sin, math.cos, math.sqrt, math.pi, etc.")
    print("Para potencias usa **: por ejemplo x**2 significa x al cuadrado\n")

    # 1. Obtiene la ecuación diferencial del usuario
    # Esta ecuación describe cómo cambia y con respecto a x
    f_func = None
    while f_func is None: # Continúa preguntando hasta que la ecuación sea válida
        f_str = input("Introduce la EDO dy/dx = f(x, y): ")
        f_func = create_function(f_str, ['x', 'y']) # Convierte el texto en función
        
    # 2. Obtiene las condiciones iniciales y parámetros del método
    x0 = get_numerical_input("Introduce el valor inicial x0:      ")
    y0 = get_numerical_input("Introduce el valor inicial y0 (y(x0)): ")
    h = get_numerical_input("Introduce el tamaño de paso (h):     ")
    x_final = get_numerical_input("Introduce el valor final de x:       ")
    
    # 3. Pregunta si el usuario conoce la solución exacta para hacer comparaciones
    g_func = None
    has_analitica = input("\n¿Tienes la solución 'real' (analítica) para comparar? (s/n): ").lower().strip()
    if has_analitica == 's':
        while g_func is None: # Continúa hasta que la solución sea válida
            g_str = input("Introduce la solución g(x) =       ")
            g_func = create_function(g_str, ['x']) # Convierte el texto en función
    
    # Devuelve todos los datos recopilados para que el programa los use
    return f_func, g_func, x0, y0, h, x_final

# --- 4. Implementación del Método de Euler ---

def metodo_euler(f, x0, y0, h, x_final):
    """
    Implementa el método numérico de Euler para resolver la ecuación diferencial.
    Calcula paso a paso los valores aproximados y muestra una tabla con los resultados.
    """
    
    # Calcula cuántos pasos necesitamos para llegar desde x0 hasta x_final
    n_pasos = int(round(abs(x_final - x0) / h))
    
    if n_pasos == 0 and x0 != x_final:
        print("Error: El tamaño de paso 'h' es demasiado grande.")
        return [], [] # Devuelve listas vacías para indicar error
        
    # Crea listas para guardar todos los valores de x e y que vamos calculando
    x_valores = [0.0] * (n_pasos + 1)
    y_valores = [0.0] * (n_pasos + 1)
    
    # Guarda el punto inicial (el punto de partida que nos dio el usuario)
    x_valores[0] = x0
    y_valores[0] = y0
    
    # Muestra el encabezado de la tabla donde veremos todos los resultados
    print("\n--- Calculando con Método de Euler ---")
    print("--------------------------------------")
    print(f"| {'Paso':<4} | {'x':<10} | {'y (aprox)':<18} |")
    print("--------------------------------------")
    print(f"| {0:<4} | {x0:<10.4f} | {y0:<18.6f} |")

    # Aplicamos la fórmula de Euler para cada paso
    for i in range(n_pasos):
        x_i = x_valores[i] # Valor actual de x
        y_i = y_valores[i] # Valor actual de y
        
        # Fórmula de Euler: y_nuevo = y_actual + h * f(x_actual, y_actual)
        # donde f(x,y) es nuestra ecuación diferencial
        try:
            # 1. Calcula la pendiente (derivada) en el punto actual usando nuestra ecuación
            pendiente = f(x_i, y_i)
        except (ValueError, ZeroDivisionError) as e:
            # Si hay un error matemático (como dividir por cero), para el cálculo
            print(f"¡Error en el paso {i+1}! No se puede calcular f({x_i}, {y_i}). Detalle: {e}")
            print("El cálculo se detendrá.")
            return x_valores[:i+1], y_valores[:i+1] # Devuelve lo que calculó hasta ahora
            
        # 2. Calcula el siguiente valor de y usando la fórmula de Euler
        y_siguiente = y_i + h * pendiente 
        
        # 3. Guarda los nuevos valores en nuestras listas
        # Calculamos x de esta forma para evitar errores de redondeo acumulados
        x_valores[i+1] = x0 + (i + 1) * h 
        y_valores[i+1] = y_siguiente
        
        # Muestra esta fila en la tabla de resultados
        print(f"| {i+1:<4} | {x_valores[i+1]:<10.4f} | {y_siguiente:<18.6f} |")
        
    print("--------------------------------------")
    print("Cálculo completado.")
    
    # Devuelve todas las listas con los valores calculados
    return x_valores, y_valores

# --- 5. Generador de gráficas ---

def plot_results(x_euler, y_euler, g_func, x0, x_final, h):
    """
    Crea una gráfica que muestra los resultados del método de Euler.
    Si hay una solución analítica, también la dibuja para hacer comparaciones.
    """
    if not x_euler: # Verifica si hay datos para graficar
        print("No hay datos para dibujar.")
        return

    # Crea una nueva figura (ventana) para la gráfica
    plt.figure(figsize=(10, 6))
    
    # 1. Dibuja los puntos calculados con el método de Euler
    # 'bo--' significa: puntos azules (b=blue, o=circles) unidos con línea discontinua (--)
    plt.plot(x_euler, y_euler, 'bo--', label=f'Solución de Euler (h={h})')
    
    # 2. Si el usuario proporcionó la solución exacta, también la dibujamos
    if g_func is not None:
        # Crea muchos puntos intermedios para que la curva se vea suave
        x_analitica = np.linspace(x0, x_final, 1000)
        try:
            # Calcula los valores de la solución exacta en todos esos puntos
            y_analitica = [g_func(x) for x in x_analitica]
            # Dibuja la solución exacta como una línea roja continua
            plt.plot(x_analitica, y_analitica, 'r-', label='Solución analítica')
        except Exception as e:
            print(f"Error al dibujar la solución analítica: {e}")
    
    # 3. Añade etiquetas y título para que la gráfica sea fácil de entender
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Comparación: Método de Euler vs Solución Analítica')
    plt.legend() # Muestra la leyenda explicando qué línea es qué
    plt.grid(True) # Añade una cuadrícula para facilitar la lectura
    
    # 4. Muestra la gráfica en pantalla
    plt.show()

# --- 6. Función principal del programa ---

def main():
    """
    Función principal que coordina todo el programa.
    Llama a las otras funciones en el orden correcto para resolver el problema completo.
    """
    try:
        # 1. Obtiene todos los datos del usuario
        f_func, g_func, x0, y0, h, x_final = get_user_input()
        
        # 2. Aplica el método de Euler para resolver la ecuación
        x_euler, y_euler = metodo_euler(f_func, x0, y0, h, x_final)
        
        # 3. Crea la gráfica con los resultados
        if x_euler:  # Solo si se pudieron calcular resultados
            plot_results(x_euler, y_euler, g_func, x0, x_final, h)
        
        # 4. Muestra un resumen con los resultados principales
        print("\n--- Resumen Final ---")
        print(f"Punto inicial: ({x0}, {y0})")
        print(f"Punto final calculado: ({x_euler[-1]:.4f}, {y_euler[-1]:.6f})" if x_euler else "No se pudo calcular")
        print(f"Tamaño de paso usado: {h}")
        print(f"Número de pasos: {len(x_euler)-1 if x_euler else 0}")
        
        if g_func is not None and x_euler:
            try:
                # Si hay solución exacta, calcula qué tan cerca estuvo nuestro resultado
                y_real = g_func(x_euler[-1])
                error = abs(y_euler[-1] - y_real)
                print(f"Valor real en x_final: {y_real:.6f}")
                print(f"Error absoluto: {error:.6f}")
            except Exception as e:
                print(f"No se pudo calcular el error: {e}")
        
    except KeyboardInterrupt:
        # Si el usuario presiona Ctrl+C para interrumpir el programa
        print("\n\nPrograma interrumpido por el usuario. ¡Hasta luego!")
    except Exception as e:
        # Si ocurre cualquier otro error inesperado, lo maneja de forma elegante
        print(f"\nOcurrió un error inesperado: {e}")
        print("Por favor, revisa tus datos e intenta de nuevo.")

# --- 7. Punto de inicio del programa ---

if __name__ == "__main__":
    # Esta línea verifica si el archivo se está ejecutando directamente
    # (no siendo importado como parte de otro programa)
    # Si es así, ejecuta la función principal
    main()
