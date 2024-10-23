import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sympy import symbols, Eq, solve, sympify
win =tk.Tk()

win.title("Máy tính bản")
#create tab1
tabControl = ttk.Notebook(win)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text= 'Tính toán')
tabControl.pack(expand= 1, fill= 'both')

number_label = tk.Label(tab1,text="Bảng nhập số")
number_label.grid(column= 0, row= 0)

number1 = tk.StringVar()
number_enter1 = tk.Entry(tab1, width = 30, textvariable= number1)
number_enter1.grid(column= 0, row = 1)

number2 = tk.StringVar()
number_enter2 = tk.Entry(tab1,width = 30, textvariable= number2)
number_enter2.grid(column= 0, row = 2)

result = tk.StringVar()
result_label = tk.Label(tab1, text= "Bảng kết quả")
result_label.grid(column= 0, row = 3)

result_entry = tk.Entry(tab1,width= 30, textvariable= result)
result_entry.grid(column= 0, row= 4)
result_entry.configure(state='disabled')

#Plus
def plus_function():
    try:
        a = float(number1.get())
        b = float(number2.get())
        x = a + b
        result.set(x)
    except ValueError:
        messagebox.showerror("Sai dữ liệu","Bạn đã nhập sai dữ liệu, xin nhập lại dữ liệu đúng")


plus_button = tk.Button(tab1,width=20, text = "+", command= plus_function)
plus_button.grid(column= 1, row = 1)

#Minus
def minus_function():
    try:
        a = float(number1.get())
        b = float(number2.get())
        x = a - b
        result.set(x)
    except ValueError:
        messagebox.showerror("Sai dữ liệu","Bạn đã nhập sai dữ liệu, xin nhập lại dữ liệu đúng")


plus_button = tk.Button(tab1,width=20, text = "-", command= minus_function)
plus_button.grid(column= 2, row = 1)


#Multiple
def multiple_function():
    try:
        a = float(number1.get())
        b = float(number2.get())
        x = a * b
        result.set(x)
    except ValueError:
        messagebox.showerror("Sai dữ liệu","Bạn đã nhập sai dữ liệu, xin nhập lại dữ liệu đúng")


plus_button = tk.Button(tab1,width=20, text = "*", command= multiple_function)
plus_button.grid(column= 1, row = 2)


#Divide
def divide_function():
    try:
        a = float(number1.get())
        b = float(number2.get())
        x = a / b
        result.set(x)
    except ValueError:
        messagebox.showerror("Sai dữ liệu","Bạn đã nhập sai dữ liệu, xin nhập lại dữ liệu đúng")


plus_button = tk.Button(tab1,width=20, text = "/", command= divide_function)
plus_button.grid(column= 2, row = 2)

#Reset 
def reset_function():
    number1.set("")
    number2.set("")
    result.set("")

Reset_button = tk.Button(tab1,width= 20, text= "CE",command= reset_function)
Reset_button.grid(column= 1, row =3)

#Delete
def delete():
    current_widget =tab1.focus_get()
    if isinstance(current_widget, tk.Entry):
        cursor_position = current_widget.index(tk.INSERT)
        if cursor_position > 0:
            current_widget.delete(cursor_position - 1, cursor_position)

delete_button = tk.Button(tab1, width= 20, text= "Delete", command=delete)
delete_button.grid(column= 2, row = 3)

#Create tab2
tab2 =ttk.Frame(tabControl)
tabControl.add(tab2, text = "Giải phương trình")

equation_label = tk.Label(tab2, text = "Nhập phương trình").grid(column= 0, row =0)

equaltion_Var = tk.StringVar()
equaltion_entry = ttk.Entry(tab2, width= 24, textvariable= equaltion_Var)
equaltion_entry.grid(column= 0, row = 1)

solution1 = tk.StringVar()
solution2 = tk.StringVar()

solution1_entry = tk.Entry(tab2, width=24, textvariable=solution1, state='disabled')
solution1_entry.grid(column=0, row=2)

solution2_entry = tk.Entry(tab2, width=24, textvariable=solution2, state='disabled')
solution2_entry.grid(column=0, row=3)

def _solve():
    equation_str = equaltion_Var.get().replace(" ", "")
    

    if "=" not in equation_str:
        messagebox.showerror("Lỗi", "Vui lòng nhập thêm dấu '='.")
        return
    

    left_side, right_side = equation_str.split("=")
    

    equation_str = left_side + "-(" + right_side + ")"
    
    x = symbols('x')
    try:
        formatted_eq = equation_str.replace("^", "**")
        formatted_eq = formatted_eq.replace("x", "*x").replace("**x", "x")
        
        equation = sympify(formatted_eq)
        eq = Eq(equation, 0)
        
        solutions = solve(eq, x)
        
        if not solutions:
            solution1.set("Vô nghiệm")
            solution2.set("N/A")
        elif isinstance(solutions, list) and len(solutions) >= 1:
            solution1.set(str(solutions[0]))
            solution2.set(str(solutions[1]) if len(solutions) > 1 else "N/A")
        else:
            solution1.set("Vô số nghiệm")
            solution2.set("N/A")
    
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")

solve_button = tk.Button(tab2, width=24, text="Giải", command=_solve)
solve_button.grid(column=1, row=1)



number_enter1.focus()


win.mainloop()