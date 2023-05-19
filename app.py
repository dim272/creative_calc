import time
from pathlib import Path
from typing import List

from flask import Flask, render_template, request, session

from db_interface import DataBase
from main import calculating, prepare_handmade_list
import consts

app = Flask(__name__)
app.secret_key = '12345'


@app.route("/")
def main_page():
    """Отображение главной страницы"""
    db = DataBase()
    handmade_list = prepare_handmade_list(db.get_last_handmade(limit=20))
    logged_in = session.get('loggedin')
    if logged_in:
        nav_links = consts.LOGIN_NAV_LIST
    else:
        nav_links = consts.NOT_LOGIN_NAV_LIST

    return render_template("index.html",
                           h1='Лучшие работы',
                           handmade_list=handmade_list,
                           nav_links=nav_links,
                           categories=consts.CATEGORIES)


@app.route("/login.html")
def login_page(msg=None):
    """Отображение страницы авторизации"""
    if not msg:
        msg = "Введите логин и пароль"
    return render_template("login.html",
                           h1='Авторизация',
                           msg=msg,
                           nav_links=consts.NOT_LOGIN_NAV_LIST,
                           categories=consts.CATEGORIES)


@app.route('/login', methods=['POST'])
def login():
    """Функция обработки запроса авторизации.

    Обрабатывает форму login.
    Проверяет наличие пользователя в таблице user с введёнными в форму email и password.
    """
    db = DataBase()
    email = request.form.get('email')
    password = request.form.get('password')
    user_info = db.login(email, password)
    if user_info:
        user_id = user_info[0]
        user_name = user_info[3]

        session['loggedin'] = True
        session['id'] = user_id
        session['username'] = user_name

        return profile_page()
    else:
        msg = "Вы ввели неправильный логин или пароль."
        return render_template("login.html", msg=msg)


@app.route('/logout')
def logout():
    """Функция обработки кнопки "Выход".

    Удаляет данные пользователя из объекта session. Перенаправляет на главную страницу.
    """
    session['loggedin'] = False
    del session['id']
    del session['username']
    return main_page()


@app.route("/registration.html")
def registration_page(msg=None):
    """Отображение страницы регистрации пользователя"""
    return render_template("registration.html",
                           h1='Регистрация',
                           msg=msg,
                           nav_links=consts.NOT_LOGIN_NAV_LIST,
                           categories=consts.CATEGORIES
                           )


@app.route('/registration', methods=['POST'])
def registration():
    """Функция обработки запроса регистрации.

    Обрабатывает форму registration.
    Проверяет наличие пользователя в таблице user с введённым в форму email.
    Если пользователь не найден, сохраняет данные нового пользователя.
    """
    db = DataBase()
    email = request.form.get('email')
    name = request.form.get('username')
    password = request.form.get('password')
    user_exist = db.check_user_exists(email)
    if user_exist:
        msg = "Пользователь с таким email уже зарегистрирован."
        return registration_page(msg)
    else:
        db.create_user(email, password, name)
        msg = "Регистрация прошла успешно."
        return login_page(msg)


@app.route("/create.html")
def create_page():
    """Отображение страницы создания новой работы"""
    if not session.get('loggedin'):
        return login_page()
    else:
        return render_template("create.html",
                               h1='Создание новой работы',
                               nav_links=consts.LOGIN_NAV_LIST,
                               categories=consts.CATEGORIES)


@app.route('/create', methods=['POST'])
def create_handmade():
    """Функция обработки запроса создания новой работы.

     Обрабатывает форму create_handmade.

     Из списка списков перекладываем информацию о материалах в список словарей, для вычисления себестоимости работы
     и сохранения материалов в бд.
     Сохраняем работу и материалы в бд.
     """
    handmade_name = request.form.get('name')
    is_private = 0 if request.form.get('is_private') == 'false' else 1
    tax = request.form.get('tax')

    materials = []
    for name in request.form.getlist('m_name'):
        materials.append({'name': name})

    for index, quantity in enumerate(request.form.getlist('m_quantity')):
        materials[index]['quantity'] = int(quantity)

    for index, total_quantity in enumerate(request.form.getlist('m_total_quantity')):
        materials[index]['total_quantity'] = int(total_quantity)

    for index, price in enumerate(request.form.getlist('m_price')):
        materials[index]['price'] = int(price)

    handmade_price = calculating(materials, tax)
    user_id = session.get('id')

    # сохраняем картинку
    image_name = 'default.jpg'
    image = request.files['image']
    if image.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        # добавляем цифры для создания уникального имени файла
        seconds = time.time()
        image_file_part = str(seconds).replace('.', '')[4:14] + '_'
        image_name = image_file_part + image.filename.replace(' ', '_')
        # генерируем путь для сохранения файла
        image_save_path = Path(consts.IMAGE_UPLOAD_DIR / image_name)
        # сохраняем файл
        image.save(dst=image_save_path)

    db = DataBase()
    handmade_id = db.create_handmade(
        name=handmade_name,
        is_private=is_private,
        user_id=user_id,
        price=handmade_price,
        filename=image_name
    )
    db.create_materials(handmade_id=handmade_id, materials=materials)

    return profile_page()


@app.route('/profile.html')
def profile_page():
    """Отображение страницы личного кабинета пользователя"""
    user_id = session.get('id')
    if user_id:
        db = DataBase()
        handmade_list = prepare_handmade_list(db.get_handmade_by_user(user_id))
        return render_template("profile.html",
                               h1='Личный кабинет',
                               handmade_list=handmade_list,
                               nav_links=consts.LOGIN_NAV_LIST,
                               categories=consts.CATEGORIES)
    else:
        return login_page()


@app.route('/single.html')
def single_page():
    handmade_id = request.values.get('id')
    db = DataBase()
    handmade_info = prepare_handmade_list([db.get_handmade_by_id(handmade_id)])
    materials_from_db = db.get_materials(handmade_id)
    materials = [
        {
            'name': material[1],
            'quantity': material[2]
        }
        for material in materials_from_db
    ]

    return render_template("single.html",
                           h1=handmade_info[0]['name'],
                           handmade=handmade_info[0],
                           materials=materials,
                           nav_links=consts.LOGIN_NAV_LIST,
                           categories=consts.CATEGORIES)


if __name__ == '__main__':
    app.run(port=5002)
