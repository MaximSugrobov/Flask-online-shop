from flask import Flask, render_template, request, redirect
import json
import mysql.connector
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
'''app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DSsite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Pictures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True)
    text = db.Column(db.Text, nullable=False)'''


@app.route('/')
def home_page():
    return render_template('home_page.html')


@app.route('/about')
def about():
    return render_template('about.html')


'''@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        text = request.form['text']
        picture = Pictures(title=title, price=price, text=text)
        try:
            db.session.add(picture)
            db.session.commit()
            return redirect('/')
        except:
            return 'Что-то пошло не так, проверьте правильность заполняемых данных'
    else:
        return render_template('create.html')'''


@app.route('/pictures')
def get_widgets():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="password",
        database="inventory"
    )
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM pictures")
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    cursor.close()
    return json.dumps(json_data)


@app.route('/initdb')
def db_init():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="password"
    )
    cursor = mydb.cursor()

    cursor.execute("DROP DATABASE IF EXISTS inventory")
    cursor.execute("CREATE DATABASE inventory")
    cursor.close()

    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="password",
        database="inventory"
    )
    cursor = mydb.cursor()

    cursor.execute("DROP TABLE IF EXISTS pictures")
    cursor.execute("CREATE TABLE pictures (title VARCHAR(255), price INTEGER, "
                   "active BOOLEAN, description VARCHAR(255))")
    cursor.close()
    return 'init database'


if __name__ == '__main__':
    app.run(debug=True)
