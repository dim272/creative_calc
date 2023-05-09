import sqlite3
from typing import List, Dict, Tuple, Optional
from datetime import datetime


class DataBase:
    """  Класс для работы с базой данных  """

    def __init__(self):
        """ Создание и подключение к базе данных, выполнение функции создания таблиц   """
        self.connect = sqlite3.connect('lavander.db')
        self.create_tables()

    def create_tables(self):
        """ Создание таблиц в базе данных """
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

    def create_user(self, email: str, password: str, name: str):
        """ Сохранение нового пользователя в бд

        :param email: Логин пользователя
        :param password: Пароль пользователя
        :param name: Имя пользователя
        """
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

    def create_handmade(self, name: str, is_private: int, user_id: int, price: int) -> int:
        """Сохранение новой работы в бд

        :param name: Название работы
        :param is_private: Приватный/открытый работы
        :param user_id: номер/id пользователя
        :param price: себестоимость работы вычисленная
        :return: id сохранённой работы
        """
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
            return cursor.lastrowid

    def create_materials(self, handmade_id: int, materials: List[Dict]):
        """ Сохранение списка материалов в базу данных

        :param handmade_id: Уникальный номер работы.
        :param materials: Список словарей в каждом из которых хранится информация о материале.
        """
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

    def get_last_handmade(self, limit: int = 25) -> List[Tuple]:
        """ Запрашивает из таблицы handmade все доступные (не приватные) работы.

         Для вывода на экран списка работ на главной страницы.

        :param limit: Ограничение количества работ.
        :return: Список работ
        """
        with self.connect:
            cursor = self.connect.cursor()
            cursor.execute(
                """
                SELECT h.id ,h.name ,h.is_private ,u.name ,h.price ,h.date_added  FROM handmade h 
                INNER JOIN "user" u ON h.user_id = u.id 
                WHERE h.is_private = 0
                ORDER BY h.id DESC 
                LIMIT ?               
                """,
                (limit,)
            )
            handmade_list=cursor.fetchall()
        return handmade_list

    def get_handmade_by_user(self, user_id: int) -> List[Tuple]:
        """ Запрашивает из таблицы handmade все работы определенного пользователя.

        Для вывода на экран списка работ в личном кабинете.

        :param user_id: Номер пользователя.
        :return: Список работ.
        """
        with self.connect:
            cursor = self.connect.cursor()
            cursor.execute(
                """
                SELECT h.id ,h.name ,h.is_private ,u.name ,h.price ,h.date_added  FROM handmade h 
                INNER JOIN "user" u ON h.user_id = u.id 
                WHERE h.user_id = ?
                ORDER BY h.id DESC 
                """,
                (user_id,)
            )
            handmade_list = cursor.fetchall()
            return handmade_list

    def get_materials(self,handmade_id) -> List[Tuple]:
        """Запрашивает из таблицы material список материалов относящихся к определенной работе

        Для вывода на экран списка материалов на странице работы

        :param handmade_id:
        :return:
        """
        with self.connect:
            cursor = self.connect.cursor()
            cursor.execute(
                """
                SELECT * FROM material
                WHERE handmade_id = ?
                """,
                (handmade_id,)
            )
            materials = cursor.fetchall()
        return materials

    def check_user_exists(self, email: str) -> bool:
        """Производит поиск в таблице user на наличие строки с переданными значением email.

        Используется в процессе регистрации.

        :param email: Адрес электронной почты пользователя (логин).
        :return: Существует / не существует пользователь с таким email.
        """
        with self.connect:
            cursor = self.connect.cursor()
            cursor.execute(
                """
                SELECT * FROM user
                WHERE email = ?
                """,
                (email,)
            )
            return bool(cursor.fetchone())

    def login(self, email: str, password: str) -> Optional[Tuple[str]]:
        """Производит поиск в таблице user на наличие строки с переданными значениями email и password.

        Используется при авторизации пользователя.
        Возвращает информацию о пользователе, если он введёт правильные email и password, находящиеся в бд.
        Иначе возвращает None.

        :param email: Адрес электронной почты пользователя (логин).
        :param password: Пароль пользователя.
        :return: Данные пользователя с указанным email и password.
        """

        with self.connect:
            cursor = self.connect.cursor()
            cursor.execute(
                """
                SELECT * FROM user
                WHERE email = ? AND password = ?
                """,
                (email, password)
            )
            return cursor.fetchone()


# if __name__ == "__main__":
#     db = DataBase()
#     db.create_user('test11@mail.ru', '111', 'test11')
#
#     materials = [
#         {
#             'name': 'Воск',
#             'quantity': 100,
#             'total_quantity': 500,
#             'price': 349,
#         },
#         {
#             'name': 'Фитиль',
#             'quantity': 1,
#             'total_quantity': 20,
#             'price': 149,
#         },
#         {
#             'name': 'Отдушка',
#             'quantity': 10,
#             'total_quantity': 100,
#             'price': 499,
#         }
#     ]
#
#     from main import calculating
#
#     price = calculating(materials)
#
#     handmade_id = db.create_handmade('Candle', 0, 3, price)
#     db.create_materials(handmade_id, materials)
