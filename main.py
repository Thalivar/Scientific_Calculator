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
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(round(result, 6)))
    except Exception as e:
        messagebox.showerror("Calculation Error", f"Invalid input:\n{e}")

# === Button Logic ===

def press(key):
    entry.insert(tk.END, key)
    
def clear():
    entry.delete(0, tk.END)

# === GUI Setup ===

root = tk.Tk()
root.title("Myriea's Calculator")
root.resizable(False, False)

entry = tk.Entry(root, font=("Arial", 16), width=25, borderwidth=3, relief="ridge", justify='right')
entry.grid(row = 0, column = 0, columnspan = 5, padx = 10, pady = 10)

# === Button Layout ===

buttons = [
    ['7', '8', '9', '/', 'sqrt'],
    ['4', '5', '6', '*', 'log'],
    ['1', '2', '3', '-', 'log10'],
    ['0', '.', '(', ')', '+'],
    ['C', 'pi', 'e', 'factorial', '='],
    ['sin', 'cos', 'tan', 'pow', 'abs']
]

for i, row in enumerate(buttons):
    for j, text in enumerate(row):
        if text == '=':
            action = evaluate_expression
        elif text == 'C':
            action = clear
        else:
            action = lambda k = text: press(k)
        tk.Button(root, text=text, width=6, height=2, font=("Arial", 14), command=action).grid(row=i+1, column=j)

root.mainloop()