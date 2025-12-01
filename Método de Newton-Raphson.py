# ===== LIBRERÍAS NECESARIAS =====
# Estas son herramientas que necesitamos para que el programa funcione

import numpy as np  # Nos ayuda a trabajar con cálculos matemáticos y listas de números
import matplotlib.pyplot as plt  # Nos permite crear gráficas para visualizar los resultados
import sympy as sp  # Biblioteca especializada en matemáticas simbólicas (derivadas automáticas)
from sympy import symbols, diff, lambdify  # Herramientas específicas para trabajar con símbolos y derivadas
import tkinter as tk  # Biblioteca para crear la interfaz gráfica (ventanas, botones, etc.)
from tkinter import ttk, messagebox  # Elementos adicionales de la interfaz (botones modernos, mensajes)

# ===== CLASE PRINCIPAL DEL CALCULADOR =====
# Esta clase contiene todo lo necesario para crear la interfaz gráfica y realizar los cálculos

class NewtonRaphsonCalculator:
    def __init__(self):
        """
        Inicializa el programa creando la ventana principal y preparando las herramientas matemáticas.
        """
        self.root = tk.Tk()  # Crea la ventana principal
        self.root.title("Método de Newton-Raphson")  # Le pone título a la ventana
        self.root.geometry("600x700")  # Define el tamaño de la ventana
        # Crea una variable simbólica 'x' que usaremos para las ecuaciones
        self.x = symbols('x')
        self.x = symbols('t')
        self.setup_ui()  # Llama a la función que creará todos los elementos visuales

    def setup_ui(self):
        """
        Crea toda la interfaz visual del programa: botones, campos de texto, áreas de resultados, etc.
        Es como diseñar y organizar todos los elementos de una aplicación.
        """
        # Crea el contenedor principal donde irán todos los elementos
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Crea y coloca el título principal de la aplicación
        title_label = ttk.Label(main_frame, text="Método de Newton-Raphson",
                                font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Texto explicativo sobre qué hace el método
        desc_text = """El método de Newton-Raphson es un algoritmo iterativo para encontrar 
las raíces de una función real. Fórmula: xₙ₊₁ = xₙ - f(xₙ)/f'(xₙ)"""
        desc_label = ttk.Label(main_frame, text=desc_text, justify=tk.CENTER)
        desc_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        # Sección para ingresar la función matemática
        ttk.Label(main_frame, text="Función f(x):", font=("Arial", 11, "bold")).grid(
            row=2, column=0, sticky=tk.W, pady=5)

        # Contenedor para el campo de la función
        func_frame = ttk.Frame(main_frame)
        func_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(func_frame, text="f(x) =").grid(row=0, column=0, padx=(0, 10))
        # Campo de texto donde el usuario escribirá su función
        self.func_entry = ttk.Entry(func_frame, width=40)
        self.func_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.func_entry.insert(0, "x**3 - 2*x - 5")  # Ejemplo por defecto

        # Ejemplos y ayudas para que el usuario sepa cómo escribir funciones
        examples = [
            "Ejemplos: x**2 - 4, exp(x) - 2, cos(x) - x, x**3 - 2*x - 5",
            "Usar: exp() para eˣ, log() para ln(x), sin(), cos(), tan()"
        ]

        # Muestra los ejemplos de funciones en pantalla para ayudar al usuario
        for i, example in enumerate(examples):
            example_label = ttk.Label(main_frame, text=example,
                                      font=("Arial", 9), foreground="gray")
            example_label.grid(row=4 + i, column=0, columnspan=2, sticky=tk.W, pady=2)

        # Sección de parámetros del método (valores que controlan cómo funciona el algoritmo)
        params_frame = ttk.LabelFrame(main_frame, text="Parámetros", padding="10")
        params_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Campo para el valor inicial (desde dónde empezamos a buscar la raíz)
        ttk.Label(params_frame, text="Valor inicial (x₀):").grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.x0_entry = ttk.Entry(params_frame, width=15)
        self.x0_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.x0_entry.insert(0, "2.0")  # Valor por defecto

        # Campo para la tolerancia (qué tan preciso queremos el resultado)
        ttk.Label(params_frame, text="Tolerancia:").grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.tol_entry = ttk.Entry(params_frame, width=15)
        self.tol_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        self.tol_entry.insert(0, "1e-6")  # Muy preciso por defecto

        # Campo para el máximo de iteraciones (cuántos intentos como máximo)
        ttk.Label(params_frame, text="Máx iteraciones:").grid(
            row=2, column=0, sticky=tk.W, pady=5)
        self.max_iter_entry = ttk.Entry(params_frame, width=15)
        self.max_iter_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        self.max_iter_entry.insert(0, "100")  # Suficientes intentos por defecto

        # Sección de botones principales del programa
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)

        # Botón para calcular la raíz usando el método de Newton-Raphson
        calc_btn = ttk.Button(button_frame, text="Calcular Raíz",
                              command=self.calculate_root)
        calc_btn.grid(row=0, column=0, padx=10)

        # Botón para crear una gráfica de la función y el proceso de convergencia
        graph_btn = ttk.Button(button_frame, text="Graficar Función",
                               command=self.plot_function)
        graph_btn.grid(row=0, column=1, padx=10)

        # Botón para limpiar todos los campos y empezar de nuevo
        clear_btn = ttk.Button(button_frame, text="Limpiar",
                               command=self.clear_fields)
        clear_btn.grid(row=0, column=2, padx=10)

        # Área donde se mostrarán los resultados del cálculo
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        results_frame.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        # Campo de texto grande para mostrar tablas y resultados detallados
        self.results_text = tk.Text(results_frame, height=12, width=70)
        # Barra de desplazamiento por si los resultados son muy largos
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical",
                                  command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)

        # Coloca el área de texto y la barra de desplazamiento en su posición
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Configuraciones para que los elementos se redimensionen correctamente con la ventana
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(8, weight=1)
        func_frame.columnconfigure(1, weight=1)
        params_frame.columnconfigure(1, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

    def parse_function(self, func_str):
        """
        Convierte un texto como "x**2 + 3*x - 5" en funciones matemáticas que la computadora puede usar.
        También calcula automáticamente la derivada que necesita el método de Newton-Raphson.
        """
        try:
            # Reemplaza ^ por ** porque Python usa ** para potencias
            func_str = func_str.replace('^', '**')
            # Convierte el texto en una expresión matemática simbólica
            expr = sp.sympify(func_str)
            # Crea funciones numéricas que pueden calcular valores rápidamente
            f = lambdify(self.x, expr, modules=['numpy'])  # La función original
            f_prime = lambdify(self.x, diff(expr, self.x), modules=['numpy'])  # Su derivada
            return f, f_prime, expr
        except Exception as e:
            # Si el texto no se puede convertir, muestra un error explicativo
            raise ValueError(f"Error en la función: {str(e)}")

    def newton_raphson(self, f, f_prime, x0, tol=1e-6, max_iter=100):
        """
        Implementa el algoritmo de Newton-Raphson para encontrar raíces de funciones.
        El método funciona dibujando líneas tangentes y siguiendo donde tocan el eje x.
        Repite este proceso hasta encontrar una aproximación muy precisa de la raíz.
        """
        iterations = []  # Lista para guardar el progreso de cada paso
        x = x0  # Empezamos desde el valor inicial que el usuario proporcionó

        for i in range(max_iter):  # Repetimos hasta el máximo de iteraciones permitidas
            fx = float(f(x))    # Calculamos f(x) en el punto actual
            fpx = float(f_prime(x))  # Calculamos f'(x) (la pendiente) en el punto actual

            # Verificamos que la derivada no sea cero (evita divisiones problemáticas)
            if abs(fpx) < 1e-12:
                raise ValueError("Derivada cercana a cero. El método puede no converger.")

            # Aplicamos la fórmula de Newton-Raphson: x_nuevo = x_actual - f(x)/f'(x)
            x_new = x - fx / fpx
            error = abs(x_new - x)  # Calculamos qué tanto cambió el resultado

            # Guardamos toda la información de esta iteración
            iterations.append({
                'iter': i + 1,
                'x': x,
                'fx': fx,
                'fpx': fpx,
                'x_new': x_new,
                'error': error
            })

            # Verificamos si ya encontramos una solución suficientemente precisa
            if error < tol:
                x = x_new
                break  # Salimos del bucle porque ya tenemos la respuesta

            x = x_new  # Preparamos la siguiente iteración

        return x, iterations  # Devolvemos la raíz encontrada y todo el proceso

    def calculate_root(self):
        """
        Función principal que coordina todo el proceso de cálculo.
        Toma los datos de la interfaz, aplica el método de Newton-Raphson y muestra los resultados.
        """
        try:
            # Obtiene todos los parámetros que el usuario escribió en la interfaz
            func_str = self.func_entry.get()  # La función matemática
            x0 = float(self.x0_entry.get())   # Valor inicial
            tol = float(self.tol_entry.get()) # Tolerancia (precisión deseada)
            max_iter = int(self.max_iter_entry.get())  # Máximo de intentos

            # Convierte el texto de la función en funciones matemáticas utilizables
            f, f_prime, expr = self.parse_function(func_str)

            # Calcula la derivada simbólica para mostrar en los resultados
            derivada = diff(expr, self.x)

            # Ejecuta el método de Newton-Raphson
            raiz, iteraciones = self.newton_raphson(f, f_prime, x0, tol, max_iter)

            # Presenta todos los resultados en la interfaz de manera organizada
            self.mostrar_resultados(expr, derivada, raiz, iteraciones)

        except Exception as e:
            # Si algo sale mal, muestra un mensaje de error amigable al usuario
            messagebox.showerror("Error", f"Error en el cálculo: {str(e)}")

    def mostrar_resultados(self, expr, derivada, raiz, iteraciones):
        """
        Organiza y presenta todos los resultados del cálculo de manera clara y detallada.
        Muestra la función, su derivada, una tabla con cada iteración y el resultado final.
        """
        self.results_text.delete(1.0, tk.END)  # Limpia el área de resultados

        # Encabezado principal
        self.results_text.insert(tk.END, "MÉTODO DE NEWTON-RAPHSON\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")

        # Información sobre la función y su derivada
        self.results_text.insert(tk.END, f"Función: f(x) = {expr}\n")
        self.results_text.insert(tk.END, f"Derivada: f'(x) = {derivada}\n\n")

        # Tabla detallada con cada paso del método
        self.results_text.insert(tk.END, "ITERACIONES:\n")
        self.results_text.insert(tk.END, "-" * 80 + "\n")
        # Encabezado de la tabla explicando qué significa cada columna
        self.results_text.insert(tk.END,
                                 "{:<6} {:<12} {:<12} {:<12} {:<12} {:<12}\n".format(
                                     'Iter', 'xₙ', 'f(xₙ)', "f'(xₙ)", 'xₙ₊₁', 'Error'))
        self.results_text.insert(tk.END, "-" * 80 + "\n")

        # Muestra cada iteración con todos sus valores calculados
        for it in iteraciones:
            self.results_text.insert(tk.END,
                                     f"{it['iter']:<6} {it['x']:<12.6f} {it['fx']:<12.6f} "
                                     f"{it['fpx']:<12.6f} {it['x_new']:<12.6f} {it['error']:<12.2e}\n")

        # Resumen final con la solución encontrada
        self.results_text.insert(tk.END, "-" * 80 + "\n\n")
        if iteraciones:
            last_fx = iteraciones[-1]['fx']
        else:
            last_fx = float(sp.N(expr.subs(self.x, raiz)))
        self.results_text.insert(tk.END, f"RAÍZ ENCONTRADA: x = {raiz:.8f}\n")
        self.results_text.insert(tk.END, f"f({raiz:.8f}) = {last_fx:.2e}\n")
        self.results_text.insert(tk.END, f"Iteraciones realizadas: {len(iteraciones)}\n")

    def plot_function(self):
        """
        Crea gráficas visuales para mostrar la función y cómo converge el método.
        Genera dos gráficos: uno mostrando la función y su raíz, otro mostrando la velocidad de convergencia.
        """
        try:
            # Obtiene los datos necesarios de la interfaz
            func_str = self.func_entry.get()
            x0 = float(self.x0_entry.get())

            # Convierte la función de texto a funciones matemáticas
            f, f_prime, expr = self.parse_function(func_str)

            # Ejecuta el método para obtener la raíz y el proceso de convergencia
            raiz, iteraciones = self.newton_raphson(f, f_prime, x0)

            # Crea una figura con dos gráficos lado a lado
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

            # PRIMER GRÁFICO: La función y dónde está su raíz
            x_vals = np.linspace(raiz - 3, raiz + 3, 400)  # Puntos alrededor de la raíz
            y_vals = f(x_vals)  # Valores de la función en esos puntos

            ax1.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {expr}')
            ax1.axhline(y=0, color='k', linestyle='--', alpha=0.3)  # Línea horizontal en y=0
            ax1.axvline(x=raiz, color='r', linestyle='--', alpha=0.7, label=f'Raíz: {raiz:.6f}')  # Línea vertical en la raíz
            ax1.plot(raiz, float(f(raiz)), 'ro', markersize=8, label='Raíz encontrada')  # Punto donde está la raíz
            ax1.set_xlabel('x')
            ax1.set_ylabel('f(x)')
            ax1.set_title('Función y Raíz Encontrada')
            ax1.legend()
            ax1.grid(True, alpha=0.3)  # Rejilla para facilitar la lectura

            # SEGUNDO GRÁFICO: Cómo va disminuyendo el error en cada iteración
            errores = [it['error'] for it in iteraciones]  # Lista de errores por iteración
            iter_nums = [it['iter'] for it in iteraciones]  # Números de iteración

            if errores:
                # Usa escala logarítmica para ver mejor cómo disminuye el error
                ax2.semilogy(iter_nums, errores, 'go-', linewidth=2, markersize=6)
            ax2.set_xlabel('Iteración')
            ax2.set_ylabel('Error (escala log)')
            ax2.set_title('Convergencia del Error')
            ax2.grid(True, alpha=0.3)

            plt.tight_layout()  # Ajusta automáticamente el espaciado
            plt.show()  # Muestra las gráficas en pantalla

        except Exception as e:
            # Si hay algún problema, muestra un error amigable
            messagebox.showerror("Error", f"Error al graficar: {str(e)}")

    def clear_fields(self):
        """
        Resetea todos los campos de la interfaz a sus valores por defecto.
        Útil cuando el usuario quiere probar con una función diferente desde cero.
        """
        # Limpia y restaura el campo de la función
        self.func_entry.delete(0, tk.END)
        self.func_entry.insert(0, "x**3 - 2*x - 5")
        
        # Restaura los parámetros a valores estándar
        self.x0_entry.delete(0, tk.END)
        self.x0_entry.insert(0, "2.0")
        self.tol_entry.delete(0, tk.END)
        self.tol_entry.insert(0, "1e-6")
        self.max_iter_entry.delete(0, tk.END)
        self.max_iter_entry.insert(0, "100")
        
        # Limpia el área de resultados
        self.results_text.delete(1.0, tk.END)

    def run(self):
        """
        Inicia la interfaz gráfica y mantiene el programa funcionando.
        Esta función no termina hasta que el usuario cierre la ventana.
        """
        self.root.mainloop()


# ===== EJEMPLO SIN INTERFAZ GRÁFICA =====
# Esta sección muestra cómo usar el método de Newton-Raphson sin la interfaz visual

def ejemplo_newton_raphson():
    """
    Ejemplo básico que muestra el método de Newton-Raphson funcionando paso a paso.
    Útil para entender cómo funciona el algoritmo sin la complejidad de la interfaz gráfica.
    """
    print("EJEMPLO MÉTODO NEWTON-RAPHSON")
    print("=" * 40)

    # Definimos manualmente la función y su derivada
    def f(x):
        """Función ejemplo: f(x) = x³ - 2x - 5"""
        return x**3 - 2*x - 5

    def f_prime(x):
        """Derivada de f(x): f'(x) = 3x² - 2"""
        return 3*x**2 - 2

    # Parámetros del método
    x0 = 2.0      # Punto donde empezamos a buscar
    tol = 1e-6    # Qué tan preciso queremos el resultado
    max_iter = 100  # Máximo número de intentos

    # Muestra la información inicial
    print(f"Función: f(x) = x³ - 2x - 5")
    print(f"Derivada: f'(x) = 3x² - 2")
    print(f"Valor inicial: x0 = {x0}")
    print(f"Tolerancia: {tol}")
    print(f"Máximo de iteraciones: {max_iter}")
    print("\nIteraciones:")
    print("-" * 70)
    # Encabezado de la tabla con explicación de cada columna
    print("{:<4} {:<12} {:<12} {:<12} {:<12} {:<12}".format(
        'Iter', 'xₙ', 'f(xₙ)', "f'(xₙ)", 'xₙ₊₁', 'Error'))
    print("-" * 70)

    # Aplicamos el método de Newton-Raphson paso a paso
    x = x0  # Empezamos desde el valor inicial
    for i in range(max_iter):
        fx = f(x)      # Calculamos f(x) en el punto actual
        fpx = f_prime(x)  # Calculamos f'(x) en el punto actual
        x_new = x - fx / fpx  # Aplicamos la fórmula de Newton-Raphson
        error = abs(x_new - x)  # Medimos qué tanto cambió

        # Mostramos los resultados de esta iteración
        print(f"{i+1:<4} {x:<12.6f} {fx:<12.6f} {fpx:<12.6f} {x_new:<12.6f} {error:<12.2e}")

        # Verificamos si ya encontramos una solución suficientemente precisa
        if error < tol:
            break

        x = x_new  # Preparamos para la siguiente iteración

    # Mostramos el resumen final
    print("-" * 70)
    print(f"\nRaíz encontrada: x = {x_new:.8f}")
    print(f"f({x_new:.8f}) = {f(x_new):.2e}")
    print(f"Iteraciones realizadas: {i+1}")


# ===== PUNTO DE INICIO DEL PROGRAMA =====
if __name__ == "__main__":
    # Esta sección se ejecuta cuando el archivo se corre directamente
    # (no cuando se importa como parte de otro programa)
    
    # Comentario sobre las dependencias necesarias
    # Para que este programa funcione, necesitas instalar:
    # pip install numpy matplotlib sympy

    print("Método de Newton-Raphson")
    print("=" * 30)

    # Primero ejecuta el ejemplo simple para mostrar cómo funciona el método
    ejemplo_newton_raphson()

    print("\n" + "=" * 50)
    print("Iniciando interfaz gráfica...")

    # Después inicia la interfaz gráfica completa para uso interactivo
    app = NewtonRaphsonCalculator()
    app.run()