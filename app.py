from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from db import db
from os import path
from lab1 import lab1
from lab2 import lab2 
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'G45qw765LpoGGG5')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

if app.config['DB_TYPE']=='postgres':
    db_name = 'maria_xmeleva_orm'
    db_user = 'maria_xmeleva_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path,"maria_xmeleva_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'


db.init_app(app)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)

@app.route("/")
@app.route("/index")
def start():
    return redirect("/menu", code=302)

@app.route("/menu")
def menu():
    return '''
<!doctype html>
<html>
<link rel="stylesheet" href="'''+url_for('static', filename='static.css')+'''">
    <head>
        <title> НГТУ, ФБ, Лабораторные работы»</title/>
    </head>
    <body>
        <header>
           НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>

    <a href="/lab1"> Лабораторная работа 1 </a> <br>

    <a href="/lab2"> Лабораторная работа 2 </a> <br>

    <a href="/lab3"> Лабораторная работа 3 </a> <br>

    <a href="/lab4"> Лабораторная работа 4 </a> <br>

    <a href="/lab5"> Лабораторная работа 5 </a> <br>

    <a href="/lab6"> Лабораторная работа 6 </a> <br>

    <a href="/lab7"> Лабораторная работа 7 </a> <br>

    <a href="/lab8"> Лабораторная работа 8 </a> <br>
        <footer>
            &copy: Хмелёва Мария, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
'''