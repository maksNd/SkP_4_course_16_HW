from main import app

user_keys = {'id', 'first_name', 'last_name', 'age', 'email', 'role', 'phone'}
order_keys = {'id', 'name', 'description', 'start_date', 'end_date',
              'address', 'price', 'customer_id', 'executor_id'}
offers_keys = {'id', 'order_id', 'executor_id'}


class TestApi:

    def test_element_keys_from_user(self):
        response = app.test_client().get('/users/')
        assert len(response.json[0]) == len(user_keys), 'Ошибка в количестве ключей'
        assert set(response.json[0]) == user_keys, 'Ошибка в названии ключей'

    def test_element_keys_from_orders(self):
        response = app.test_client().get('/orders/')
        assert len(response.json[0]) == len(order_keys), 'Ошибка в количестве ключей'
        assert set(response.json[0]) == order_keys, 'Ошибка в названии ключей'

    def test_element_keys_from_offers(self):
        response = app.test_client().get('/offers/')
        assert len(response.json[0]) == len(offers_keys), 'Ошибка в количестве ключей'
        assert set(response.json[0]) == offers_keys, 'Ошибка в названии ключей'

    def test_page_from_users(self):
        response = app.test_client().get('/users/')
        assert response.status_code == 200, 404
        assert type(response.json) == list, 'Это не список'

    def test_page_from_orders(self):
        response = app.test_client().get('/orders/')
        assert response.status_code == 200, 404
        assert type(response.json) == list, 'Это не список'

    def test_page_from_offers(self):
        response = app.test_client().get('/offers/')
        assert response.status_code == 200, 404
        assert type(response.json) == list, 'Это не список'

    def test_page_from_one_user(self):
        response = app.test_client().get('/users/1/')
        assert response.status_code == 200, 404
        assert type(response.json) == dict, 'Это не список'

    def test_page_from_one_order(self):
        response = app.test_client().get('/orders/1/')
        assert response.status_code == 200, 404
        assert type(response.json) == dict, 'Это не список'

    def test_page_from_one_offer(self):
        response = app.test_client().get('/offers/1/')
        assert response.status_code == 200, 404
        assert type(response.json) == dict, 'Это не список'

    def test_not_found_page(self):
        response = app.test_client().get('/qwerty/')
        assert response.status_code == 404

    def test_page_not_found_user(self):
        response = app.test_client().get('/users/444', follow_redirects=True)
        assert response.status_code == 404

    def test_page_not_found_order(self):
        response = app.test_client().get('/orders/444', follow_redirects=True)
        assert response.status_code == 404

    def test_page_not_found_offer(self):
        response = app.test_client().get('/offers/444', follow_redirects=True)
        assert response.status_code == 404
