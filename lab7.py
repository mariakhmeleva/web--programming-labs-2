from flask import Blueprint, render_template, request, abort, jsonify
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

films = [
    {
        "title": "Inception",
        "title_ru": "Начало",
        "year": 2010,
        "description": "Кобб – талантливый вор, лучший из лучших в опасном искусстве извлечения: он крадет ценные секреты из глубин подсознания во время сна, когда человеческий разум наиболее уязвим. Редкие способности Кобба сделали его ценным игроком в привычном к предательству мире промышленного шпионажа, но они же превратили его в извечного беглеца и лишили всего, что он когда-либо любил."
    },
    {
        "title": "Green Book",
        "title_ru": "Зеленая книга",
        "year": 2018,
        "description": "1960-е годы. После закрытия нью-йоркского ночного клуба на ремонт вышибала Тони по прозвищу Болтун ищет подработку на пару месяцев. Как раз в это время Дон Ширли — утонченный светский лев, богатый и талантливый чернокожий музыкант, исполняющий классическую музыку — собирается в турне по южным штатам, где ещё сильны расистские убеждения и царит сегрегация. Он нанимает Тони в качестве водителя, телохранителя и человека, способного решать текущие проблемы. У этих двоих так мало общего, и эта поездка навсегда изменит жизнь обоих."
    },
    {
        "title": "Pulp Fiction",
        "title_ru": "Криминальное чтиво",
        "year": 1994,
        "description": "Двое бандитов Винсент Вега и Джулс Винфилд ведут философские беседы в перерывах между разборками и решением проблем с должниками криминального босса Марселласа Уоллеса. В первой истории Винсент проводит незабываемый вечер с женой Марселласа Мией. Во второй Марселлас покупает боксёра Бутча Кулиджа, чтобы тот сдал бой. В третьей истории Винсент и Джулс по нелепой случайности попадают в неприятности."
    },
    {
        "title": "Schindler's List",
        "title_ru": "Список Шиндлера",
        "year": 1993,
        "description": "Фильм рассказывает реальную историю загадочного Оскара Шиндлера, члена нацистской партии, преуспевающего фабриканта, спасшего во время Второй мировой войны почти 1200 евреев."
    }
]

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < len(films):
        return jsonify(films[id])
    else:
        abort(404, description="Film not found")

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < len(films):
        del films[id]
        return '', 204
    else:
        abort(404, description="Film not found")

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < len(films):
        film = request.get_json()
        errors = validate_film(film)
        if errors:
            return jsonify(errors), 400
        films[id] = film
        return jsonify(films[id])
    else:
        abort(404, description="Film not found")

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    new_film = request.get_json()
    errors = validate_film(new_film)
    if errors:
        return jsonify(errors), 400
    films.append(new_film)
    return jsonify({'id': len(films) - 1}), 201

def validate_film(film):
    errors = {}
    current_year = datetime.now().year

    if not film.get('title') and not film.get('title_ru'):
        errors['title'] = 'Название на оригинальном языке или русское название должно быть заполнено'

    if not film.get('title_ru'):
        errors['title_ru'] = 'Русское название должно быть заполнено'

    if not (1895 <= int(film.get('year', 0))):
        errors['year'] = f'Год должен быть от 1895 до {current_year}'

    if not film.get('description'):
        errors['description'] = 'Описание должно быть заполнено'
    elif len(film.get('description', '')) > 2000:
        errors['description'] = 'Описание должно быть не более 2000 символов'

    return errors