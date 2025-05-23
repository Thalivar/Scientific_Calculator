import math
import tkinter as tk
from tkinter import messagebox

# === Math Logic ===

def factorial(x):
    if not x.is_integer() or x < 0:
        raise ValueError("Input must be a non-negative integer.")
    return math.factorial(int(x))

def evaluate_expression():
    try:
        expression = entry.get()

        safe_env = {
            'sqrt': math.sqrt,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log,
            'log10': math.log10,
            'pi': math.pi,
            'e': math.e,
            'abs': abs,
            'pow': math.pow,
            'factorial': factorial,
        }

        result = eval(expression, {"__builtins__": None}, safe_env)
        entry.delete(0, tl.END)
        entry.insert(tk.END, str(round(result, 6)))
    except Exception as e:
        messagebox.showerror("Calculation Error", f"Invalid input:\n{e}")

    # === Button Logic ===

    def press(key):
        entry.insert(tk.END, key)
    
    def clear()
        entry.delete(0, tk.END)

        