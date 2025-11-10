import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

class QRCodeGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Generador de Códigos QR")
        self.root.geometry("500x600")
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        