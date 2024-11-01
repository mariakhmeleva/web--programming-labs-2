from flask import Blueprint, render_template,request, make_response, redirect, session
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods=["POST"])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div-form.html', error='Оба поля должны быть заполнены!')
    try:
        x1 = int(x1)
        x2 = int(x2)
        if x2 == 0:
            return render_template('lab4/div-form.html', error='Деление на ноль невозможно', x1=x1, x2=x2)
        result = x1 / x2
        return render_template('lab4/div-form.html', x1=x1, x2=x2, result=result)
    except ValueError:
        return render_template('lab4/div-form.html', error='Оба поля должны содержать числа')
    
# Суммирование
@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum_():
    x1 = request.form.get('x1') or '0'
    x2 = request.form.get('x2') or '0'
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/sum.html', error='Оба поля должны содержать числа')
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

# Умножение
@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1') or '1'
    x2 = request.form.get('x2') or '1'
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/mul.html', error='Оба поля должны содержать числа')
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)

# Вычитание
@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны содержать числа')
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/sub.html', error='Оба поля должны содержать числа')
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)

# Возведение в степень
@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def pow_():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны содержать числа')
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/pow.html', error='Введите числовые значения')
    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='0^0 не определено')
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)

tree_count = 0

MAX_TREES = 10 

@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')

    if operation == 'cut':
        if tree_count > 0:
            tree_count -= 1
    elif operation == 'plant':
        if tree_count < MAX_TREES:
            tree_count += 1
    

    return redirect('/lab4/tree')

users = [
    {'login': 'mia22', 'password': 'pass123', 'name': 'Мия Бойка ', 'gender': 'female'},
    {'login': 'maria', 'password': 'pass456', 'name': 'Мария Хмелева', 'gender': 'female'}
]


@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        authorized = 'login' in session
        name = session['name'] if authorized else ''
        return render_template("lab4/login.html", authorized=authorized, name=name)
    
    login = request.form.get('login', '').strip()
    password = request.form.get('password', '').strip()

    if not login:
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)

    if not password:
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            session['name'] = user['name']
            return render_template('lab4/login.html', error='Успешная авторизация', authorized=True, login=login, name=user['name'])
    
    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login=login)

@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login', '').strip()
        password = request.form.get('password', '').strip()
        name = request.form.get('name', '').strip()
        gender = request.form.get('gender', '').strip()

        # Проверка, что все поля заполнены
        if not all([login, password, name, gender]):
            return render_template('lab4/register.html', error='Все поля должны быть заполнены')

        # Проверка уникальности логина
        if any(user['login'] == login for user in users):
            return render_template('lab4/register.html', error='Пользователь с таким логином уже существует')

        # Добавление пользователя в массив
        users.append({'login': login, 'password': password, 'name': name, 'gender': gender})
        return redirect('/lab4/login')
    
    return render_template('lab4/register.html')

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    session.pop('name', None)
    return redirect('/lab4/login')

# Страница списка пользователей
@lab4.route('/lab4/users')
def user_list():
    if 'login' not in session:
        return redirect('/lab4/login')

    return render_template('lab4/user_list.html', users=users)

# Удаление пользователя
@lab4.route('/lab4/delete_user', methods=['POST'])
def delete_user():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    login = session['login']
    global users
    users = [user for user in users if user['login'] != login]
    logout()
    return redirect('/lab4/users')

# Редактирование пользователя
@lab4.route('/lab4/edit_user', methods=['GET', 'POST'])
def edit_user():
    if 'login' not in session:
        return redirect('/lab4/login')

    if request.method == 'POST':
        login = session['login']
        new_name = request.form.get('name', '').strip()
        new_password = request.form.get('password', '').strip()

        if not all([new_name, new_password]):
            return render_template('lab4/edit_user.html', error='Все поля должны быть заполнены')

        for user in users:
            if user['login'] == login:
                user['name'] = new_name
                user['password'] = new_password
                session['name'] = new_name  # обновляем имя в сессии
                break

        return redirect('/lab4/users')

    return render_template('lab4/edit_user.html')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    message = ""
    snowflakes = 0

    if request.method == 'POST':
        try:
            temperature = float(request.form.get('temperature', '').strip())
        except ValueError:
            message = "Ошибка: не задана температура"
            return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes)

        if temperature < -12:
            message = "Не удалось установить температуру — слишком низкое значение"
        elif temperature > -1:
            message = "Не удалось установить температуру — слишком высокое значение"
        elif -12 <= temperature <= -9:
            message = f"Установлена температура: {temperature}°С"
            snowflakes = 3
        elif -8 <= temperature <= -5:
            message = f"Установлена температура: {temperature}°С"
            snowflakes = 2
        elif -4 <= temperature <= -1:
            message = f"Установлена температура: {temperature}°С"
            snowflakes = 1

    return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes)


@lab4.route('/lab4/order_grain', methods=['GET', 'POST'])
def order_grain():
    prices = {
        'ячмень': 12345,
        'овёс': 8522,
        'пшеница': 8722,
        'рожь': 14111
    }
    message = ""
    discount_message = ""
    total_price = 0

    if request.method == 'POST':
        grain_type = request.form.get('grain_type')
        try:
            weight = float(request.form.get('weight', '').strip())
        except ValueError:
            message = "Ошибка: вес не указан или введено некорректное значение"
            return render_template('lab4/order_grain.html', message=message, discount_message=discount_message)

        if weight <= 0:
            message = "Ошибка: вес должен быть больше 0"
        elif weight > 500:
            message = "Ошибка: такого объёма сейчас нет в наличии"
        else:
            price_per_ton = prices.get(grain_type, 0)
            total_price = price_per_ton * weight
            
            if weight > 50:
                discount = 0.1 * total_price
                total_price -= discount
                discount_message = f"Скидка за большой объем: 10% (сэкономлено {discount:.2f} руб)"
            
            message = f"Заказ успешно сформирован. Вы заказали {grain_type}. Вес: {weight} т. Сумма к оплате: {total_price:.2f} руб."
    
    return render_template('lab4/order_grain.html', message=message, discount_message=discount_message)

