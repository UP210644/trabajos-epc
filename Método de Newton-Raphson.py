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