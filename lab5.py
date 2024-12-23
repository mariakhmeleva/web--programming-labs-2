from flask import Blueprint, render_template, request, make_response, redirect, session, current_app, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path
from dotenv import load_dotenv

lab5 = Blueprint('lab5', __name__)

load_dotenv()

@lab5.route('/lab5/')
def lab():
    username = 'Анонимус'
    return render_template('lab5/lab5.html', username=username, login=session.get('login'))

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='maria_khmeleva_knowledge_base_db',
            user='maria_khmeleva_knowledge_base_db',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        error = 'Заполните оба поля' if not login and not password else (
            'Заполните логин' if not login else 'Заполните пароль'
        )
        return render_template('lab5/register.html', error=error)

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))
    db_close(conn, cur)

    return render_template('lab5/succes.html', login=login)


@lab5.route('/lab5/success')
def success():
    login = request.args.get('login')
    return render_template('lab5/succes.html', login=login)


@lab5.route('/lab5/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        error = 'Заполните оба поля' if not login and not password else (
            'Заполните логин' if not login else 'Заполните пароль'
        )
        return render_template('lab5/login.html', error=error)

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')

    if not check_password_hash (user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')

    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/login_succes.html', login = login)


@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = bool(request.form.get('is_public'))

    if not title or not article_text:
        error = 'Заполните оба поля' if not title and not article_text else (
            'Заполните тему статьи' if not title else 'Заполните текст статьи'
        )
        return render_template('lab5/create_article.html', error=error)

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute(f"SELECT * FROM users WHERE login=?;", (login, ))

    user_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO articles (user_id, title, article_text, is_public) VALUES (%s, %s, %s, %s);",
                    (user_id, title, article_text, is_public))
    else:
        cur.execute(f"INSERT INTO articles (user_id, title, article_text, is_public) VALUES (?, ?, ?, ?);",
                    (user_id, title, article_text, is_public))

    db_close(conn, cur)
    return redirect('/lab5')


@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute(f"SELECT id FROM users WHERE login=?;", (login,))

    user_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE user_id=%s ORDER BY is_favorite DESC;", (user_id,))
    else:
        cur.execute(f"SELECT * FROM articles WHERE user_id=? ORDER BY is_favorite DESC;", (user_id,))

    articles = cur.fetchall()

    db_close(conn, cur)

    if not articles:
        no_articles_message = 'У вас пока нет ни одной статьи'
        return render_template('lab5/articles.html', no_articles_message=no_articles_message)

    return render_template('lab5/articles.html', articles=articles)


@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5/login')


@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute(f"SELECT * FROM articles WHERE id=?;", (article_id,))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return render_template('lab5/error.html', error="Статья не найдена.")

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute(f"SELECT * FROM users WHERE login=?;", (login,))

    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        is_public = bool(request.form.get('is_public'))

        if not title or not article_text:
            error = 'Заполните все поля для сохранения изменений.'
            return render_template('lab5/edit_articles.html', article=article, error=error)

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE articles SET title=%s, article_text=%s, is_public=%s WHERE id=%s;",
                        (title, article_text, is_public, article_id))
        else:
            cur.execute("UPDATE articles SET title=?, article_text=?, is_public=? WHERE id=?;",
                        (title, article_text, is_public, article_id))

        db_close(conn, cur)
        return redirect('/lab5/list')

    db_close(conn, cur)
    return render_template('lab5/edit_articles.html', article=article)


@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute(f"SELECT * FROM articles WHERE id=?;", (article_id,))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return render_template('lab5/error.html', error="Статья не найдена.")

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("DELETE FROM articles WHERE id=?;", (article_id,))

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/users')
def list_users():
    conn, cur = db_connect()
    cur.execute("SELECT login FROM users;")
    users = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/users.html', users=users)


@lab5.route('/lab5/favorite/<int:article_id>', methods=['POST'])
def favorite_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute(f"SELECT id FROM users WHERE login=?;", (login,))
    user_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND login_id=?;", (article_id, user_id))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return render_template('lab5/error.html', error="Статья не найдена или вы не можете её изменить.")

    new_favorite_status = not article['is_favorite']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET is_favorite=%s WHERE id=%s;", (new_favorite_status, article_id))
    else:
        cur.execute(f"UPDATE articles SET is_favorite=? WHERE id=?;", (new_favorite_status, article_id))

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/favorites')
def favorite_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute(f"SELECT id FROM users WHERE login=?;", (login,))
    user_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE user_id=%s AND is_favorite=TRUE;", (user_id,))
    else:
        cur.execute(f"SELECT * FROM articles WHERE user_id=? AND is_favorite=1;", (user_id,))

    favorite_articles = cur.fetchall()

    db_close(conn, cur)

    if not favorite_articles:
        no_favorites_message = 'У вас пока нет любимых статей.'
        return render_template('lab5/favorites.html', no_favorites_message=no_favorites_message)

    return render_template('lab5/favorites.html', articles=favorite_articles)


@lab5.route('/lab5/public_articles')
def public_articles():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT articles.*, users.login AS author FROM articles JOIN users ON articles.user_id = users.id WHERE is_public=TRUE;")
    else:
        cur.execute(f"SELECT articles.*, users.login AS author FROM articles JOIN users ON articles.user_id = users.id WHERE is_public=1;")

    public_articles = cur.fetchall()

    db_close(conn, cur)

    if not public_articles:
        no_public_articles_message = 'Нет публичных статей.'
        return render_template('lab5/public_articles.html', no_public_articles_message=no_public_articles_message)

    return render_template('lab5/public_articles.html', articles=public_articles)