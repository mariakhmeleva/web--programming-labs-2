from flask import Flask, redirect, url_for, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def start():
    return redirect("/menu", code=302)

@app.route("/lab1")
def lab1():
    return '''
<!doctype html>
<html>
<link rel="stylesheet" href="'''+url_for('static', filename='static.css')+'''">
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

        <a href="http://127.0.0.1:5000/menu"> Меню </a>

         <h1>Реализованные роуты</h1>
    <ul>
    <li> <a href="http://127.0.0.1:5000/lab1/oak"> Дуб </a> </li>
    <li> <a href="http://127.0.0.1:5000/lab1/student"> Студент </a> </li>
    <li> <a href="http://127.0.0.1:5000/lab1/python"> Python </a> </li>
    <li> <a href="http://127.0.0.1:5000/lab1/dota"> Dota 2 </a> </li>
    </ul>

        <footer>
            &copy: Хмелёва Мария, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
'''

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

    <a href="http://127.0.0.1:5000/lab1"> Лабораторная работа 1 </a>

        <footer>
            &copy: Хмелёва Мария, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
'''

@app.route('/lab1/oak')
def oak():
    return '''
<!doctype html>
<html>
 <link rel="stylesheet" href="'''+url_for('static', filename='static.css')+'''">
    <body>
        <h1>Дуб</h1>

        <p>
        Дуб — это величественное дерево, которое известно своим впечатляющим размером и долговечностью. 
        Существует множество видов дубов, но наиболее распространены дуб черешчатый и дуб пушистый. 
        Эти деревья могут достигать в высоту до 40 метров и жить более 500 лет. Листья дуба имеют характерную lobed форму 
        и меняют свой цвет в зависимости от поры года: весной они яркие и светло-зеленые, летом становятся темно-зелеными, 
        а осенью окрашиваются в золотисто-желтые и красные оттенки. Дуб также славится своими прочными и тяжелыми древесными волокнами, 
        которые используют в строительстве и для производства мебели.
        Кроме того, дуб играет важную роль в экосистеме. Его шишки и желудями питаются множество животных, включая белок и птиц. 
        Дерево также предоставляет убежище и место для гнездования многим видам. В культуре дуб символизирует силу и стойкость, 
        часто ассоциируясь с мудростью и долголетием. Дубы являются важной частью лесных экосистем и садов, и их защита — 
        это забота о природном наследии и будущих поколениях.
        </p>

        <img src="''' + url_for('static', filename='oak.jpg') + '''">
        
    </body>
</html>
'''    

@app.route('/lab1/student')
def student():
    return '''
<!doctype html>
<html>
 <link rel="stylesheet" href="'''+url_for('static', filename='static.css')+'''">
    <title> Студент </title>
    
    <body>
        <h1>Хмелёва Мария Сергеевна</h1>
        <img src="''' + url_for('static', filename='logo.jpg') + '''">
        
    </body>
</html>
'''   
@app.route('/lab1/python')
def py():
    return '''
<!doctype html>
<html>
 <link rel="stylesheet" href="'''+url_for('static', filename='static.css')+'''">
  <title>Python</title>
    <body>
        <h1>Язык программирования Python</h1>

        <p>
        Python — это высокоуровневый язык программирования, который отличается
        простотой и читаемостью синтаксиса. Он широко используется для разработки веб-приложений, 
        анализа данных, автоматизации задач и создания искусственного интеллекта благодаря большому 
        количеству библиотек и фреймворков. Python поддерживает множество парадигм программирования,
        включая объектно-ориентированное, функциональное и процедурное программирование, что делает его универсальным 
        инструментом для разработчиков.
        </p>

        <img src="''' + url_for('static', filename='py.jpg') + '''">
        
    </body>
</html>
'''    

@app.route('/lab1/dota')
def dota():
    return '''
<!doctype html>
<html>
 <link rel="stylesheet" href="'''+url_for('static', filename='static.css')+'''">
 <title>Dota 2</title>
    <body>
        <h1>Dota 2</h1>

        <p>
       Dota 2 — это многопользовательская онлайн-игра в жанре MOBA (Multiplayer Online Battle Arena), 
       разработанная компанией Valve. В игре две команды из пяти игроков сражаются друг с другом с целью разрушить 
       трон противника, управляя уникальными героями, каждый из которых обладает своими способностями и характеристиками. 
       Dota 2 известна своей сложной стратегией и глубокой механикой, что делает её одной из самых популярных киберспортивных 
       дисциплин в мире.

        </p>

        <img src="''' + url_for('static', filename='dota2.jpg') + '''">
        
    </body>
</html>
'''    


@app.route('/lab2/example')
def example():
    name = 'Мария Хмелева'
    number = '2'
    group = 'ФБИ-23'
    course_number = 3
    return render_template('example.html',name=name,number=number,
                           group=group,course_number=course_number)
    
