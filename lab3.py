from flask import Blueprint, render_template,request, make_response, redirect
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name', 'аноним')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age', 'неизвестен')
    return render_template('lab3/lab3.html', name=name, name_color = name_color, age=age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name','Alex', max_age = 5)
    resp.set_cookie('age','неизвестен')
    resp.set_cookie('name_color','red')
    resp.set_cookie('age')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name','Alex', max_age = 0)
    resp.set_cookie('age','неизвестен')
    resp.set_cookie('name_color','black')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    if not age == '': 
        errors['age'] = 'Заполните поле!' 

    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex,errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    global price
    price = 0
    drink = request.args.get('drink')
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    else:
        pass
    if request.args.get('sugar') == 'on':
        price += 10
    else:
        pass
    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    global price
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        if 'clear' in request.form:  # Проверяем, была ли нажата кнопка "Очистить куки"
            resp = make_response(redirect('/lab3/settings'))
            # Очистка всех кук
            resp.set_cookie('color', '', expires=0)
            resp.set_cookie('background_color', '', expires=0)
            resp.set_cookie('font_size', '', expires=0)
            resp.set_cookie('text_align', '', expires=0)
            return resp

        # Обработка обновления куки
        color = request.form.get('color')
        background_color = request.form.get('background_color')
        font_size = request.form.get('font_size')
        text_align = request.form.get('text_align')

        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if background_color:
            resp.set_cookie('background_color', background_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if text_align:
            resp.set_cookie('text_align', text_align)
        return resp

    # Обработка GET-запроса
    color = request.cookies.get('color')
    background_color = request.cookies.get('background_color')
    font_size = request.cookies.get('font_size')
    text_align = request.cookies.get('text_align')


    resp = make_response(render_template('lab3/settings.html', 
                                        color=color,
                                        background_color=background_color,
                                        font_size=font_size,
                                        text_align=text_align))
    return resp

@lab3.route('/lab3/ticket_form') 
def ticket(): 
    return render_template('lab3/ticket_form.html') 
 
@lab3.route('/lab3/ticket', methods=['POST']) 
def calculate(): 
    fio = request.form['fio'] 
    shelf = request.form['shelf'] 
    bedding = 'bedding' in request.form 
    luggage = 'luggage' in request.form 
    age = int(request.form['age']) 
    departure = request.form['departure'] 
    destination = request.form['destination'] 
    date = request.form['date'] 
    insurance = 'insurance' in request.form 
 
    # Цены и расчеты 
    price = 700 if age < 18 else 1000 
 
    if shelf in ['lower', 'lower_side']: 
        price += 100 
    if bedding: 
        price += 75 
    if luggage: 
        price += 250 
    if insurance: 
        price += 150 
 
    ticket_info = { 
        'fio': fio, 
        'shelf': shelf, 
        'bedding': bedding, 
        'luggage': luggage, 
        'age': age, 
        'departure': departure, 
        'destination': destination, 
        'date': date, 
        'insurance': insurance, 
        'price': price, 
        'child_ticket': age < 18 
    } 
 
    return render_template('lab3/ticket.html', ticket=ticket_info)


books = [
    {"name": "1984", "price": 300, "author": "Джордж Оруэлл", "year": 1949, "pages": 328, "rating": 4.5},
    {"name": "Убить пересмешника", "price": 400, "author": "Харпер Ли", "year": 1960, "pages": 281, "rating": 4.7},
    {"name": "Гордость и предубеждение", "price": 250, "author": "Джейн Остин", "year": 1813, "pages": 279, "rating": 4.5},
    {"name": "Мастер и Маргарита", "price": 450, "author": "Михаил Булгаков", "year": 1967, "pages": 384, "rating": 4.8},
    {"name": "Анна Каренина", "price": 500, "author": "Лев Толстой", "year": 1877, "pages": 864, "rating": 4.6},
    {"name": "Преступление и наказание", "price": 600, "author": "Федор Достоевский", "year": 1866, "pages": 430, "rating": 4.4},
    {"name": "451 градус по Фаренгейту", "price": 320, "author": "Рэй Брэдбери", "year": 1953, "pages": 249, "rating": 4.3},
    {"name": "Портрет Дориана Грея", "price": 350, "author": "Оскар Уайльд", "year": 1890, "pages": 254, "rating": 4.2},
    {"name": "Старик и море", "price": 330, "author": "Эрнест Хемингуэй", "year": 1952, "pages": 128, "rating": 4.1},
    {"name": "На западном фронте без перемен", "price": 370, "author": "Эрих Мария Ремарк", "year": 1929, "pages": 328, "rating": 4.5},
    {"name": "О дивный новый мир", "price": 290, "author": "Олдос Хаксли", "year": 1932, "pages": 311, "rating": 4.3},
    {"name": "Доктор Живаго", "price": 600, "author": "Борис Пастернак", "year": 1957, "pages": 572, "rating": 4.4},
    {"name": "Слово о полку Игореве", "price": 150, "author": "Неизвестный", "year": 1185, "pages": 100, "rating": 4.6},
    {"name": "Война и мир", "price": 800, "author": "Лев Толстой", "year": 1869, "pages": 1225, "rating": 4.9},
    {"name": "Тетрадь смерти", "price": 400, "author": "Цугуми Оба", "year": 2003, "pages": 600, "rating": 4.5},
    {"name": "Сияние", "price": 350, "author": "Стивен Кинг", "year": 1977, "pages": 447, "rating": 4.4},
    {"name": "Дар", "price": 670, "author": "Владимир Набоков", "year": 1937, "pages": 544, "rating": 4.5},
    {"name": "Звериная ферма", "price": 210, "author": "Джордж Оруэлл", "year": 1945, "pages": 112, "rating": 4.6},
    {"name": "Безмолвный пациент", "price": 540, "author": "Алекс Михаэлидис", "year": 2019, "pages": 368, "rating": 4.3},
    {"name": "Тень горы", "price": 430, "author": "Грегори Дэвид Робертс", "year": 2009, "pages": 720, "rating": 4.7}
]

@lab3.route('/lab3/books_search', methods=['GET', 'POST'])
def books_search():
    if request.method == 'POST':
        min_price = float(request.form.get('min_price', 0))
        max_price = float(request.form.get('max_price', float('inf')))
        
        # Фильтруем товары по цене
        filtered_books = [
            books for books in books
            if min_price <= books['price'] <= max_price
        ]
        return render_template('lab3/books_result.html', books=filtered_books)

    return render_template('lab3/books_search.html', books=books)
