import math
import sympy as sp
import tkinter as tk
from tkinter import messagebox

# 预定义函数
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "错误：除数不能为零"
    return x / y

def power(x, y):
    return x ** y

def exp(x):
    return math.exp(x)

def log(x, base=math.e):
    if x <= 0 or base <= 0 or base == 1:
        return "错误：对数输入无效"
    return math.log(x, base)

def sin(x):
    return math.sin(math.radians(x))

def cos(x):
    return math.cos(math.radians(x))

def tan(x):
    if math.cos(math.radians(x)) == 0:
        return "错误：正切函数分母不能为零"
    return math.tan(math.radians(x))

# 反三角函数
def arcsin(x):
    if -1 <= x <= 1:
        return math.degrees(math.asin(x))
    return "错误：反正弦函数输入必须在 -1 到 1 之间"

def arccos(x):
    if -1 <= x <= 1:
        return math.degrees(math.acos(x))
    return "错误：反余弦函数输入必须在 -1 到 1 之间"

def arctan(x):
    return math.degrees(math.atan(x))

# 双曲函数
def sinh(x):
    return math.sinh(x)

def cosh(x):
    return math.cosh(x)

def tanh(x):
    return math.tanh(x)

# 新增余切、正割、余割函数
def cot(x):
    if math.sin(math.radians(x)) == 0:
        return "错误：余切函数分母不能为零"
    return 1 / math.tan(math.radians(x))

def sec(x):
    if math.cos(math.radians(x)) == 0:
        return "错误：正割函数分母不能为零"
    return 1 / math.cos(math.radians(x))

def csc(x):
    if math.sin(math.radians(x)) == 0:
        return "错误：余割函数分母不能为零"
    return 1 / math.sin(math.radians(x))

# 存储用户自定义函数
custom_functions = {}

# 函数英文到中文的映射
function_translation = {
    'sin': '正弦',
    'cos': '余弦',
    'tan': '正切',
    'cot': '余切',
    'sec': '正割',
    'csc': '余割',
    'arcsin': '反正弦',
    'arccos': '反余弦',
    'arctan': '反正切',
    'sinh': '双曲正弦',
    'cosh': '双曲余弦',
    'tanh': '双曲正切',
    'exp': '指数',
    'log': '对数'
}

def calculate():
    expression = entry.get()
    try:
        if expression.lower() == '退出':
            root.destroy()
            return

        # 检查是否为自定义函数定义
        if '(' in expression and '=' in expression:
            func_name, expr_str = expression.split('=', 1)
            func_name = func_name.strip()
            var_str = func_name[func_name.index('(') + 1:func_name.index(')')]
            var = sp.symbols(var_str)
            expr = sp.sympify(expr_str)
            custom_functions[func_name.split('(')[0]] = (var, expr)
            messagebox.showinfo("提示", f"自定义函数 {func_name} 定义成功。")
            return

        if ' ' in expression:
            num1, operator, num2 = expression.split()
            num1 = float(num1)
            num2 = float(num2)

            if operator == '+':
                result = add(num1, num2)
            elif operator == '-':
                result = subtract(num1, num2)
            elif operator == '*':
                result = multiply(num1, num2)
            elif operator == '/':
                result = divide(num1, num2)
            elif operator == '^':
                result = power(num1, num2)
            else:
                result = "错误：不支持的运算符"
        elif '(' in expression and ')' in expression:
            for eng, chi in function_translation.items():
                if chi in expression:
                    expression = expression.replace(chi, eng)
            func, num_str = expression.split('(')
            num = float(num_str.rstrip(')'))
            if func == 'exp':
                result = exp(num)
            elif func == 'log':
                parts = num_str.rstrip(')').split(',')
                if len(parts) == 1:
                    result = log(num)
                elif len(parts) == 2:
                    base = float(parts[1])
                    result = log(num, base)
                else:
                    result = "错误：对数函数输入格式错误"
            elif func == 'sin':
                result = sin(num)
            elif func == 'cos':
                result = cos(num)
            elif func == 'tan':
                result = tan(num)
            elif func == 'arcsin':
                result = arcsin(num)
            elif func == 'arccos':
                result = arccos(num)
            elif func == 'arctan':
                result = arctan(num)
            elif func == 'sinh':
                result = sinh(num)
            elif func == 'cosh':
                result = cosh(num)
            elif func == 'tanh':
                result = tanh(num)
            elif func == 'cot':
                result = cot(num)
            elif func == 'sec':
                result = sec(num)
            elif func == 'csc':
                result = csc(num)
            elif func in custom_functions:
                var, expr = custom_functions[func]
                result = float(expr.subs(var, num))
            else:
                result = "错误：不支持的函数"
        else:
            result = "错误：输入格式错误"

        result_label.config(text=f"结果: {result}")
    except ValueError:
        messagebox.showerror("错误", "输入无效，请输入有效的数字。")
    except sp.SympifyError:
        messagebox.showerror("错误", "表达式解析失败，请检查自定义函数表达式。")

def insert_text(text):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current + text)

# 创建主窗口
root = tk.Tk()
root.title("函数计算器")
root.geometry("500x750")
root.configure(bg="#f0f8ff")  # 设置窗口背景颜色为淡蓝色

# 通用字体设置
font_style = ("Arial", 14)

# 输入框
entry = tk.Entry(root, width=30, font=font_style, bd=3, relief=tk.SOLID, bg="#ffffff", fg="#000000")
entry.pack(pady=20)

# 函数按钮框架
function_frame = tk.Frame(root, bg="#f0f8ff", bd=2, relief=tk.GROOVE)
function_frame.pack(pady=20)

functions = ['sin', 'cos', 'tan', 'cot', 'sec', 'csc', 'arcsin', 'arccos', 'arctan', 'sinh', 'cosh', 'tanh', 'exp', 'log']
row = 0
col = 0
for func in functions:
    button_text = function_translation[func]
    button = tk.Button(function_frame, text=button_text, command=lambda f=func: insert_text(f + '('),
                       font=font_style, bg="#e1f5fe", activebackground="#b3e5fc", bd=2, relief=tk.RAISED, fg="#000000")
    button.grid(row=row, column=col, padx=10, pady=10)
    col += 1
    if col == 3:
        col = 0
        row += 1

# 基础运算按钮框架
basic_op_frame = tk.Frame(root, bg="#f0f8ff", bd=2, relief=tk.GROOVE)
basic_op_frame.pack(pady=20)

basic_operators = ['+', '-', '*', '/', '^']
for i, op in enumerate(basic_operators):
    button = tk.Button(basic_op_frame, text=op, command=lambda o=op: insert_text(' ' + o + ' '),
                       font=font_style, bg="#e1f5fe", activebackground="#b3e5fc", bd=2, relief=tk.RAISED, fg="#000000")
    button.grid(row=0, column=i, padx=10, pady=10)

# 计算按钮
calculate_button = tk.Button(root, text="计算", command=calculate,
                             font=("Arial", 16), bg="#2196f3", activebackground="#1976d2", fg="white", bd=3, relief=tk.RAISED)
calculate_button.pack(pady=30)

# 结果标签
result_label = tk.Label(root, text="结果: ", font=font_style, bg="#f0f8ff", fg="#000000")
result_label.pack(pady=20)

# 运行主循环
root.mainloop()
    