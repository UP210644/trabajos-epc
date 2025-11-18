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