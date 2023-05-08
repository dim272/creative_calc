"""
Класс для общения с базой данных
"""
import sqlite3
from datetime import datetime


class DbConnection:
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
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    name TEXT,
                    about TEXT,
                    date_added DATETIME NOT NULL
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS handmade 
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    date_added DATETIME NOT NULL,
                    is_private INTEGER NOT NULL,
                    price INTEGER,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user (id) 
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS material 
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    total_quantity INTEGER NOT NULL,
                    price INTEGER NOT NULL,
                    handmade_id INTEGER NOT NULL,
                    FOREIGN KEY (handmade_id) REFERENCES handmade (id) 
                )
                """
            )
            self.con.commit()

    def save_user(self, **kwargs):
        with self.con:
            cur = self.con.cursor()
            date_added = datetime.now()
            cur.execute(
                """
                INSERT INTO user (email, password, name, about, date_added)
                VALUES (?, ?, ?, ?, ?)
                """,
                (kwargs.get('email'), kwargs.get('password'), kwargs.get('name'), kwargs.get('about'), date_added)
            )
            self.con.commit()

    def save_handmade(self, **kwargs):
        with self.con:
            cur = self.con.cursor()
            date_added = datetime.now()
            cur.execute(
                """
                INSERT INTO handmade (name, date_added, user_id, is_private)
                VALUES (?, ?, ?, ?)
                """,
                (kwargs.get('name'), date_added, kwargs.get('user_id'), kwargs.get('is_private'))
            )
            self.con.commit()

    def save_materials(self, materials_list):
        with self.con:
            cur = self.con.cursor()
            for materials in materials_list:
                cur.execute(
                    """
                    INSERT INTO material (name, quantity, total_quantity, price, handmade_id)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    materials
                )
            self.con.commit()

    def get_total_handmade_list(self, limit):
        with self.con:
            cur = self.con.cursor()
            cur.execute(
                """
                SELECT * FROM handmade
                ORDER BY id
                LIMIT (?)
                """,
                (limit,)
            )
            handmade_list = cur.fetchall()
        return handmade_list

    def get_user_handmade_list(self, user_id):
        with self.con:
            cur = self.con.cursor()
            cur.execute(
                """
                SELECT * FROM handmade
                WHERE user_id = (?)
                ORDER BY id
                """,
                (user_id,)
            )
            handmade_list = cur.fetchall()
        return handmade_list

    def get_material_list(self, handmade_id):
        with self.con:
            cur = self.con.cursor()
            cur.execute(
                """
                SELECT * FROM material
                WHERE handmade_id = (?)
                ORDER BY id
                """,
                (handmade_id,)
            )
            material_list = cur.fetchall()
        return material_list


if __name__ == '__main__':
    x = DbConnection()
    # x.save_user(
    #     **{
    #         'email': 'test2@test.com',
    #         'password': 'test2_pass',
    #         'name': 'test2_name',
    #         'about': 'test test test'
    #     }
    # )
    # x.save_handmade(
    #     **{
    #         'name': 'Свеча',
    #         'user_id': 1,
    #         'is_private': 0
    #     }
    # )
    # x.save_materials(
    #     [
    #         ('Воск', 100, 500, 349, 1),
    #         ('Фитиль', 1, 20, 149, 1),
    #         ('Отдушка', 10, 100, 499, 1)
    #     ]
    # )
    m = x.get_material_list(1)
    print(m)

    from main import calculating
    price = calculating(m)
    print(price)

