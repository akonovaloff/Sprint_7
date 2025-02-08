from conftest import client, registered_user, user_data
import requests


class TestDeleteCourier:
    def test_delete_courier_success(self, client, registered_user):
        """
        Тест проверяет возможность удаления курьера
        :param client: Фикстура
        :param registered_user: Фикстура
        """
        client.delete(registered_user)

    def test_delete_courier_twice(self, client, registered_user):
        """
        Тест проверяет, что сервер вернёт ошибку, если удалить не существующего пользователя
        :param client: Фикстура
        :param registered_user: Фикстура
        """
        # Логиним курьера, чтобы получить его id
        courier_id = client.login(registered_user)
        # Удаляем курьера
        client.delete(registered_user)
        # Отправляем запрос на удаление не существующего пользователя
        resp = client.send_delete_request(courier_id)
        assert resp.status_code == client.DELETE_NOT_FOUND_CODE, "Статус-код не совпадает с ожидаемым"
        assert resp.json()["message"] == "Курьера с таким id нет.", "Формат ответа не совпадает с ожидаемым"

    def test_delete_courier_without_id(self, client, registered_user):
        courier_id = client.login(registered_user)
        response = requests.delete(url=client.DELETE_COURIER_URL, data={"id": courier_id})
        print(f"<-- {response.json()}")
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для удаления курьера"
