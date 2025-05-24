import math
import tkinter as tk
from tkinter import messagebox

# === Constants ===

display_expr = ""
backend_expr = ""

calculation_history = []
history_index = -1

# === Math Logic ===

def factorial(x):
    if not x.is_integer() or x < 0:
        raise ValueError("Input must be a non-negative integer.")
    return math.factorial(int(x))

def evaluate_expression():
    global display_expr, backend_expr, calculation_history, history_index

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

        calculation_entry = f"{display_expr if display_expr else expression} = {result}"
        calculation_history.append(calculation_entry)
        if len(calculation_history) > 10:
            calculation_history.pop(0)
        
        history_index = -1

        display_expr = ""
        backend_expr = ""

    except ZeroDivisionError:
        messagebox.showerror("Calculation Error", "Division by zero is not allowed.")
    
    except ValueError as e:
        messagebox.showerror("Calculation Error", f"Math error:\n{e}")

    except Exception as e:
        messagebox.showerror("Calculation Error", f"Invalid expression:\n{e}")

# === History Navigation ===

def navigate_history(direction):
    global history_index, calculation_history

    if not calculation_history:
        return
    
    if direction == 'up':
        if history_index < len(calculation_history) - 1:
            history_index += 1
    elif direction == 'down':
        if history_index > -1:
            history_index -= 1
    
    if history_index >= 0:
        calc = calculation_history[-(history_index + 1)]
        entry.delete(0, tk.END)
        entry.insert(tk.END, calc)
        display_expr = calc
        backend_expr = calc
        
    else:
        entry.delete(0, tk.END)
        display_expr = ""
        backend_expr = ""

# === Button Logic ===

def handle_factorial():
    global display_expr, backend_expr

    display_expr += '!'
    if backend_expr and backend_expr[-1].isdigit():
        i = len(backend_expr) - 1
        while i >= 0 and (backend_expr[i].isdigit() or backend_expr[i] == '.'):
            i -= 1
        number = backend_expr[i+1:]
        backend_expr = backend_expr[:i+1] + f'factorial({number})'
    else:
        backend_expr += 'factorial('

def handle_power():
    global display_expr, backend_expr

    display_expr += '^'
    backend_expr += 'pow('

def press(key):
    global display_expr, backend_expr

    history_index = -1

    symbol_map = {
        'π': ('π', 'pi'),
        '√': ('√', 'sqrt('),
        'ln': ('ln', 'log('),
        'log': ('log', 'log10('),
        '!': ('!', 'factorial('),
        '^': ('^', 'pow('),
        '|x|': ('|x|', 'abs('),
    }

    if key == '!':
        handle_factorial()
        return
    elif key == '^':
        handle_power()
        return
    elif key in symbol_map:
        display, backend = symbol_map[key]
        display_expr += display
        backend_expr += backend
    else:
        display_expr += key
        backend_expr += key

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

def backspace():
    global display_expr, backend_expr

    history_index = -1

    if display_expr:
        display_expr = display_expr[:-1]
        backend_expr = backend_expr[:-1]
        
        entry.delete(0, tk.END)
        entry.insert(tk.END, display_expr)

# === GUI Setup ===

root = tk.Tk()
root.title("Myriea's Calculator")
root.resizable(False, False)
root.config(bg="#3B3939")

entry = tk.Entry(root, font=("Arial", 16), width=25, borderwidth=3, relief="ridge", justify='right')
entry.grid(row = 0, column = 0, columnspan = 5, padx = 10, pady = 10)

# === Button Layout ===

buttons = [
    ['√', 'C', '!', '^', '/'],
    ['ln', '7', '8', '9', '*'],
    ['log', '4', '5', '6', '-'],
    ['(', '1', '2', '3', ')'],
    ['π', '0', '.', '=', '+'],
    ['sin', 'cos', 'tan', 'e', '|x|']
]

# === Color Scheme ===

number_color = "#c05ddf"
operator_color = "#76488b"
function_color = "#ad35ad"
special_color = "#c17fca"

for i, row in enumerate(buttons):
    for j, text in enumerate(row):

        if text in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
            color = number_color
        elif text in ['+', '-', '*', '/', '^']:
            color = operator_color
        elif text in ['C', '=', '!']:
            color = special_color
        else:
            color = function_color


        if text == '=':
            action = evaluate_expression
        elif text == 'C':
            action = clear
        else:
            action = lambda k = text: press(k)
        
        btn = tk.Button(root, text=text, width=6, height=2, font=("Arial", 12, "bold"), 
                       command=action, bg=color, relief='raised', borderwidth=1)
        btn.grid(row=i+1, column=j, padx=1, pady=1)

# === Keyboard Event Handling ===

def on_key_press(event):
    key = event.keysym
    char = event.char
    
    # Handle arrow keys for history navigation
    if key == 'Up':
        navigate_history("up")
        return "break"
    elif key == 'Down':
        navigate_history("down")
        return "break"
    elif key == 'Return':
        evaluate_expression()
        return "break"
    elif key == 'BackSpace':
        backspace()
        return "break"
    elif char and (char.isdigit() or char in '+-*/.()'):
        press(char)
        return "break"
    elif char.lower() == 'c':
        clear()
        return "break"

entry.bind('<KeyPress>', on_key_press)
entry.focus()

root.mainloop()