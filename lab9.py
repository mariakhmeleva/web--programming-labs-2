from flask import Blueprint, render_template, request, redirect, url_for, session

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/')
def main():
    return render_template('lab9/index.html')

@lab9.route('/lab9/age', methods=['GET', 'POST'])
def age():
    return render_template('lab9/age.html')

@lab9.route('/lab9/gender', methods=['GET', 'POST'])
def gender():
    return render_template('lab9/gender.html')

@lab9.route('/lab9/preference1', methods=['GET', 'POST'])
def preference1():
    if request.method == 'POST':
        session['gender'] = request.form.get('gender')
        return redirect(url_for('lab9.preference2'))
    return render_template('lab9/preference1.html')

@lab9.route('/lab9/preference2', methods=['GET', 'POST'])
def preference2():
    # if 'gender' not in session:  # Проверяем, что gender есть в сессии
    #     return redirect(url_for('lab9.preference1'))
    
    if request.method == 'POST':
        session['preference1'] = request.form.get('preference1')
        return redirect(url_for('lab9.congratulations'))
    return render_template('lab9/preference2.html', preference1=session.get('preference1'))

@lab9.route('/lab9/congratulations', methods=['POST','GET'])
def congratulations():
    # Проверяем, есть ли все необходимые данные в сессии
    
    # Извлекаем preference2 из формы
    preference2 = request.form.get('preference2')
   
    # Сохраняем preference2 в сессии
    session['preference2'] = preference2
    
    name = session.get('name')
    age = session.get('age')
    gender = session.get('gender')
    preference1 = session.get('preference1')
    
    # Отображаем финальную страницу
    return render_template('lab9/congratulations.html', name=name, age=age, gender=gender, preference1=preference1, preference2=preference2)