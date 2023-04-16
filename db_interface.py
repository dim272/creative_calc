"""
Класс для общения с базой данных
"""
import sqlite3


class DatabaseInterface:
    """
    В классе реализованы функции чтения и добавления данных в базу
    """

    def __init__(self):
        self.con = sqlite3.connect('cc_demo.db')
        self.init_tables()

    def init_tables(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS user 
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE,
                    password TEXT,
                    name TEXT,
                    about TEXT,
                    added DATETIME
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS handmade 
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    added DATETIME,
                    user_id INTEGER
                    FOREIGN KEY (user_id) REFERENCES user (id) 
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS material 
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    quantity INTEGER,
                    total_quantity INTEGER,
                    price INTEGER,
                    handmade_id INTEGER
                    FOREIGN KEY (handmade_id) REFERENCES handmade (id) 
                )
                """
            )
            self.con.commit()

    def read_user(self):
        pass

    def read_handmade(self):
        pass

    def read_material(self):
        pass

    def write_value(self):
        self.cur.execute(
            """
            INSERT INTO user (email, password, name, about, added) 
            VALUES ('first_user@mail.ru', 'test123', 'Helen', 'Люблю кофе и котиков', '03.04.2023')
            """
        )
        self.con.commit()


if __name__ == '__main__':
    x = DatabaseInterface()
    x.write_value()