import sqlite3      # Библиотека для работы с БД


db = sqlite3.connect('db.db')
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS Employee (
    ID                      INTEGER PRIMARY KEY,
    name_surname_patronymic TEXT    NOT NULL,
    phone                   TEXT,
    email                   TEXT,
    salary                  REAL    NOT NULL
);""")
db.commit()


def add_employee(name_surname_patronymic: str, phone: str, email: str, salary: int) -> None:
    sql.execute("""INSERT INTO employee (name_surname_patronymic, phone, email, salary) VALUES(?, ?, ?, ?)""",
                (name_surname_patronymic, phone, email, salary))
    db.commit()


def update_employee(id, name_surname_patronymic: str, phone: str, email: str, salary: int) -> None:
    sql.execute("""UPDATE employee SET name_surname_patronymic=?, phone=?, email=?, salary=? WHERE id=?""",
                (name_surname_patronymic, phone, email, salary, id))
    db.commit()


def delete_employee(id) -> None:
    sql.execute("""DELETE FROM employee WHERE id=?""", (id,))
    db.commit()


def search_employee(name_surname_patronymic: str) -> list:
    return sql.execute("""SELECT * FROM employee WHERE name_surname_patronymic=?""", (name_surname_patronymic,)).fetchall()


def select_all_employees() -> list:
    return sql.execute("""SELECT * FROM employee""").fetchall()
