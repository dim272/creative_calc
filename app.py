from flask import Flask, render_template

from db_interface import DataBase

app = Flask(__name__)


@app.route("/")
def main_page():
    db = DataBase()
    handmade_items = []
    handmade_list = db.get_last_handmade(limit=20)
    for item in handmade_list:
        handmade_items.append({
            'name': item[0],
            'link': '#',
            'date_added': item[1],
            'price': item[2],
            'user_name': item[3]
        })
    return render_template("index.html", handmade_list=handmade_items)


@app.route("/login.html")
def login_page():
    return "<h1>Creative calc</h1>"


if __name__ == '__main__':
    app.run(debug=True, port=5002)
