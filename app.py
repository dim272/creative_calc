from flask import Flask, render_template

from db_interface import DbConnection

app = Flask(__name__)


@app.route("/")
def hello():
    db = DbConnection()
    handmade_list = db.get_total_handmade_list(limit=20)
    return render_template("index.html", handmade_list=handmade_list)


if __name__ == '__main__':
    app.run(debug=True, port=5002)
