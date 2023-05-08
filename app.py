from flask import Flask, render_template, request, session

from db_interface import DataBase
from main import date_format

app = Flask(__name__)
app.secret_key = '123'


@app.route("/")
def main_page():
    handmade_items = []
    db = DataBase()
    handmade_list = db.get_last_handmade(limit=20)
    for item in handmade_list:
        handmade_items.append({
            'name': item[1],
            'link': '#',
            'date_added': date_format(item[5]),
            'price': item[4],
            'user_name': item[3]
        })
    return render_template("index.html", h1='Лучшие работы', handmade_list=handmade_items)


@app.route("/login.html")
def login_page():
    return render_template("login.html", h1='Авторизация')


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

        msg = f"Здравствуйте {user_name}"
    else:
        msg = "Вы ввели неправильный логин или пароль."
    return render_template("login.html", msg=msg)


@app.route("/registration.html")
def registration_page():
    return render_template("registration.html", h1='Регистрация')


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
    return render_template("create.html")


if __name__ == '__main__':
    app.run()
