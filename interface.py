from settings import *
import tkinter as tk
import tkinter.ttk as ttk
import db


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(TITLE)
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.resizable(False, False)
        self.create_interface()

    def create_interface(self):
        self.employee_frame = ttk.Frame(
            self.root, width=WIDTH_OF_TABLE, height=HEIGHT_OF_TABLE)
        self.employee_frame.pack(padx=15, pady=15, fill="both", expand="yes")

        self.tree = ttk.Treeview(
            self.employee_frame, columns=(
                "ID", "ФИО", "Телефон", "Email", "Зарплата")
        )
        scroll = ttk.Scrollbar(self.root, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)
        size = (WIDTH_OF_TABLE - 45) // 4
        self.tree.column("ID", width=45)
        self.tree.column("ФИО", width=size)
        self.tree.column("Телефон", width=size)
        self.tree.column("Email", width=size)
        self.tree.column("Зарплата", width=size)
        self.tree.heading("#1", text="ID")
        self.tree.heading("#2", text="ФИО")
        self.tree.heading("#3", text="Телефон")
        self.tree.heading("#4", text="Email")
        self.tree.heading("#5", text="Зарплата")
        self.tree.pack(fill="both", expand="yes")

        self.tree.bind('<<TreeviewSelect>>', self.paste_data_on_entries)

        self.update_data_on_table()

        self.form_frame = ttk.Frame(self.root)
        self.form_frame.pack(padx=15, pady=15, fill="both", expand="yes")

        self.label_name = ttk.Label(self.form_frame, text='ФИО: ')
        self.entry_name = ttk.Entry(self.form_frame)
        self.label_name.grid(column=0, row=0, padx=15, pady=5)
        self.entry_name.grid(column=1, row=0, padx=15, pady=5)

        self.label_phone = ttk.Label(self.form_frame, text='Телефон: ')
        self.entry_phone = ttk.Entry(self.form_frame)
        self.label_phone.grid(column=0, row=1, padx=15, pady=5)
        self.entry_phone.grid(column=1, row=1, padx=15, pady=5)

        self.label_email = ttk.Label(self.form_frame, text='Email: ')
        self.entry_email = ttk.Entry(self.form_frame)
        self.label_email.grid(column=0, row=2, padx=15, pady=5)
        self.entry_email.grid(column=1, row=2, padx=15, pady=5)

        self.label_salary = ttk.Label(
            self.form_frame, text='Зарплата (руб): ')
        self.entry_salary = ttk.Entry(self.form_frame)
        self.label_salary.grid(column=0, row=3, padx=15, pady=5)
        self.entry_salary.grid(column=1, row=3, padx=15, pady=5)

        self.add_new_employee_btn = ttk.Button(
            self.form_frame, command=self.add_new_employee, text="Добавить")
        self.add_new_employee_btn.grid(column=0, row=4)
        self.add_new_employee_btn = ttk.Button(
            self.form_frame, command=self.update_employee, text="Изменить")
        self.add_new_employee_btn.grid(column=1, row=4)

        self.delete_btn = ttk.Button(
            self.form_frame, text="Удалить сотрудника", command=self.delete_btn_command)
        self.delete_btn.grid(column=2, row=0, columnspan=2)

        self.search_entry = ttk.Entry(self.form_frame, width=35)
        self.search_btn = ttk.Button(self.form_frame, text='Поиск сотрудников',
                                     command=lambda: self.search_employees(self.search_entry.get()), width=35)
        self.search_entry.grid(column=2, row=1, columnspan=2)
        self.search_btn.grid(column=2, columnspan=2, row=2)

    def update_employee(self):
        db.update_employee(
            self.tree.set(self.tree.selection()[0], '#1'),
            self.entry_name.get(),
            self.entry_phone.get(),
            self.entry_email.get(),
            float(self.entry_salary.get())
        )
        self.update_data_on_table()

    def add_new_employee(self) -> None:
        db.add_employee(
            self.entry_name.get(),
            self.entry_phone.get(),
            self.entry_email.get(),
            float(self.entry_salary.get()),
        )
        self.update_data_on_table()

    def delete_btn_command(self) -> None:
        db.delete_employee(
            self.tree.set(self.tree.selection()[0], '#1'))
        self.update_data_on_table()

    def update_data_on_table(self, data=None) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        if data == None:
            for employee in db.select_all_employees():
                self.tree.insert("", "end", values=employee)
        else:
            for employee in data:
                self.tree.insert("", "end", values=employee)

    def clear_entries(self) -> None:
        self.entry_name.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_salary.delete(0, tk.END)

    def paste_data_on_entries(self, event) -> None:
        self.clear_entries()
        selected_item = self.tree.selection()
        if selected_item:
            employee = self.tree.item(selected_item)["values"]
            self.entry_name.insert(0, employee[1])
            self.entry_phone.insert(0, employee[2])
            self.entry_email.insert(0, employee[3])
            self.entry_salary.insert(0, employee[4])

    def search_employees(self, name) -> None:
        employees = db.search_employee(name)
        self.search_entry.delete(0, tk.END)
        if name == '':
            employees = None
        self.update_data_on_table(employees)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
