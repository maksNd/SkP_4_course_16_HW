from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from utils import load_users, load_offers, load_orders, offer_serialize, order_serialize

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///from_16_HW.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.ensure_ascii = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    age = db.Column(db.Integer)
    email = db.Column(db.String(30))
    role = db.Column(db.String(15))
    phone = db.Column(db.String(15))


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(500))
    start_date = db.Column(db.String(30))
    end_date = db.Column(db.String(30))
    address = db.Column(db.String(100))
    price = db.Column(db.Float)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    customer = db.relationship('User', foreign_keys=[customer_id])
    executor = db.relationship('User', foreign_keys=[executor_id])


class Offer(db.Model):
    __tablename__ = 'offer'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    order = db.relationship('Order')
    executor = db.relationship('User')


db.drop_all()
db.create_all()
users = [User(**row) for row in load_users()]
order = [Order(**row) for row in load_orders()]
offer = [Offer(**row) for row in load_offers()]

with db.session.begin():
    db.session.add_all(users)
    db.session.add_all(order)
    db.session.add_all(offer)


@app.get('/')
def response_page():
    return '<div style="background-color:black;color:white;padding:700px;">' \
           '<centre><h1>Сейчас вы на главной страничке, для того что бы перейти на нужную вкладку, необходимо ' \
           'ввести в адресной строке соответствующий запрос!</h1><centre>' \
           '</div>'


@app.get('/orders/')
def all_orders_page():
    """Выводит все данные из orders.json в json формате"""

    orders = Order.query.all()
    return jsonify([order_serialize(row) for row in orders])


@app.get('/orders/<int:uid>/')
def get_orders_uid(uid):
    """Выводит один 'заказ' в json формате"""

    orders = Order.query.get(uid)
    if not orders:
        return abort(404)

    return jsonify(order_serialize(orders))


@app.get('/offers/')
def all_offers_page():
    """Выводит все данные из offers.json в json формате"""

    offers = Offer.query.all()
    return jsonify([offer_serialize(row) for row in offers])


@app.get('/offers/<int:uid>/')
def get_offer_uid(uid):
    """Выводит одно 'предложение' в json формате"""

    offers = Offer.query.get(uid)
    if not offers:
        return abort(404)

    return jsonify(offer_serialize(offers))


###################################################################################

# -------------------- From Users: Post, Put, Delete ---------------------------- #

###################################################################################


###################################################################################

# -------------------- From Order: Post, Put, Delete ---------------------------- #

###################################################################################


@app.post('/orders/')
def create_new_order():
    """
    Добавляет заказ в таблицу orders.
    Заполнение происходит через json с помощью метода POST
    """

    query = request.json
    order = Order(
        name=query.get('name'),
        description=query.get('description'),
        start_date=query.get('start_date'),
        end_date=query.get('end_date'),
        address=query.get('address'),
        price=query.get('price'),
        customer_id=query.get('customer_id'),
        executor_id=query.get('executor_id')
    )
    db.session.add(order)
    db.session.commit()
    return jsonify(order_serialize(order))


@app.put('/orders/<int:uid>/')
def changes_order_info(uid):
    """
    Получает конкретный заказ по его id.
    Обновляет данные о заказе в таблице данными из json,
    с помощью метода PUT.
    """

    order = Order.query.get(uid)
    if not order:
        return abort(404)

    query = request.json

    order.name = query.get('name')
    order.description = query.get('description')
    order.start_date = query.get('start_date')
    order.end_date = query.get('end_date')
    order.address = query.get('address')
    order.price = query.get('price')
    order.customer_id = query.get('customer_id')
    order.executor_id = query.get('executor_id')

    db.session.add(order)
    db.session.commit()

    return jsonify(order_serialize(order))


@app.delete('/orders/<int:uid>/')
def delete_order(uid):
    """
    Получает заказ по его id.
    Удаляет информацию о нём.
    """

    order = Order.query.get(uid)
    if not order:
        return abort(404)

    db.session.delete(order)
    db.session.commit()
    return jsonify({'Attention !': f'Order into {uid} removed'})


###################################################################################

# -------------------- From Offer: Post, Put, Delete ---------------------------- #

###################################################################################


@app.post('/offers/')
def create_new_offer():
    """
    Добавляет предложение в таблицу offers.
    Заполнение происходит через json с помощью метода POST
    """

    query = request.json
    offer = Offer(
        order_id=query.get('order_id'),
        executor_id=query.get('executor_id')
    )
    db.session.add(offer)
    db.session.commit()
    return jsonify(offer_serialize(offer))


@app.put('/offers/<int:uid>/')
def change_offer_info(uid):
    """
    Получает конкретное предложение по его id.
    Обновляет данные о предложении в таблице данными из json,
    с помощью метода PUT.
    """

    offer = Offer.query.get(uid)
    if not offer:
        return abort(404)

    query = request.json

    offer.order_id = query.get('order_id')
    offer.executor_id = query.get('executor_id')

    db.session.add(offer)
    db.session.commit()

    return jsonify(offer_serialize(offer))


@app.delete('/offers/<int:uid>/')
def delete_offer(uid):
    """
    Получает пользователя по его id.
    Удаляет информацию о нём.
    """

    offer = Offer.query.get(uid)
    if not offer:
        return abort(404)

    db.session.delete(offer)
    db.session.commit()
    return jsonify({'Attention !': f'Offer into {uid} removed'})


@app.errorhandler(404)
def page_400_error(error):
    """ Обработчик ошибок на стороне сервера"""

    return jsonify({"Error": 'Information Not Found'}), 404

#
# if __name__ == '__main__':
#     app.run(debug=True)
