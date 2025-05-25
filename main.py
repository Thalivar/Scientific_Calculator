import math
import tkinter as tk
from tkinter import messagebox

# === Constants ===

display_expr = ""
backend_expr = ""

calculation_history = []
history_index = -1

angle_mode = "deg"
memory_value = 0

# === Math Logic ===

def factorial(x):
    if not x.is_integer() or x < 0:
        raise ValueError("Input must be a non-negative integer.")
    return math.factorial(int(x))

def evaluate_expression():
    global display_expr, backend_expr, calculation_history, history_index

    if not backend_expr.strip():
        return

    try:
        expression = backend_expr if backend_expr else entry.get()

        if not expression.strip():
            return

        safe_env = {
            'sqrt': math.sqrt,
            'sin': lambda x: math.sin(math.radians(x)) if angle_mode == 'deg' else math.sin(x),
            'cos': lambda x: math.cos(math.radians(x)) if angle_mode == 'deg' else math.cos(x),
            'tan': lambda x: math.tan(math.radians(x)) if angle_mode == 'deg' else math.tan(x),
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

    except Exception as e:
        handle_error(e)


def handle_error(e):
    
    if isinstance(e, ValueError):
        messagebox.showerror("Error", f"Math Error: {str(e)}")
    elif isinstance(e, ZeroDivisionError):
        messagebox.showerror("Error", "Math Error: Division by zero")
    else:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# === History Navigation ===

def navigate_history(direction):
    global history_index, calculation_history, display_expr, backend_expr

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

    if not backend_expr or not backend_expr[-1].isdigit():
        messagebox.showerror("Error", "Factorial requires a number")
        return
        
    display_expr += '!'

    i = len(backend_expr) - 1
    while i >= 0 and (backend_expr[i].isdigit() or backend_expr[i] == '.'):
        i -= 1
    number = backend_expr[i+1:]
    backend_expr = backend_expr[:i+1] + f'factorial({number})'
    entry.delete(0, tk.END)
    entry.insert(tk.END, display_expr)

def handle_power():
    global display_expr, backend_expr

    display_expr += '^'
    backend_expr += 'pow('

    entry.delete(0, tk.END)
    entry.insert(tk.END, display_expr)

def press(key):
    global display_expr, backend_expr

    if key == '(' and backend_expr.count('(') <= backend_expr.count(')'):
        messagebox.showarning("Parentheses", "No opening parenthesis to close")
        return

    symbol_map = {
        'π': ('π', 'pi'),
        '√': ('√', 'sqrt('),
        'ln': ('ln', 'log('),
        'log': ('log', 'log10('),
        '|x|': ('|x|', 'abs('),
        'sin': ('sin(', 'sin('),
        'cos': ('cos(', 'cos('),
        'tan': ('tan(', 'tan('),
        'e': ('e', 'e'),  
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

    entry.delete(0, tk.END)
    entry.insert(tk.END, display_expr)
    
def clear():
    global display_expr, backend_expr

    display_expr = ""
    backend_expr = ""

    entry.delete(0, tk.END)

def backspace():
    global display_expr, backend_expr

    if not display_expr:
        return
    
    func_mapping = {
        'sqrt(': 5,
        'log(': 4,
        'log10(': 6,
        'sin(': 4,
        'cos(': 4,
        'tan(': 4,
        'abs(': 4,
        'ln(': 3
    }

    for func, length in func_mapping.items():
        if backend_expr.endswith(func):
            display_expr = display_expr[:-len(func)+1]
            backend_expr = backend_expr[:-length]
            entry.delete(0, tk.END)
            entry.insert(tk.END, display_expr)
            return
        
    display_expr = display_expr[:-1]
    backend_expr = backend_expr[:-1]
    entry.delete(0, tk.END)
    entry.insert(tk.END, display_expr)

def toggle_angle_mode():
    global angle_mode
    
    angle_mode = 'rad' if angle_mode == 'deg' else 'deg'
    mode_btn.config(text=f"Mode: {angle_mode.upper()}")

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

mode_btn = tk.Button(root, text=f"Mode: {angle_mode.upper()}", command=toggle_angle_mode, bg="#5D3FD3")
mode_btn.grid(row=0, column=5, padx=5)

# === Keyboard Event Handling ===

def on_key_press(event):
    key = event.keysym
    char = event.char

    key_mapping = {
        'Up': 'up',
        'Down': 'down',
        'Return': '=',
        'Escape': 'C',
        'plus': '+',
        'minus': '-',
        'asterisk': '*',
        'slash': '/',
        'parenleft': '(',
        'parenright': ')',
        'asciicircum': '^',
        'exclam': '!'
    }
    
    if key in key_mapping:
        if key == 'Up':
            navigate_history('up')
        elif key == 'Down':
            navigate_history('down')
        elif key == '=':
            evaluate_expression()
        elif key == 'C':
            clear()
        else:
            press(key_mapping[key])
    
    if char and (char.isdigit() or char in '+-*/.()^!'):
        press(char)
        return "break"
    
    return None

entry.bind('<KeyPress>', on_key_press)
entry.focus()

root.mainloop()