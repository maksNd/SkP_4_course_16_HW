from flask import Blueprint, abort, jsonify, request
from utils import user_serialize
from main import User, db

bp_users = Blueprint('bp_users', __name__)


@bp_users.get('/users/')
def all_users_page():
    """Выводит все данные из users.json в json формате"""

    user = User.query.all()
    return jsonify([user_serialize(row) for row in user])


@bp_users.get('/users/<int:uid>/')
def get_user_uid(uid):
    """Выводит одного пользователя в формате json"""

    user = User.query.get(uid)
    if not user:
        return abort(404)
    return jsonify(user_serialize(user))


@bp_users.post('/users/')
def create_new_user():
    """
    Добавляет пользователя в таблицу users.
    Заполнение происходит через json с помощью метода POST
    """

    data = request.json
    user = User(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        age=data.get('age'),
        email=data.get('email'),
        role=data.get('role'),
        phone=data.get('phone')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user_serialize(user))


@bp_users.put('/users/<int:uid>/')
def changes_user_info(uid):
    """
    Получает конкретно пользователя по его id.
    Обновляет данные о пользователе в таблице данными из json,
    с помощью метода PUT.
    """

    user = User.query.get(uid)
    if not user:
        return abort(404)

    query = request.json

    user.first_name = query.get('first_name')
    user.last_name = query.get('last_name')
    user.age = query.get('age')
    user.email = query.get('email')
    user.role = query.get('role')
    user.phone = query.get('phone')

    db.session.add(user)
    db.session.commit()
    return jsonify(user_serialize(user))


@bp_users.delete('/users/<int:uid>/')
def delete_user(uid):
    """
    Получает пользователя по его id.
    Удаляет информацию о нём.
    """

    user = User.query.get(uid)
    if not user:
        return abort(404)

    db.session.delete(user)
    db.session.commit()
    return jsonify({'Attention !': f'User into {uid} removed'})
