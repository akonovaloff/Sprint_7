import pytest

from conftest import order_data, client


class TestCreateOrder:
    def test_create_order_success(self, order_data, client):
        order_resp = client.send_raw_data_to_create_order(order_data)
        assert order_resp.status_code == client.CREATE_ORDER_SUCCESS_CODE, "Код ответа сервера не совпадает с ожидаемым"
        assert "track" in order_resp.json(), 'В ответе сервера отсутствует обязательное поле "track"'

    @pytest.mark.parametrize("colors_array", [[], ["BLACK"], ["GRAY"], ["BLACK", "GREY"], ["GREY", "BLACK"]])
    def test_create_order_by_color(self, order_data, client, colors_array):
        order_data["color"] = colors_array
        order_resp = client.send_raw_data_to_create_order(order_data)
        assert order_resp.status_code == client.CREATE_ORDER_SUCCESS_CODE, f"Код ответа сервера не совпадает с ожидаемым. Выбранный цвет: {colors_array}"
        assert "track" in order_resp.json(), 'В ответе сервера отсутствует обязательное поле "track"'

    @pytest.mark.parametrize("query", [{"limit": "10", "page": "0"}])
    def test_get_orders(self, client, query):
        resp = client.send_raw_data_to_get_orders_list(query)
        assert resp.status_code == client.ORDERS_SUCCESS_CODE, "Статус-код "
        assert "orders" in resp.json(), 'В ответе сервера отсутствует обязательное поле "orders"'
        assert len(resp.json()["orders"]) >= int(query["limit"]), "Число заказов в ответе превышает запрошенное"