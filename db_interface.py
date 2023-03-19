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
        self.cur = self.con.cursor()
        self._init_tables()

    def _init_tables(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS user 
            (
                id INTEGER PRIMARY KEY,
                email TEXT,
                password TEXT,
                name TEXT,
                about TEXT,
                added DATETIME
            )
            """
        )

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS handmade 
            (
                id INTEGER PRIMARY KEY,
                name TEXT,
                added DATETIME,
                user_id INTEGER
            );
            """
        )

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS material 
            (
                id INTEGER PRIMARY KEY,
                name TEXT,
                quantity INTEGER,
                price INTEGER,
                handmade_id INTEGER
            )
            """
        )

    def read_user(self):
        pass

    def read_handmade(self):
        pass

    def read_material(self):
        pass

    def write_value(self):
        pass
