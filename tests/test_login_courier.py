import pytest
import requests
from conftest import client, user_data, registered_user


class TestLoginCourier:
    def test_login_success(self, client, registered_user):
        """
        Тест проверяет, что зарегистрированный пользователь может успешно залогиниться
        :param client: фикстура
        :param registered_user: фикстура
        """
        log_resp = client.send_login_request(login=registered_user["login"],
                                             password=registered_user["password"])
        assert log_resp.status_code == client.LOGIN_SUCCESS_CODE, (
            f"Не удалось залогинить пользователя: {registered_user["login"]}\n"
            f"\tОтвет сервера: {log_resp.text}"
        )
        assert "id" in log_resp.json(), f"Ответ сервера не содержит id: {log_resp.json()}"

    @pytest.mark.parametrize("required_field", ("login", "password"))
    def test_login_without_required_fields(self, client, registered_user, required_field):
        """
        Тест проверяет невозможность залогиниться без обязательных полей в запросе
        :param client: фикстура
        :param registered_user: фикстура
        :param required_field: список обязательных полей
        """
        # Создаём копию данных пользователя, чтобы не потерять исходные данные
        payload = registered_user.copy()
        # Удаляем из запроса необязательно поле "first_name"
        del payload["first_name"]
        # Удаляем из запроса обязательное поле
        del payload[required_field]
        # Отправляем запрос
        headers = {"Content-Type": "application/json"}
        response = requests.post(client.LOGIN_COURIER_URL, json=payload, headers=headers)
        assert response.status_code in (client.LOGIN_UNFILLED_CODE, 504), (
            f"Удалось залогинить пользователя без обязательного поля {required_field}\nЗапрос: {payload}\n"
        )

    def test_login_with_not_registered_user(self, client, user_data):
        """
        Тест проверяет, что нельзя войти под незарегистрированным пользователем
        :param client: фикстура
        :param user_data: фикстура
        """
        resp = client.send_login_request(login=user_data["login"],
                                         password=user_data["password"])
        assert resp.status_code == client.LOGIN_NOT_FOUND_CODE

    @pytest.mark.parametrize("empty_fields", [["login"], ["password"], ["login", "password"]])
    def test_login_with_empty_data(self, registered_user, client, empty_fields):
        """
        Тест проверяет, что сервер вернёт ошибку, если логинить пользователя с пустым логином и/или паролем
        :param registered_user: фикстура
        :param client: фикстура
        """
        user = registered_user.copy()
        del user["first_name"]
        for key in empty_fields:
            user[key] = []
        resp = client.send_login_request(login=user['login'],
                                         password=user['password'])
        assert resp.status_code == client.LOGIN_NOT_FOUND_CODE

    def test_login_with_unmatched_password(self, registered_user, client):
        """
        Тест проверят, что нельзя залогинить курьера по неправильному паролю
        :param registered_user: фикстура
        :param client: фикстура
        """
        user = registered_user.copy()
        del user["first_name"]
        user["password"] = user["password"][0:-1]
        resp = client.send_login_request(login=user['login'],
                                         password=user['password'])
        assert resp.status_code == client.LOGIN_NOT_FOUND_CODE
