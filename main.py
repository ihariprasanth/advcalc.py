import tkinter as tk
from tkinter import ttk, messagebox
import math
import re

class AdvancedCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        
        # Variables
        self.expression = ""
        self.result_var = tk.StringVar()
        self.memory = 0
        self.angle_mode = "DEG"  # DEG or RAD
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Result display
        result_frame = ttk.Frame(main_frame)
        result_frame.grid(row=0, column=0, columnspan=5, sticky=(tk.W, tk.E))
        
        self.result_entry = ttk.Entry(
            result_frame, 
            textvariable=self.result_var, 
            font=('Arial', 20), 
            state='readonly',
            justify='right'
        )
        self.result_entry.pack(fill=tk.BOTH, ipady=10)
        
        # Create notebook for different calculator modes
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=5, pady=10, sticky=(tk.W, tk.E))
        
        # Standard calculator tab
        self.standard_frame = ttk.Frame(self.notebook, padding="5")
        self.notebook.add(self.standard_frame, text="Standard")
        
        # Scientific calculator tab
        self.scientific_frame = ttk.Frame(self.notebook, padding="5")
        self.notebook.add(self.scientific_frame, text="Scientific")
        
        # Programmer calculator tab
        self.programmer_frame = ttk.Frame(self.notebook, padding="5")
        self.notebook.add(self.programmer_frame, text="Programmer")
        
        # Build calculator interfaces
        self.build_standard_calculator()
        self.build_scientific_calculator()
        self.build_programmer_calculator()
        
        # Memory and settings frame
        settings_frame = ttk.Frame(main_frame)
        settings_frame.grid(row=2, column=0, columnspan=5, pady=10, sticky=(tk.W, tk.E))
        
        # Memory buttons
        ttk.Button(settings_frame, text="MC", command=self.memory_clear).grid(row=0, column=0, padx=2)
        ttk.Button(settings_frame, text="MR", command=self.memory_recall).grid(row=0, column=1, padx=2)
        ttk.Button(settings_frame, text="M+", command=self.memory_add).grid(row=0, column=2, padx=2)
        ttk.Button(settings_frame, text="M-", command=self.memory_subtract).grid(row=0, column=3, padx=2)
        ttk.Button(settings_frame, text="MS", command=self.memory_store).grid(row=0, column=4, padx=2)
        
        # Angle mode toggle
        self.angle_btn = ttk.Button(settings_frame, text="DEG", command=self.toggle_angle_mode)
        self.angle_btn.grid(row=0, column=5, padx=2)
        
        # History button
        ttk.Button(settings_frame, text="History", command=self.show_history).grid(row=0, column=6, padx=2)
        
        # History
        self.history = []
        
    def build_standard_calculator(self):
        # Standard calculator buttons
        buttons = [
            ('C', 0, 0), ('±', 0, 1), ('%', 0, 2), ('/', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('*', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('⌫', 4, 3)
        ]
        
        for (text, row, col) in buttons:
            if text == '=':
                btn = ttk.Button(self.standard_frame, text=text, command=self.calculate)
                btn.grid(row=row, column=col, sticky=(tk.W, tk.E), ipadx=10, ipady=10, padx=2, pady=2)
            elif text == 'C':
                btn = ttk.Button(self.standard_frame, text=text, command=self.clear)
                btn.grid(row=row, column=col, sticky=(tk.W, tk.E), ipadx=10, ipady=10, padx=2, pady=2)
            elif text == '⌫':
                btn = ttk.Button(self.standard_frame, text=text, command=self.backspace)
                btn.grid(row=row, column=col, sticky=(tk.W, tk.E), ipadx=10, ipady=10, padx=2, pady=2)
            elif text == '±':
                btn = ttk.Button(self.standard_frame, text=text, command=self.negate)
                btn.grid(row=row, column=col, sticky=(tk.W, tk.E), ipadx=10, ipady=10, padx=2, pady=2)
            else:
                btn = ttk.Button(self.standard_frame, text=text, 
                                command=lambda t=text: self.append_expression(t))
                btn.grid(row=row, column=col, sticky=(tk.W, tk.E), ipadx=10, ipady=10, padx=2, pady=2)
                
        # Configure grid weights
        for i in range(5):
            self.standard_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.standard_frame.grid_columnconfigure(i, weight=1)
            
    def build_scientific_calculator(self):
        # Scientific calculator buttons
        buttons = [
            ('π', 0, 0), ('e', 0, 1), ('(', 0, 2), (')', 0, 3), ('C', 0, 4),
            ('sin', 1, 0), ('cos', 1, 1), ('tan', 1, 2), ('^', 1, 3), ('⌫', 1, 4),
            ('asin', 2, 0), ('acos', 2, 1), ('atan', 2, 2), ('√', 2, 3), ('log', 2, 4),
            ('sinh', 3, 0), ('cosh', 3, 1), ('tanh', 3, 2), ('ln', 3, 3), ('!', 3, 4),
            ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('/', 4, 3), ('%', 4, 4),
            ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('*', 5, 3), ('1/x', 5, 4),
            ('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('-', 6, 3), ('±', 6, 4),
            ('0', 7, 0), ('.', 7, 1), ('=', 7, 2), ('+', 7, 3), ('10^x', 7, 4)
        ]
        
        for (text, row, col) in buttons:
            if text == '=':
                btn = ttk.Button(self.scientific_frame, text=text, command=self.calculate)
                btn.grid(row=row, column=col, sticky=(tk.W, tk.E), ipadx=5, ipady=5, padx=2, pady=2)
            elif text == 'C':
                btn = ttk.Button(self.scientific_frame, text=text, command=self.clear)
                btn.grid(row=row, column=col, sticky=(tk.W, tk.E), ipadx=5, ipady=5, padx=2, pady=2)
            elif text == '⌫':
                btn = ttk.Button(self.scientific_frame, text=text, command=self.backspace)
                btn.grid(row=row, column=col, sticky=(tk.W, tk.E), ipadx=5, ipady=5, padx=2, pady=2)
            elif text == '±':
                btn = ttk.Button(self.scientific_frame, text=text, command=self.negate)
                btn.grid(row=row, column=col, sticky=(tk.W, tk.E), ipadx=5, ipady=5, padx=2, pady=2)
            else:
                btn = ttk.Button(self.scientific_frame, text=text, 
                                command=lambda t=text: self.append_expression(t))
                btn.grid(row=row, column=col, sticky=(tk.W, tk.E), ipadx=5, ipady=5, padx=2, pady=2)
                
        # Configure grid weights
        for i in range(8):
            self.scientific_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.scientific_frame.grid_columnconfigure(i, weight=1)
            
    def build_programmer_calculator(self):
        # Programmer calculator will be implemented similarly
        label = ttk.Label(self.programmer_frame, text="Programmer Mode - Coming Soon!")
        label.pack(pady=20)
        
    def append_expression(self, value):
        self.expression += str(value)
        self.result_var.set(self.expression)
        
    def clear(self):
        self.expression = ""
        self.result_var.set("")
        
    def backspace(self):
        self.expression = self.expression[:-1]
        self.result_var.set(self.expression)
        
    def negate(self):
        if self.expression:
            if self.expression[0] == '-':
                self.expression = self.expression[1:]
            else:
                self.expression = '-' + self.expression
            self.result_var.set(self.expression)
            
    def toggle_angle_mode(self):
        if self.angle_mode == "DEG":
            self.angle_mode = "RAD"
            self.angle_btn.config(text="RAD")
        else:
            self.angle_mode = "DEG"
            self.angle_btn.config(text="DEG")
            
    def memory_clear(self):
        self.memory = 0
        
    def memory_recall(self):
        self.append_expression(str(self.memory))
        
    def memory_add(self):
        try:
            result = eval(self.expression)
            self.memory += result
        except:
            messagebox.showerror("Error", "Invalid expression")
            
    def memory_subtract(self):
        try:
            result = eval(self.expression)
            self.memory -= result
        except:
            messagebox.showerror("Error", "Invalid expression")
            
    def memory_store(self):
        try:
            result = eval(self.expression)
            self.memory = result
        except:
            messagebox.showerror("Error", "Invalid expression")
            
    def show_history(self):
        history_text = "\n".join(self.history[-10:]) if self.history else "No history yet"
        messagebox.showinfo("Calculation History", history_text)
        
    def calculate(self):
        try:
            # Replace special constants and functions
            expr = self.expression
            expr = expr.replace('π', str(math.pi))
            expr = expr.replace('e', str(math.e))
            
            # Handle trigonometric functions with angle mode conversion
            if self.angle_mode == "DEG":
                # Convert degrees to radians for trigonometric functions
                trig_patterns = [
                    (r'sin\(([^)]+)\)', lambda x: math.sin(math.radians(x))),
                    (r'cos\(([^)]+)\)', lambda x: math.cos(math.radians(x))),
                    (r'tan\(([^)]+)\)', lambda x: math.tan(math.radians(x))),
                    (r'asin\(([^)]+)\)', lambda x: math.degrees(math.asin(x))),
                    (r'acos\(([^)]+)\)', lambda x: math.degrees(math.acos(x))),
                    (r'atan\(([^)]+)\)', lambda x: math.degrees(math.atan(x))),
                ]
            else:
                # Use radians directly
                trig_patterns = [
                    (r'sin\(([^)]+)\)', lambda x: math.sin(x)),
                    (r'cos\(([^)]+)\)', lambda x: math.cos(x)),
                    (r'tan\(([^)]+)\)', lambda x: math.tan(x)),
                    (r'asin\(([^)]+)\)', lambda x: math.asin(x)),
                    (r'acos\(([^)]+)\)', lambda x: math.acos(x)),
                    (r'atan\(([^)]+)\)', lambda x: math.atan(x)),
                ]
                
            # Apply trigonometric function replacements
            for pattern, func in trig_patterns:
                matches = re.findall(pattern, expr)
                for match in matches:
                    try:
                        value = float(match)
                        result = func(value)
                        expr = expr.replace(f"{pattern.split('(')[0]}({match})", str(result))
                    except:
                        pass
                        
            # Handle other functions
            expr = re.sub(r'√\(([^)]+)\)', lambda m: str(math.sqrt(float(m.group(1)))), expr)
            expr = re.sub(r'ln\(([^)]+)\)', lambda m: str(math.log(float(m.group(1)))), expr)
            expr = re.sub(r'log\(([^)]+)\)', lambda m: str(math.log10(float(m.group(1)))), expr)
            expr = re.sub(r'sinh\(([^)]+)\)', lambda m: str(math.sinh(float(m.group(1)))), expr)
            expr = re.sub(r'cosh\(([^)]+)\)', lambda m: str(math.cosh(float(m.group(1)))), expr)
            expr = re.sub(r'tanh\(([^)]+)\)', lambda m: str(math.tanh(float(m.group(1)))), expr)
            expr = re.sub(r'10\^\(([^)]+)\)', lambda m: str(10 ** float(m.group(1))), expr)
            expr = re.sub(r'1\/\(([^)]+)\)', lambda m: str(1 / float(m.group(1))), expr)
            
            # Handle factorial
            factorial_matches = re.findall(r'(\d+)!', expr)
            for match in factorial_matches:
                try:
                    n = int(match)
                    if n < 0:
                        raise ValueError("Factorial not defined for negative numbers")
                    result = math.factorial(n)
                    expr = expr.replace(f"{match}!", str(result))
                except:
                    pass
                    
            # Evaluate the expression
            result = eval(expr)
            
            # Format the result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    # Limit decimal places for very small numbers
                    if abs(result) < 1e-10:
                        result = 0
                    else:
                        result = round(result, 10)
            
            # Update expression and result
            original_expression = self.expression
            self.expression = str(result)
            self.result_var.set(self.expression)
            
            # Add to history
            self.history.append(f"{original_expression} = {result}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Invalid expression: {str(e)}")
            self.clear()

if __name__ == "__main__":
    root = tk.Tk()
    calculator = AdvancedCalculator(root)
    root.mainloop()