from flask import Blueprint, render_template, request, redirect, url_for, session

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/')
def main():
    if 'name' in session and 'age' in session and 'gender' in session  and 'preference2' in session:
        return redirect(url_for('lab9.congratulations'))
    return render_template('lab9/index.html')

@lab9.route('/lab9/age', methods=['GET', 'POST'])
def age():
    session['name'] = request.form.get('name')
    return render_template('lab9/age.html')

@lab9.route('/lab9/gender', methods=['GET', 'POST'])
def gender():
    session['age'] = request.form.get('age')
    return render_template('lab9/gender.html')

@lab9.route('/lab9/preference1', methods=['GET', 'POST'])
def preference1():
    session['gender'] = request.form.get('gender')
    return render_template('lab9/preference1.html')

@lab9.route('/lab9/preference2', methods=['GET', 'POST'])
def preference2():
    session['preference1'] = request.form.get('preference1')
    preference2 = request.form.get('preference2')
    session['preference2'] = None
    print('1',session)
   
    return render_template('lab9/preference2.html', preference1=session.get('preference1'))

@lab9.route('/lab9/congratulations', methods=['POST','GET'])
def congratulations():
    if session.get('preference2') == None:
        preference2 = request.form.get('preference2')
        session['preference2'] = preference2
        print('Выполнил')
    else:
        preference2 = session.get('preference2')
    name = session.get('name')
    age = session.get('age')
    gender = session.get('gender')
    preference1 = session.get('preference1')
    
    
    # Отображаем финальную страницу
    print('КОнц',session)
    return render_template('lab9/congratulations.html', name=name, age=age, gender=gender, preference1=preference1, preference2=preference2)


@lab9.route('/lab9/reset',methods=['POST'])
def reset():
    session.clear()  # Очищаем сессию
    return redirect(url_for('lab9.main'))