import json
from global_variables import ORDERS_PATH, OFFERS_PATH, USERS_PATH


def load_json(filename: str) -> list[dict]:
    """Возвращает по filename выбранный json с данными"""

    with open(filename, encoding='utf-8') as file:
        return json.load(file)


def load_users() -> list[dict]:
    """Возвращает users_json с данными"""

    return load_json(USERS_PATH)


def load_offers() -> list[dict]:
    """Возвращает offers_json с данными"""

    return load_json(OFFERS_PATH)


def load_orders() -> list[dict]:
    """Возвращает orders_json с данными"""

    return load_json(ORDERS_PATH)


def user_serialize(user_info) -> dict:
    """Serialize implementation"""

    return {
        "id": user_info.id,
        "first_name": user_info.first_name,
        "last_name": user_info.last_name,
        "age": user_info.age,
        "email": user_info.email,
        "role": user_info.role,
        "phone": user_info.phone
    }


def order_serialize(order_info) -> dict:
    """Serialize implementation"""

    return {
        "id": order_info.id,
        "name": order_info.name,
        "description": order_info.description,
        "start_date": order_info.start_date,
        "end_date": order_info.end_date,
        "address": order_info.address,
        "price": order_info.price,
        "customer_id": order_info.customer_id,
        "executor_id": order_info.executor_id
    }


def offer_serialize(offer_info) -> dict:
    """Serialize implementation"""

    return {
        "id": offer_info.id,
        "order_id": offer_info.order_id,
        "executor_id": offer_info.executor_id
    }
