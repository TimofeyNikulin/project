import sqlite3


db = sqlite3.connect('db.db')
sql = db.cursor()


def add_employee(name_surname_patronymic: str, phone: str, email: str, salary: int) -> None:
    sql.execute("""INSERT INTO employee VALUES(?, ?, ?, ?, ?)""",
                (name_surname_patronymic, phone, email, salary))
    db.commit()


def update_employee(id, name_surname_patronymic: str, phone: str, email: str, salary: int) -> None:
    sql.execute("""UPDATE employee SET name_surname_patronymic=?, phone=?, email=?, salary=? WHERE id=?""",
                (name_surname_patronymic, phone, email, salary, id))
    db.commit()


def delete_employee(id) -> None:
    sql.execute("""DELETE FROM employee WHERE id=?""", (id))
    db.commit()


def search_employee(name_surname_patronymic: str) -> list:
    return sql.execute("""SELECT * FROM WHERE name_surname_patronymic=?""", (name_surname_patronymic)).fetchall()
