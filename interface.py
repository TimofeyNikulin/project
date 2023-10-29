from settings import *              # Файл с настройками приложения
import tkinter as tk                # Библиотека для создания GUI
import tkinter.ttk as ttk           # Библиотека для создания GUI
import tkinter.messagebox as msg    # Библиотека для отображения диалоговых окон
import db                           # Файл с финкциями для взаимодействия с БД


# Класс с приложением
class App:
    def __init__(self, root: tk.Tk) -> None:  # Инициализация окна
        self.root = root
        self.root.title(TITLE)
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.resizable(False, False)
        self.create_interface()  # Создание интерфейса

    # Метод создания интерфейса
    def create_interface(self):
        self.employee_frame = ttk.Frame(
            self.root, width=WIDTH_OF_TABLE, height=HEIGHT_OF_TABLE)
        self.employee_frame.pack(padx=15, pady=15, fill="both", expand="yes")

        # Создание таблицы
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

        # Привязка события выделения строки
        self.tree.bind('<<TreeviewSelect>>', self.paste_data_on_entries)

        self.update_data_on_table()  # Обновление таблицы при запуске программы

        # Создание блока интерактианости
        self.form_frame = ttk.Frame(self.root)
        self.form_frame.pack(padx=15, pady=15, fill="both", expand="yes")

        # Форма ввода ФИО
        self.label_name = ttk.Label(self.form_frame, text='ФИО: ')
        self.entry_name = ttk.Entry(self.form_frame)
        self.label_name.grid(column=0, row=0, padx=15, pady=5)
        self.entry_name.grid(column=1, row=0, padx=15, pady=5)

        # Форма ввода номера телефона
        self.label_phone = ttk.Label(self.form_frame, text='Телефон: ')
        self.entry_phone = ttk.Entry(self.form_frame)
        self.label_phone.grid(column=0, row=1, padx=15, pady=5)
        self.entry_phone.grid(column=1, row=1, padx=15, pady=5)

        # Форма ввода email
        self.label_email = ttk.Label(self.form_frame, text='Email: ')
        self.entry_email = ttk.Entry(self.form_frame)
        self.label_email.grid(column=0, row=2, padx=15, pady=5)
        self.entry_email.grid(column=1, row=2, padx=15, pady=5)

        # Форма ввода величины зарплаты
        self.label_salary = ttk.Label(
            self.form_frame, text='Зарплата (руб): ')
        self.entry_salary = ttk.Entry(self.form_frame)
        self.label_salary.grid(column=0, row=3, padx=15, pady=5)
        self.entry_salary.grid(column=1, row=3, padx=15, pady=5)

        # Кнопка добавление нового сотрудника
        self.add_new_employee_btn = ttk.Button(
            self.form_frame, command=self.add_new_employee, text="Добавить")
        self.add_new_employee_btn.grid(column=0, row=4)

        # Кнопка изменение данных выбранного сотрудника
        self.update_employee_btn = ttk.Button(
            self.form_frame, command=self.update_employee, text="Изменить")
        self.update_employee_btn.grid(column=1, row=4)

        # Кнопка удаления выбранного сотрудника
        self.delete_btn = ttk.Button(
            self.form_frame, text="Удалить сотрудника", command=self.delete_btn_command)
        self.delete_btn.grid(column=2, row=0, columnspan=2)

        # Форма поиска сотрудника по ФИО
        self.search_entry = ttk.Entry(self.form_frame, width=35)
        self.search_btn = ttk.Button(self.form_frame, text='Поиск сотрудников',
                                     command=lambda: self.search_employees(self.search_entry.get()), width=35)
        self.search_entry.grid(column=2, row=1, columnspan=2)
        self.search_btn.grid(column=2, columnspan=2, row=2)

    # Оюновление данных сотрудника
    def update_employee(self):
        try:
            # Обновление данных сотрудника в БД
            if self.entry_name.get() != '' and self.entry_phone.get() != '' and self.entry_email.get() != '':  # Проверка заполненности полей
                db.update_employee(
                    self.tree.set(self.tree.selection()[0], '#1'),
                    self.entry_name.get(),
                    self.entry_phone.get(),
                    self.entry_email.get(),
                    float(self.entry_salary.get())
                )
                self.update_data_on_table()
            else:
                msg.showerror("Ошибка", "Заполните все поля")
        except IndexError:  # Проверка на наличие выбранного сотрудника
            pass

    # Добавление нового сотрудника
    def add_new_employee(self) -> None:
        try:
            if self.entry_name.get() != '' and self.entry_phone.get() != '' and self.entry_email.get() != '':  # Проверка на заполненность полей
                # Добавление нового сотрудника в БД
                db.add_employee(
                    self.entry_name.get(),
                    self.entry_phone.get(),
                    self.entry_email.get(),
                    float(self.entry_salary.get()),
                )
                self.update_data_on_table()
            else:
                msg.showerror("Ошибка", "Заполните все поля")
        except ValueError:  # Проверка на корректность введенных данных
            msg.showerror(
                "Ошибка", "Проверьте корректность заполнения данных")

    # Удаление сотрудника
    def delete_btn_command(self) -> None:
        try:
            # Удаление сотрудника из БД
            db.delete_employee(
                self.tree.set(self.tree.selection()[0], '#1'))
            self.update_data_on_table()
            self.clear_entries()
        except IndexError:  # Проверка на наличие выбранного сотрудника
            pass

    # Обновление данных в таблице
    def update_data_on_table(self, data=None) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        if data == None:  # Проверка на наличие передаемых данных
            for employee in db.select_all_employees():
                self.tree.insert("", "end", values=employee)
        else:
            for employee in data:
                self.tree.insert("", "end", values=employee)

    # Очищение полей ввода
    def clear_entries(self) -> None:
        self.entry_name.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_salary.delete(0, tk.END)

    # Постановка данных в поля ввода
    def paste_data_on_entries(self, event) -> None:
        self.clear_entries()
        selected_item = self.tree.selection()
        if selected_item:
            employee = self.tree.item(selected_item)["values"]
            self.entry_name.insert(0, employee[1])
            self.entry_phone.insert(0, employee[2])
            self.entry_email.insert(0, employee[3])
            self.entry_salary.insert(0, employee[4])

    # Нахождение сотрудника
    def search_employees(self, name) -> None:
        employees = db.search_employee(name)
        self.search_entry.delete(0, tk.END)
        if name == '':  # Проверка на заполненность поля ввода для поиска
            employees = None
        if employees == []:  # Проверка на наличие сотрудников с таким ФИО
            msg.showinfo('Отсутствие', 'Такого сотрудника нет')
            employees = None
        self.update_data_on_table(employees)
