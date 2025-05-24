import math
import tkinter as tk
from tkinter import messagebox

display_expr = ""
backend_expr = ""

# === Math Logic ===

def factorial(x):
    if not x.is_integer() or x < 0:
        raise ValueError("Input must be a non-negative integer.")
    return math.factorial(int(x))

def evaluate_expression():
    global display_expr, backend_expr

    try:
        expression = backend_expr if backend_expr else entry.get()

        if not expression.strip():
            return

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
            'pow': pow,
            'factorial': factorial,
        }

        result = eval(expression, {"__builtins__": None}, safe_env)
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(round(result, 6)))

        display_expr = ""
        backend_expr = ""

    except ZeroDivisionError:
        messagebox.showerror("Calculation Error", "Division by zero is not allowed.")
    
    except ValueError as e:
        messagebox.showerre("Calculation Error", f"Math error:\n{e}")

    except Exception as e:
        messagebox.showerror("Calculation Error", f"Invalid expression:\n{e}")

# === Button Logic ===

def press(key):
    global display_expr, backend_expr

    symbol_map = {
        'π': ('π', 'pi'),
        '√': ('√', 'sqrt('),
        'ln': ('ln', 'log('),
        'log': ('log', 'log10('),
        '!': ('!', 'factorial('),
        '^': ('^', 'pow('),
        '|x|': ('|x|', 'abs('),
    }

    display, backend = symbol_map.get(key, (key, key))
    display_expr += display
    backend_expr += backend

    entry.delete(0, tk.END)
    entry.insert(tk.END, display_expr)
    
def clear():
    global display_expr, backend_expr

    display_expr = ""
    backend_expr = ""

    entry.delete(0, tk.END)

# === GUI Setup ===

root = tk.Tk()
root.title("Myriea's Calculator")
root.resizable(False, False)

entry = tk.Entry(root, font=("Arial", 16), width=25, borderwidth=3, relief="ridge", justify='right')
entry.grid(row = 0, column = 0, columnspan = 5, padx = 10, pady = 10)

# === Button Layout ===

buttons = [
    ['7', '8', '9', '/', '√'],
    ['4', '5', '6', '*', 'ln'],
    ['1', '2', '3', '-', 'log'],
    ['0', '.', '(', ')', '+'],
    ['C', 'π', 'e', '!', '='],
    ['sin', 'cos', 'tan', '^', '|x|']
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