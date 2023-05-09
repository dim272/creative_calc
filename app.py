from typing import List

from flask import Flask, render_template, request, session, redirect, url_for

from db_interface import DataBase
from main import calculating, prepare_handmade_list, date_format
import consts

app = Flask(__name__)
app.secret_key = '123'


@app.route("/")
def main_page():
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
def login_page():
    return render_template("login.html",
                           h1='Авторизация',
                           nav_links=consts.NOT_LOGIN_NAV_LIST,
                           categories=consts.CATEGORIES)


@app.route('/login', methods=['POST'])
def login():
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
        session['categories'] = consts.CATEGORIES
        session['nav_links'] = consts.LOGIN_NAV_LIST

        return profile_page()
    else:
        msg = "Вы ввели неправильный логин или пароль."
        return render_template("login.html", msg=msg)


@app.route('/logout')
def logout():
    session['loggedin'] = False
    del session['id']
    del session['username']
    return main_page()


@app.route("/registration.html")
def registration_page():
    return render_template("registration.html",
                           h1='Регистрация',
                           nav_links=consts.NOT_LOGIN_NAV_LIST,
                           categories=consts.CATEGORIES
                           )


@app.route('/registration', methods=['POST'])
def registration():
    db = DataBase()
    email = request.form.get('email')
    name = request.form.get('username')
    password = request.form.get('password')
    user_exist = db.check_user_exists(email)
    if user_exist:
        msg = "Пользователь с таким email уже зарегистрирован."
    else:
        db.create_user(email, password, name)
        msg = "Регистрация прошла успешно."
    return render_template("registration.html", msg=msg)


@app.route("/create.html")
def create():
    if not session.get('loggedin'):
        return login_page()
    else:
        return render_template("create.html",
                               h1='Создание новой работы',
                               nav_links=consts.LOGIN_NAV_LIST,
                               categories=consts.CATEGORIES)


@app.route('/create', methods=['POST'])
def create_handmade():
    handmade_name = request.form.get('name')
    is_private = 0 if request.form.get('is_private') == 'false' else 1
    material_list: List[List[str]] = list(request.form.listvalues())
    materials = []
    for name in material_list[2]:
        materials.append({'name': name})

    for index, quantity in enumerate(material_list[3]):
        materials[index]['quantity'] = int(quantity)

    for index, total_quantity in enumerate(material_list[4]):
        materials[index]['total_quantity'] = int(total_quantity)

    for index, price in enumerate(material_list[5]):
        materials[index]['price'] = int(price)

    handmade_price = calculating(materials)
    user_id = session.get('id')

    db = DataBase()
    handmade_id = db.create_handmade(name=handmade_name, is_private=is_private, user_id=user_id, price=handmade_price)
    db.create_materials(handmade_id=handmade_id, materials=materials)

    return profile_page()


@app.route('/profile.html')
def profile_page():
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
        return render_template('login.html')


if __name__ == '__main__':
    app.run()
