from flask import Blueprint, redirect, url_for, render_template
lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/example')
def example():
    name = 'Мария Хмелева'
    number = '2'
    group = 'ФБИ-23'
    course_number = '3'
    fruits = [
        {'name': 'яблоки', 'price': 100}, 
        {'name': 'груши', 'price': 120}, 
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95}, 
        {'name': 'манго', 'price': 321},  
    ]

    books = [
        {'name': 'Евгений Онегин', 'author': 'Алесандр Пушкин','janr': 'роман', 'price': 315, 'str': 224}, 
        {'name': 'Десять негритят', 'author': 'Агата Кристи', 'janr': 'детектив','price': 410, 'str': 288}, 
        {'name': 'Холодный дом', 'author': 'Чарльз Диккенс', 'janr': 'роман','price': 670, 'str': 1300},
        {'name': 'Дракула', 'author': 'Брэм Стокер', 'janr': 'роман','price': 378, 'str': 471},
        {'name': 'Королевы Нью-Йорка', 'author': 'Е.Л. Шень', 'janr': 'young adult','price': 355, 'str': 268},
        {'name': 'Влюбленный призрак', 'author': 'Марк Леви', 'janr': 'проза','price': 300, 'str': 211},
        {'name': 'Эмма', 'author': 'Джейн Остен', 'janr': 'роман','price': 400, 'str': 510},
        {'name': 'Мадонна в меховом манто', 'author': 'Сабахаттин Али', 'janr': 'роман','price': 298, 'str': 192},
        {'name': 'Прачечная, стирающая надежды', 'author': 'Ким Чжи Юн', 'janr': 'роман','price': 543, 'str': 253},
        {'name': 'Под маской, или Сила женщины', 'author': 'Луиза Мэй Олкотт', 'janr': 'роман','price': 373, 'str': 146},
    ]

    return render_template('example.html',name=name,number=number,
                           group=group,course_number=course_number, fruits=fruits,
                           books=books)


@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')


@lab2.route('/lab2/chto-to-neobichnoe/')
def flowers():
    return render_template('chto-to-neobichnoe.html')

    

