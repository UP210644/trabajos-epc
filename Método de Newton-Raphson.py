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