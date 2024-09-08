from flask import Flask
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def start():
    return """
<!doctype html>
<html>
    <head>
        <title> НГТУ, ФБ, Лабораторные работы»</title/>
    </head>
    <body>
        <header>
           НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>

        <a href="http://127.0.0.1:5000/lab1"> Лабораторная работа 1 </a>

        <footer>
            &copy: Хмелёва Мария, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""

@app.route("/lab1")
def lab1():
    return """
<!doctype html>
<html>
    <head>
        <title> Хмелёва Мария Сергеевна, лабораторная 1</title/>
    </head>
    <body>
        <header>
            НГТУ, ФБ, Лабораторная 1
        </header>

        <h1>web-сервер на flask</h1>

        <p>Flask — фреймворк для создания веб-приложений на языке
        программирования Python, использующий набор инструментов
        Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
        называемых микрофреймворков — минималистичных каркасов
        веб-приложений, сознательно предоставляющих лишь самые ба-
        зовые возможности.</p>

        <footer>
            &copy: Хмелёва Мария, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""

