import sqlite3
from datetime import datetime


class DataBase:
    def __init__(self):
        self.connect = sqlite3.connect('lavander.db')
        self.create_db()

    def create_db(self):
        with self.connect:
            cursor = self.connect.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user 
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    name TEXT NOT NULL,
                    date_added DATETIME NOT NULL
                ) 
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS handmade
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    is_private INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    price INTEGER NOT NULL,
                    date_added DATETIME NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user (id)
                ) 
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS material
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    total_quantity INTEGER NOT NULL,
                    price INTEGER NOT NULL,
                    handmade_id INTEGER NOT NULL,
                    date_added DATETIME NOT NULL,
                    FOREIGN KEY (handmade_id) REFERENCES handmade (id)
                ) 
                """
            )
            self.connect.commit()

    def create_user(self, email, password, name):
        with self.connect:
            date_added = datetime.now()

            cursor = self.connect.cursor()
            cursor.execute(
                """
                INSERT INTO user (email,password,name,date_added)
                VALUES (?,?,?,?)
                """,
                (email, password, name, date_added)
            )
            self.connect.commit()

    def create_handmade(self, name, is_private, user_id,price):
        with self.connect:
            date_added = datetime.now()

            cursor = self.connect.cursor()
            cursor.execute(
                """
                INSERT INTO handmade (name,is_private,date_added,user_id,price)
                VALUES (?,?,?,?,?)
                """,
                (name, is_private, date_added, user_id, price)

            )
            self.connect.commit()

    def create_materials(self, handmade_id, materials):
        with self.connect:
            date_added = datetime.now()
            cursor = self.connect.cursor()
            for material in materials:
                cursor.execute(
                    """
                    INSERT INTO material (name,quantity,total_quantity,price,handmade_id,date_added)
                    VALUES (?,?,?,?,?,?)
                    """,
                    (material['name'], material['quantity'], material['total_quantity'], material['price'], handmade_id,
                     date_added)
                )
            self.connect.commit()

    def get_last_handmade(self, limit=25):
        with self.connect:
            cursor = self.connect.cursor()
            cursor.execute(
                """
                SELECT * FROM handmade 
                WHERE is_private = 0
                ORDER BY id DESC 
                LIMIT (?)               
                """,
                (limit,)
            )
            handmade_list=cursor.fetchall()
        return handmade_list

    def get_handemade_by_user(self,user_id):
        with self.connect:
            cursor = self.connect.cursor()
            cursor.execute(
                """
                SELECT * FROM handmade
                WHERE user_id = (?)
                ORDER BY id DESC
                """,
                (user_id,)
            )
            handmade_list = cursor.fetchall()
            return handmade_list

    def get_materials(self,handmade_id):
        with self.connect:
            cursor = self.connect.cursor()
            cursor.execute(
                """
                SELECT * FROM material
                WHERE handmade_id = (?)
                """,
                (handmade_id,)
            )
            materials = cursor.fetchall()
            return materials
