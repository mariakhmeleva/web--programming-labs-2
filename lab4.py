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

