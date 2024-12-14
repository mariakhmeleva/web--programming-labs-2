from flask import Blueprint, redirect, url_for,render_template,request,session
from db import db
from db.models import users,articles
from flask_login import login_user, login_user,login_required,current_user,logout_user
from werkzeug.security import check_password_hash, generate_password_hash
lab8 = Blueprint('lab8', __name__)


@lab8.route("/lab8/")
@login_required
def lab():
    
    return render_template('lab8/lab8.html')

@lab8.route('/lab8/register/', methods = ['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    login_exists = users.query.filter_by(login = login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error = 'Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()

    # Автоматический логин после регистрации
    login_user(new_user, remember=False)
    return redirect('/lab8/')

@lab8.route('/lab8/login/', methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember = request.form.get('remember') == 'on'

    user = users.query.filter_by(login = login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=remember)
            return redirect('/lab8/')
    
    return render_template('/lab8/login.html', error = 'Ошибка входа: логин и/или пароль неверны')

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    # Получаем статьи текущего пользователя
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    
    # Передаем статьи в шаблон
    return render_template('lab8/articles.html', articles=user_articles)

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

@lab8.route('/lab8/articles/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')  # Используем правильное имя поля

    # Создаем новую статью
    new_article = articles(
        title=title,
        article_text=article_text,  # Используем правильное имя поля
        login_id=current_user.id,  # Связываем статью с текущим пользователем через login_id
        is_favorite=False,  # По умолчанию статья не является избранной
        likes=0  # По умолчанию количество лайков равно 0
    )

    db.session.add(new_article)
    db.session.commit()

    return redirect('/lab8/articles')
    

@lab8.route('/lab8/articles/<int:article_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)

    if article.login_id != current_user.id:
        return "У вас нет прав на редактирование этой статьи", 403

    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)
    
    article.title = request.form.get('title')
    article.content = request.form.get('content')
    db.session.commit()

    return redirect('lab8/articles')

@lab8.route('/lab8/articles/<int:article_id>/delete', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.get_or_404(article_id)

    if article.login_id != current_user.id:
        return "У вас нет прав на удаление этой статьи", 403

    db.session.delete(article)
    db.session.commit()

    return redirect('/lab8/articles')


@lab8.route('/lab8/public_articles/')
def public_articles():
    # Получаем все публичные статьи
    public_articles = articles.query.filter_by(is_public=True).all()
    
    # Передаем статьи в шаблон
    return render_template('lab8/public_articles.html', articles=public_articles)

@lab8.route('/lab8/search/', methods=['GET'])
def search_articles():
    query = request.args.get('query')  # Получаем строку поиска из запроса

    # Поиск по статьям текущего пользователя и публичным статьям
    if current_user.is_authenticated:
        user_articles = articles.query.filter(
            (articles.login_id == current_user.id) | (articles.is_public == True)
        ).filter(
            (articles.title.contains(query)) | (articles.article_text.contains(query))
        ).all()
    else:
        user_articles = articles.query.filter_by(is_public=True).filter(
            (articles.title.contains(query)) | (articles.article_text.contains(query))
        ).all()

    return render_template('lab8/search_results.html', articles=user_articles, query=query)