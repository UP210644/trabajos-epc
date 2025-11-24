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
        self.setup_ui()
        
        # Variable simbólica
        self.x = symbols('x')
    
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
            example_label.grid(row=4+i, column=0, columnspan=2, sticky=tk.W, pady=2)

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
            # Reemplazar notaciones comunes
            func_str = func_str.replace('^', '**')
            func_str = func_str.replace('e', 'E')  # Evitar confusión con e como variable
            
            # Crear expresión simbólica
            expr = sp.sympify(func_str)
            
            # Crear funciones numéricas
            f = lambdify(self.x, expr, modules=['numpy', 'math'])
            f_prime = lambdify(self.x, diff(expr, self.x), modules=['numpy', 'math'])
            
            return f, f_prime, expr
            
            except Exception as e:
            raise ValueError(f"Error en la función: {str(e)}")
    
    def newton_raphson(self, f, f_prime, x0, tol=1e-6, max_iter=100):
        """Implementa el método de Newton-Raphson"""
        iterations = []
        x = x0
        
        for i in range(max_iter):
            fx = f(x)
            fpx = f_prime(x)
            
            # Evitar división por cero
            if abs(fpx) < 1e-12:
                raise ValueError("Derivada cercana a cero. El método puede no converger.")
            
             # Calcular siguiente iteración
            x_new = x - fx / fpx
            error = abs(x_new - x)
            
            iterations.append({
                'iteracion': i + 1,
                'x': x,
                'f(x)': fx,
                'f\'(x)': fpx,
                'x_new': x_new,
                'error': error
            })
            
            # Verificar convergencia
            if error < tol:
                break

            x = x_new

             return x_new, iterations
    
    def calculate_root(self):
        """Calcula la raíz usando Newton-Raphson"""
        try:
            # Obtener parámetros
            func_str = self.func_entry.get()
            x0 = float(self.x0_entry.get())
            tol = float(self.tol_entry.get())
            max_iter = int(self.max_iter_entry.get())