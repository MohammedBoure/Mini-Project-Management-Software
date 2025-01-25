import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class ConstructionManagerApp:
    def __init__(self, root,name_emloye,costs,costs_emloye):
        self.root = root
        self.root.title("برنامج إدارة تكاليف البناء")
        self.root.geometry("600x650")
        self.root.config(bg="#f7f7f7")

        self.name_emloye = name_emloye
        self.costs = costs
        self.costs_emloye = costs_emloye

        self.main_frame = tk.Frame(self.root, bg="#f7f7f7")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.canvas = tk.Canvas(self.main_frame, bg="#f7f7f7")
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f7f7f7")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.create_interface()

    def create_interface(self):
        employee_frame = self.create_frame(self.scrollable_frame, "إدارة الموظفين", 0)
        
        self.selected_employee = tk.StringVar()
        self.selected_employee.set("اختر موظفًا")
        self.employee_menu = self.create_combobox(employee_frame, "اختر الموظف:", self.selected_employee, 1)
        
        self.daily_salary_var = tk.StringVar()
        self.create_label(employee_frame, "الراتب لليوم (د.ج):", 2)
        self.create_entry(employee_frame, self.daily_salary_var, 3)

        self.create_button(employee_frame, "إضافة الراتب", self.add_daily_salary, 4)
        
        self.employee_salary_listbox = self.create_listbox(employee_frame, 5)

        self.create_label(employee_frame, "إضافة موظف جديد", 6, font=("Helvetica", 14, "bold"))
        self.new_employee_name_var = tk.StringVar()
        self.create_label(employee_frame, "اسم الموظف:", 7)
        self.create_entry(employee_frame, self.new_employee_name_var, 8)

        self.create_button(employee_frame, "إضافة الموظف", self.add_new_employee, 9)

        project_frame = self.create_frame(self.scrollable_frame, "تكاليف المشروع", 1)

        self.project_cost_var = tk.StringVar()
        self.create_label(project_frame, "أدخل التكلفة:", 0)
        self.create_entry(project_frame, self.project_cost_var, 1)

        self.project_comment_var = tk.StringVar()
        self.create_label(project_frame, "تعليق التكلفة:", 2)
        self.create_entry(project_frame, self.project_comment_var, 3)

        self.create_button(project_frame, "إضافة التكلفة", self.add_project_cost, 4)

        self.project_cost_listbox = self.create_listbox(project_frame, 5)

        total_frame = self.create_frame(self.scrollable_frame, "المجموع الكلي", 2)
        self.total_cost_label = tk.Label(total_frame, text="المجموع: 0 د.ج", font=("Helvetica", 14), bg="#ffffff")
        self.total_cost_label.grid(row=1, column=0, padx=10, pady=10)

        close_button = tk.Button(self.root, text="X", font=("Helvetica", 14, "bold"), bg="red", fg="white", command=self.root.quit)
        close_button.place(x=self.root.winfo_width()-40, y=20)

        self.update_employee_menu()
        self.update_project_costs()
        self.update_employee_salaries()
        self.update_total_cost()

    def create_frame(self, parent, title, row):
        frame = tk.Frame(parent, bd=2, relief="ridge", padx=10, pady=10, bg="#ffffff")
        frame.grid(row=row, column=0, padx=10, pady=20, sticky="ew")
        label = tk.Label(frame, text=title, font=("Helvetica", 16, "bold"), bg="#ffffff")
        label.grid(row=0, column=0, pady=10, columnspan=2)
        return frame

    def create_label(self, parent, text, row, font=("Helvetica", 12)):
        label = tk.Label(parent, text=text, font=font, bg="#ffffff")
        label.grid(row=row, column=0, sticky="w", padx=10, pady=5)

    def create_entry(self, parent, text_variable, row):
        entry = tk.Entry(parent, textvariable=text_variable, font=("Helvetica", 12))
        entry.grid(row=row, column=1, sticky="ew", padx=10, pady=5)

    def create_combobox(self, parent, label_text, text_variable, row):
        self.create_label(parent, label_text, row)
        combo = ttk.Combobox(parent, textvariable=text_variable, values=self.name_emloye, state="readonly")
        combo.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        return combo

    def create_button(self, parent, text, command, row):
        button = tk.Button(parent, text=text, font=("Helvetica", 12), command=command, relief="raised", bd=2)
        button.grid(row=row, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

    def create_listbox(self, parent, row):
        listbox = tk.Listbox(parent, height=6, font=("Helvetica", 12), bd=2, relief="sunken")
        listbox.grid(row=row, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        return listbox

    def add_daily_salary(self):
        employee = self.selected_employee.get()
        try:
            daily_salary = float(self.daily_salary_var.get().strip())
        except ValueError:
            messagebox.showerror("خطأ", "الرجاء إدخال راتب صحيح")
            return

        if employee == "اختر موظفًا":
            messagebox.showerror("خطأ", "الرجاء اختيار موظف")
            return

        self.costs_emloye.append((daily_salary, employee))
        add_costs_emloye_data('data.db',daily_salary,employee)
        self.update_employee_salaries()
        self.update_total_cost()
        self.daily_salary_var.set("")

    def add_new_employee(self):
        name = self.new_employee_name_var.get().strip()

        if not name:
            messagebox.showerror("خطأ", "اسم الموظف لا يمكن أن يكون فارغًا")
            return

        if name in self.name_emloye:
            messagebox.showerror("خطأ", "الموظف موجود بالفعل")
            return

        self.name_emloye.append(name)
        add_employee('data.db',name)
        self.update_employee_menu()
        messagebox.showinfo("نجاح", f"تمت إضافة الموظف {name}")
        self.new_employee_name_var.set("")
        self.update_total_cost()

    def add_project_cost(self):
        try:
            cost = float(self.project_cost_var.get().strip())
        except ValueError:
            messagebox.showerror("خطأ", "الرجاء إدخال تكلفة صحيحة")
            return

        comment = self.project_comment_var.get().strip()
        if not comment:
            messagebox.showerror("خطأ", "الرجاء إدخال تعليق للتكلفة")
            return

        self.costs.append((cost, comment))
        add_price_data('data.db',cost,comment)
        self.update_project_costs()
        self.update_total_cost()
        self.project_cost_var.set("")
        self.project_comment_var.set("")

    def update_employee_menu(self):
        self.employee_menu['values'] = self.name_emloye
        if self.selected_employee.get() not in self.name_emloye:
            self.selected_employee.set("اختر موظفًا")

    def update_project_costs(self):
        self.project_cost_listbox.delete(0, tk.END)
        for cost, comment in self.costs:
            self.project_cost_listbox.insert(tk.END, f"{cost} د.ج - {comment}")

    def update_employee_salaries(self):
        self.employee_salary_listbox.delete(0, tk.END)
        for salary, employee in self.costs_emloye:
            self.employee_salary_listbox.insert(tk.END, f"{employee}: {salary} د.ج")

    def update_total_cost(self):
        total = sum(cost for cost, _ in self.costs) + sum(salary for salary, _ in self.costs_emloye)
        self.total_cost_label.config(text=f"المجموع: {total:.2f} د.ج")
        

from fun_db import create_db_and_table,add_employee,fetch_all_data
from fun_db import add_price_data,fetch_all_price_data,add_costs_emloye_data,fetch_all_costs_emloye_data

if __name__ == "__main__":
    name_of_db = 'data.db'
    create_db_and_table(name_of_db)
    
    #->[(1, 'محمد'), (2, 'خالد')]
    try:
        name_emloye = [i[1] for  i in fetch_all_data(name_of_db)] 
    except:name_emloye = []
    
    #->[(1, 1000.0, 'رمل'), (2, 1000.0, 'اسمنت')]
    try:
        costs = [(i[1],i[2]) for i in fetch_all_price_data(name_of_db)] 
    except:costs = []
    
    #->[(1, 1000.0, 'name1'), (2, 1000.0, 'name2')]
    try:
        costs_emloye = [(i[1],i[2]) for i in fetch_all_costs_emloye_data(name_of_db)]
    except:costs_emloye = []
    root = tk.Tk()
    app = ConstructionManagerApp(root,name_emloye,costs,costs_emloye)
    root.mainloop()
