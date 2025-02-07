import pytest
from scooter_api.scooter_api import ApiClient

COURIER_DATA_SUCCESS = [{"courier_login": "av_konovalov_sprint_7_register_1",
                         "courier_password": "qwerty1234",
                         "courier_first_name": "Courier"}]


class TestRegisterCourier:
    client = ApiClient()
    COURIER_DATA_REGISTER_SUCCESS = [{"courier_login": "av_konovalov_sprint_7_register_1",
                                      "courier_password": "qwerty1234",
                                      "courier_first_name": "Courier"}]

    def setup_class(self):

        for courier_data in self.COURIER_DATA_REGISTER_SUCCESS:
            response = self.client.send_login_to_account_request(courier_login=courier_data["courier_login"],
                                                                 courier_password=courier_data["courier_password"])
            if response.status_code == self.client.LOGIN_SUCCESS_CODE:
                """Удалить аккаунт перед тестом"""
                courier_id = str(response.json()["id"])
                delete_resp = self.client.send_delete_courier_request(courier_id)
                assert delete_resp.status_code == self.client.DELETE_SUCCESS_CODE

    def teardown_class(self):
        self.setup_class(self)

    @pytest.mark.parametrize("courier_data", COURIER_DATA_REGISTER_SUCCESS)
    def test_register_new_courier_success(self, courier_data: dict[str, str]):
        """ Тест проверяет возможность успешного создания курьера
        :param courier_data: словарь, содержащий данные, необходимые для создания курьера (login, password, firstName)
        Ожидаемый статус-код: 201
        Ожидаемый ответ сервера: {"ok": True}
        """
        expected_status_code = 201
        expected_json = {"ok": True}

        response = self.client.send_register_new_courier_request(**courier_data)

        assert response.status_code == expected_status_code, (
            f"Ожидался статус-код {expected_status_code}, получен {response.status_code}"
        )
        assert response.json() == expected_json, (
            f"Ожидался ответ {expected_json}, получен {response.json()}"
        )


class TestLoginToAccount:
    client = ApiClient()
    COURIER_DATA_LOGIN_SUCCESS = [{"courier_login": "av_konovalov_sprint_7_login_1",
                                   "courier_password": "qwerty1234",
                                   "courier_first_name": "Courier"}]

    def setup_class(self):
        for courier_data in self.COURIER_DATA_LOGIN_SUCCESS:
            response = self.client.send_login_to_account_request(courier_login=courier_data["courier_login"],
                                                                 courier_password=courier_data["courier_password"])
            if response.status_code != self.client.LOGIN_SUCCESS_CODE:
                """Зарегистрировать аккаунт перед тестом"""
                register_resp = self.client.send_register_new_courier_request(**courier_data)
                assert register_resp.status_code == self.client.REGISTER_SUCCESS_CODE

    def teardown_class(self):
        for courier_data in self.COURIER_DATA_LOGIN_SUCCESS:
            response = self.client.send_login_to_account_request(courier_login=courier_data["courier_login"],
                                                                 courier_password=courier_data["courier_password"])
            if response.status_code == self.client.LOGIN_SUCCESS_CODE:
                """Удалить аккаунт перед тестом"""
                courier_id = str(response.json()["id"])
                delete_resp = self.client.send_delete_courier_request(courier_id)
                assert delete_resp.status_code == self.client.DELETE_SUCCESS_CODE

    @pytest.mark.parametrize("courier_data", COURIER_DATA_LOGIN_SUCCESS)
    def test_send_login_to_account_request_success(self, courier_data: dict[str, str]):
        """
        Тест проверяет возможность курьера успешно залогиниться.
        Ожидаемый статус-код: 201
        Ожидаемый ответ сервера: {"ok": True}
        :param courier_data: словарь, содержащий данные, необходимые чтобы залогинить курьера (login, password)
        """

        response = self.client.send_login_to_account_request(courier_login=courier_data["courier_login"],
                                                             courier_password=courier_data["courier_password"])

        assert response.status_code == self.client.LOGIN_SUCCESS_CODE, (
            f"Ожидался статус-код {self.client.LOGIN_SUCCESS_CODE}, получен {response.status_code}"
        )

        # Проверка структуры ответа
        response_json = response.json()
        assert "id" in response_json, "В ответе отсутствует ключ 'id'"

        # Проверка типа значения id (должно быть число)
        assert isinstance(response_json["id"], int), f"ID должен быть числом, получен {type(response_json['id'])}"


class TestDeleteCourier:
    client = ApiClient()
    COURIER_DATA_DELETE_SUCCESS = [{"courier_login": "av_konovalov_sprint_7_delete_1",
                                    "courier_password": "qwerty1234",
                                    "courier_first_name": "Courier"}]

    def setup_class(self):
        """
        Проверяем, что попытка залогиниться под тестовыми пользователями проходит успешно. Если нет, то регистрируем такого пользователя
        :return:
        """

        for courier_data in self.COURIER_DATA_DELETE_SUCCESS:
            login_response = self.client.send_login_to_account_request(courier_login=courier_data["courier_login"],
                                                                 courier_password=courier_data["courier_password"])
            if login_response.status_code != self.client.LOGIN_SUCCESS_CODE:
                register_response = self.client.send_register_new_courier_request(**courier_data)
                assert register_response.status_code == self.client.REGISTER_SUCCESS_CODE

    @pytest.mark.parametrize("courier_data", COURIER_DATA_DELETE_SUCCESS)
    def test_send_delete_courier_request_success(self, courier_data):
        """
        Тест проверяет возможность успешного удаления для ранее созданного аккаунта
        :return:
        """

        login_resp = self.client.send_login_to_account_request(courier_login=courier_data["courier_login"],
                                                               courier_password=courier_data["courier_password"])
        assert login_resp.status_code == self.client.LOGIN_SUCCESS_CODE, (
            f"Ожидался статус-код {self.client.LOGIN_SUCCESS_CODE}, получен {login_resp.status_code}"
        )
        courier_id = str(login_resp.json()["id"])
        print(f'courier_id: {courier_id}')
        delete_resp = self.client.send_delete_courier_request(courier_id)
        assert delete_resp.status_code == self.client.DELETE_SUCCESS_CODE
