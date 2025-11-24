import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from sympy import symbols, diff, lambdify
import tkinter as tk
from tkinter import ttk, messagebox

class NewtonRaphsonCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Método de Newton-Raphson")
        self.root.geometry("600x700")
        # Variable simbólica
        self.x = symbols('x')
        self.setup_ui()

    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título
        title_label = ttk.Label(main_frame, text="Método de Newton-Raphson",
                                font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Descripción
        desc_text = """El método de Newton-Raphson es un algoritmo iterativo para encontrar 
las raíces de una función real. Fórmula: xₙ₊₁ = xₙ - f(xₙ)/f'(xₙ)"""
        desc_label = ttk.Label(main_frame, text=desc_text, justify=tk.CENTER)
        desc_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        # Campo para la función
        ttk.Label(main_frame, text="Función f(x):", font=("Arial", 11, "bold")).grid(
            row=2, column=0, sticky=tk.W, pady=5)

        func_frame = ttk.Frame(main_frame)
        func_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(func_frame, text="f(x) =").grid(row=0, column=0, padx=(0, 10))
        self.func_entry = ttk.Entry(func_frame, width=40)
        self.func_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.func_entry.insert(0, "x**3 - 2*x - 5")

        # Ejemplos de funciones
        examples = [
            "Ejemplos: x**2 - 4, exp(x) - 2, cos(x) - x, x**3 - 2*x - 5",
            "Usar: exp() para eˣ, log() para ln(x), sin(), cos(), tan()"
        ]

        for i, example in enumerate(examples):
            example_label = ttk.Label(main_frame, text=example,
                                      font=("Arial", 9), foreground="gray")
            example_label.grid(row=4 + i, column=0, columnspan=2, sticky=tk.W, pady=2)

        # Parámetros
        params_frame = ttk.LabelFrame(main_frame, text="Parámetros", padding="10")
        params_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Valor inicial
        ttk.Label(params_frame, text="Valor inicial (x₀):").grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.x0_entry = ttk.Entry(params_frame, width=15)
        self.x0_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.x0_entry.insert(0, "2.0")

        # Tolerancia
        ttk.Label(params_frame, text="Tolerancia:").grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.tol_entry = ttk.Entry(params_frame, width=15)
        self.tol_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        self.tol_entry.insert(0, "1e-6")

        # Máximo de iteraciones
        ttk.Label(params_frame, text="Máx iteraciones:").grid(
            row=2, column=0, sticky=tk.W, pady=5)
        self.max_iter_entry = ttk.Entry(params_frame, width=15)
        self.max_iter_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        self.max_iter_entry.insert(0, "100")

        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)

        calc_btn = ttk.Button(button_frame, text="Calcular Raíz",
                              command=self.calculate_root)
        calc_btn.grid(row=0, column=0, padx=10)

        graph_btn = ttk.Button(button_frame, text="Graficar Función",
                               command=self.plot_function)
        graph_btn.grid(row=0, column=1, padx=10)

        clear_btn = ttk.Button(button_frame, text="Limpiar",
                               command=self.clear_fields)
        clear_btn.grid(row=0, column=2, padx=10)

        # Área de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        results_frame.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        # Text widget para resultados
        self.results_text = tk.Text(results_frame, height=12, width=70)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical",
                                  command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)

        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(8, weight=1)
        func_frame.columnconfigure(1, weight=1)
        params_frame.columnconfigure(1, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

    def parse_function(self, func_str):
        """Convierte string de función a función evaluable"""
        try:
            # Reemplazar notación de potencia
            func_str = func_str.replace('^', '**')
            # Crear expresión simbólica
            expr = sp.sympify(func_str)
            # Crear funciones numéricas (soporta numpy)
            f = lambdify(self.x, expr, modules=['numpy'])
            f_prime = lambdify(self.x, diff(expr, self.x), modules=['numpy'])
            return f, f_prime, expr
        except Exception as e:
            raise ValueError(f"Error en la función: {str(e)}")

    def newton_raphson(self, f, f_prime, x0, tol=1e-6, max_iter=100):
        """Implementa el método de Newton-Raphson"""
        iterations = []
        x = x0

        for i in range(max_iter):
            fx = float(f(x))
            fpx = float(f_prime(x))

            # Evitar división por cero
            if abs(fpx) < 1e-12:
                raise ValueError("Derivada cercana a cero. El método puede no converger.")

            # Calcular siguiente iteración
            x_new = x - fx / fpx
            error = abs(x_new - x)

            iterations.append({
                'iter': i + 1,
                'x': x,
                'fx': fx,
                'fpx': fpx,
                'x_new': x_new,
                'error': error
            })

            # Verificar convergencia
            if error < tol:
                x = x_new
                break

            x = x_new

        return x, iterations

    def calculate_root(self):
        """Calcula la raíz usando Newton-Raphson"""
        try:
            # Obtener parámetros
            func_str = self.func_entry.get()
            x0 = float(self.x0_entry.get())
            tol = float(self.tol_entry.get())
            max_iter = int(self.max_iter_entry.get())

            # Parsear función
            f, f_prime, expr = self.parse_function(func_str)

            # Calcular derivada simbólica para mostrar
            derivada = diff(expr, self.x)

            # Ejecutar método
            raiz, iteraciones = self.newton_raphson(f, f_prime, x0, tol, max_iter)

            # Mostrar resultados
            self.mostrar_resultados(expr, derivada, raiz, iteraciones)

        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {str(e)}")

    def mostrar_resultados(self, expr, derivada, raiz, iteraciones):
        """Muestra los resultados en el área de texto"""
        self.results_text.delete(1.0, tk.END)

        # Información general
        self.results_text.insert(tk.END, "MÉTODO DE NEWTON-RAPHSON\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")

        self.results_text.insert(tk.END, f"Función: f(x) = {expr}\n")
        self.results_text.insert(tk.END, f"Derivada: f'(x) = {derivada}\n\n")

        # Tabla de iteraciones
        self.results_text.insert(tk.END, "ITERACIONES:\n")
        self.results_text.insert(tk.END, "-" * 80 + "\n")
        # Cabecera corregida (evita la secuencia problemática con comillas)
        self.results_text.insert(tk.END,
                                 "{:<6} {:<12} {:<12} {:<12} {:<12} {:<12}\n".format(
                                     'Iter', 'xₙ', 'f(xₙ)', "f'(xₙ)", 'xₙ₊₁', 'Error'))
        self.results_text.insert(tk.END, "-" * 80 + "\n")

        for it in iteraciones:
            self.results_text.insert(tk.END,
                                     f"{it['iter']:<6} {it['x']:<12.6f} {it['fx']:<12.6f} "
                                     f"{it['fpx']:<12.6f} {it['x_new']:<12.6f} {it['error']:<12.2e}\n")

        # Resultado final
        self.results_text.insert(tk.END, "-" * 80 + "\n\n")
        if iteraciones:
            last_fx = iteraciones[-1]['fx']
        else:
            last_fx = float(sp.N(expr.subs(self.x, raiz)))
        self.results_text.insert(tk.END, f"RAÍZ ENCONTRADA: x = {raiz:.8f}\n")
        self.results_text.insert(tk.END, f"f({raiz:.8f}) = {last_fx:.2e}\n")
        self.results_text.insert(tk.END, f"Iteraciones realizadas: {len(iteraciones)}\n")

    def plot_function(self):
        """Grafica la función y el proceso de Newton-Raphson"""
        try:
            func_str = self.func_entry.get()
            x0 = float(self.x0_entry.get())

            f, f_prime, expr = self.parse_function(func_str)

            # Calcular para obtener iteraciones
            raiz, iteraciones = self.newton_raphson(f, f_prime, x0)

            # Crear gráfico
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

            # Gráfico 1: Función y raíz
            x_vals = np.linspace(raiz - 3, raiz + 3, 400)
            # lambdified f maneja arreglos numpy
            y_vals = f(x_vals)

            ax1.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {expr}')
            ax1.axhline(y=0, color='k', linestyle='--', alpha=0.3)
            ax1.axvline(x=raiz, color='r', linestyle='--', alpha=0.7, label=f'Raíz: {raiz:.6f}')
            ax1.plot(raiz, float(f(raiz)), 'ro', markersize=8, label='Raíz encontrada')
            ax1.set_xlabel('x')
            ax1.set_ylabel('f(x)')
            ax1.set_title('Función y Raíz Encontrada')
            ax1.legend()
            ax1.grid(True, alpha=0.3)

            # Gráfico 2: Convergencia del error
            errores = [it['error'] for it in iteraciones]
            iter_nums = [it['iter'] for it in iteraciones]

            if errores:
                ax2.semilogy(iter_nums, errores, 'go-', linewidth=2, markersize=6)
            ax2.set_xlabel('Iteración')
            ax2.set_ylabel('Error (escala log)')
            ax2.set_title('Convergencia del Error')
            ax2.grid(True, alpha=0.3)

            plt.tight_layout()
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"Error al graficar: {str(e)}")

    def clear_fields(self):
        """Limpia todos los campos"""
        self.func_entry.delete(0, tk.END)
        self.func_entry.insert(0, "x**3 - 2*x - 5")
        self.x0_entry.delete(0, tk.END)
        self.x0_entry.insert(0, "2.0")
        self.tol_entry.delete(0, tk.END)
        self.tol_entry.insert(0, "1e-6")
        self.max_iter_entry.delete(0, tk.END)
        self.max_iter_entry.insert(0, "100")
        self.results_text.delete(1.0, tk.END)

    def run(self):
        self.root.mainloop()


# Ejemplos de uso directo (sin interfaz gráfica)
def ejemplo_newton_raphson():
    """Ejemplo básico del método Newton-Raphson"""
    print("EJEMPLO MÉTODO NEWTON-RAPHSON")
    print("=" * 40)

    # Definir función y su derivada
    def f(x):
        return x**3 - 2*x - 5

    def f_prime(x):
        return 3*x**2 - 2

    # Parámetros
    x0 = 2.0
    tol = 1e-6
    max_iter = 100

    print(f"Función: f(x) = x³ - 2x - 5")
    print(f"Derivada: f'(x) = 3x² - 2")
    print(f"Valor inicial: x0 = {x0}")
    print(f"Tolerancia: {tol}")
    print(f"Máximo de iteraciones: {max_iter}")
    print("\nIteraciones:")
    print("-" * 70)
    # Cabecera corregida para evitar comillas internas
    print("{:<4} {:<12} {:<12} {:<12} {:<12} {:<12}".format(
        'Iter', 'xₙ', 'f(xₙ)', "f'(xₙ)", 'xₙ₊₁', 'Error'))
    print("-" * 70)

    x = x0
    for i in range(max_iter):
        fx = f(x)
        fpx = f_prime(x)
        x_new = x - fx / fpx
        error = abs(x_new - x)

        print(f"{i+1:<4} {x:<12.6f} {fx:<12.6f} {fpx:<12.6f} {x_new:<12.6f} {error:<12.2e}")

        if error < tol:
            break

        x = x_new

    print("-" * 70)
    print(f"\nRaíz encontrada: x = {x_new:.8f}")
    print(f"f({x_new:.8f}) = {f(x_new):.2e}")
    print(f"Iteraciones realizadas: {i+1}")


if __name__ == "__main__":
    
    print("Método de Newton-Raphson")
    print("=" * 30)

    # Ejecutar ejemplo básico
    ejemplo_newton_raphson()

    print("\n" + "=" * 50)
    print("Iniciando interfaz gráfica...")

    # Ejecutar interfaz gráfica
    app = NewtonRaphsonCalculator()
    app.run()