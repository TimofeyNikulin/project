import db                   # Файл с финкциями для взаимодействия с БД
import settings             # Файл с настройками приложения
from interface import App   # Класс с приложением
import tkinter as tk        # Библиотека для создания GUI


# Инициализация приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
