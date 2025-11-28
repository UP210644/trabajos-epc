import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Callable, Optional

class RungeKuttaSolver:
    """
    Solver profesional para EDOs con RK4.
    Muestra pasos intermedios (k1-k4) y genera gráficos.
    """
    def __init__(self, f: Callable[[float, float], float], label: str = "y(x)"):
        self.f = f
        self.label = label
        self.results = None

    def solve(self, x0: float, y0: float, h: float, x_end: float, 
              exact_func: Optional[Callable[[float], float]] = None) -> pd.DataFrame:
        
        # Calcular número de pasos
        try:
            steps = int(np.ceil(abs(x_end - x0) / h))
        except ZeroDivisionError:
            print("Error: El paso h no puede ser 0.")
            return pd.DataFrame()

        # Inicialización de Arrays para x e y
        x_values = np.zeros(steps + 1)
        y_values = np.zeros(steps + 1)
        x_values[0] = x0
        y_values[0] = y0
        
        # Listas para almacenar las pendientes intermedias
        # Se llenarán paso a paso
        k1_list = []
        k2_list = []
        k3_list = []
        k4_list = []
        
        print(f"\nProcesando... (x0={x0}, y0={y0}, h={h}, pasos={steps})")
        
        for i in range(steps):
            xi = x_values[i]
            yi = y_values[i]
            
            try:
                # --- PASO 1: Calcular pendientes ---
                k1 = self.f(xi, yi)
                k2 = self.f(xi + 0.5 * h, yi + 0.5 * h * k1)
                k3 = self.f(xi + 0.5 * h, yi + 0.5 * h * k2)
                k4 = self.f(xi + h, yi + h * k3)
                
                # Guardamos las k para verlas en la tabla
                k1_list.append(k1)
                k2_list.append(k2)
                k3_list.append(k3)
                k4_list.append(k4)
                
                # --- PASO 2: Promedio ponderado y avance ---
                y_next = yi + (h / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
                
                x_values[i+1] = xi + h
                y_values[i+1] = y_next
                
            except Exception as e:
                print(f"Error matemático en el paso {i}: {e}")
                break

        # Rellenamos el último valor de las K con NaN (Not a Number)
        # porque en el último punto ya no calculamos pendientes siguientes.
        k1_list.append(None)
        k2_list.append(None)
        k3_list.append(None)
        k4_list.append(None)

        # --- CONSTRUCCIÓN DE LA TABLA COMPLETA ---
        data = {
            'x': x_values,
            'y_RK4': y_values,
            'k1': k1_list,
            'k2': k2_list,
            'k3': k3_list,
            'k4': k4_list
        }
        
        # Calcular errores si hay solución exacta
        if exact_func:
            try:
                y_exact = exact_func(x_values)
                data['y_Exacta'] = y_exact
                data['Error Abs'] = np.abs(y_exact - y_values)
                # Cálculo seguro del error relativo
                with np.errstate(divide='ignore', invalid='ignore'):
                    data['Err Rel(%)'] = np.abs((y_exact - y_values) / y_exact) * 100
            except Exception as e:
                print(f"No se pudo calcular la solución exacta: {e}")
            
        self.results = pd.DataFrame(data)
        
        # Reordenar columnas para que k1-k4 salgan antes que los errores (estética)
        cols = ['x', 'y_RK4', 'k1', 'k2', 'k3', 'k4']
        if 'y_Exacta' in data:
            cols += ['y_Exacta', 'Error Abs', 'Err Rel(%)']
        self.results = self.results[cols]
        
        return self.results

    def plot(self):
        if self.results is None or self.results.empty:
            print("No hay resultados para graficar.")
            return

        plt.figure(figsize=(10, 6))
        plt.plot(self.results['x'], self.results['y_RK4'], 'o--', label='Aproximación RK4', color='crimson')
        
        if 'y_Exacta' in self.results.columns:
            plt.plot(self.results['x'], self.results['y_Exacta'], 'b-', label='Solución Exacta', alpha=0.6, linewidth=2)
            plt.fill_between(self.results['x'], self.results['y_RK4'], self.results['y_Exacta'], color='gray', alpha=0.1)

        plt.title(f"Método RK4: {self.label}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        plt.show()

# --- FUNCIONES DE INTERFAZ DE USUARIO ---

def parse_math_function(func_str):
    """Convierte texto a función matemática segura."""
    safe_dict = {
        "x": 0, "y": 0,
        "sin": np.sin, "cos": np.cos, "tan": np.tan, "exp": np.exp, 
        "sqrt": np.sqrt, "log": np.log, "pi": np.pi, "e": np.e, 
        "abs": np.abs, "np": np
    }
    
    def func(x, y=None):
        local_scope = safe_dict.copy()
        local_scope['x'] = x
        if y is not None: local_scope['y'] = y
        return eval(func_str, {"__builtins__": None}, local_scope)
    
    return func

def get_user_input():
    print("\n" + "="*50)
    print("  SOLUCIONADOR RK4 PROFESIONAL (Con detalle de pasos)")
    print("="*50)
    print("Sintaxis: Potencias con '**', Raíz con 'sqrt()', etc.")
    print("-" * 50)

    # 1. Entrada de Ecuación
    while True:
        eq_str = input("\nIntroduce dy/dx = f(x,y): ")
        try:
            test_f = parse_math_function(eq_str)
            test_f(1.0, 1.0) 
            user_f = test_f
            break
        except Exception as e:
            print(f"Error de sintaxis: {e}")

    # 2. Parámetros
    try:
        x0 = float(input("x0 inicial: "))
        y0 = float(input("y0 inicial: "))
        h = float(input("Tamaño del paso (h): "))
        x_end = float(input("x final: "))
    except ValueError:
        print("\n¡Error! Introduce solo números válidos.")
        return

    # 3. Solución Exacta (Opcional)
    exact_f = None
    has_exact = input("\n¿Conoces la solución exacta para comparar? (s/n): ").lower().strip()
    if has_exact == 's':
        while True:
            exact_str = input("Introduce y(x) = : ")
            try:
                test_exact = parse_math_function(exact_str)
                test_exact(1.0)
                exact_f = test_exact
                break
            except Exception as e:
                print(f"Error en solución exacta: {e}")

    # --- EJECUCIÓN ---
    solver = RungeKuttaSolver(f=user_f, label=f"dy/dx = {eq_str}")
    df = solver.solve(x0, y0, h, x_end, exact_func=exact_f)
    
    print("\n" + "="*20 + " RESULTADOS DETALLADOS " + "="*20)
    # Configuración para que Pandas muestre bien los decimales
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.float_format', lambda x: '%.6f' % x if pd.notnull(x) else '   ---   ')
    
    print(df)
    
    print("\nGenerando gráfico...")
    solver.plot()

if __name__ == "__main__":
    get_user_input()