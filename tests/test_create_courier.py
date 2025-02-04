import pytest
from scooter_api import ApiClient

COURIER_DATA_SUCCESS = [{"courier_login": "av_konovalov_sprint_7_register_1",
                         "courier_password": "qwerty1234",
                         "courier_first_name": "Courier"}]


class TestCreateCourier:

    @pytest.mark.parametrize("courier_data", COURIER_DATA_SUCCESS)
    def test_register_new_courier_success(self, courier_data: dict[str, str]):
        """ Тест проверяет возможность успешного создания курьера
        :param courier_data: словарь, содержащий данные, необходимые для создания курьера (login, password, firstName)
        Ожидаемый статус-код: 201
        Ожидаемый ответ сервера: {"ok": True}
        """
        expected_status_code = 201
        expected_json = {"ok": True}

        client = ApiClient()
        response = client.send_register_new_courier_request(**courier_data)

        assert response.status_code == expected_status_code, (
            f"Ожидался статус-код {expected_status_code}, получен {response.status_code}"
        )
        assert response.json() == expected_json, (
            f"Ожидался ответ {expected_json}, получен {response.json()}"
        )


class TestLoginToAccount:
    @pytest.mark.parametrize("courier_data", COURIER_DATA_SUCCESS)
    def test_send_login_to_account_request_success(self, courier_data: dict[str, str]):
        """
        Тест проверяет возможность курьера успешно залогиниться.
        Ожидаемый статус-код: 201
        Ожидаемый ответ сервера: {"ok": True}
        :param courier_data: словарь, содержащий данные, необходимые чтобы залогинить курьера (login, password)
        """
        expected_status_code = 200

        client = ApiClient()
        response = client.send_login_to_account_request(courier_login=courier_data["courier_login"],
                                                        courier_password=courier_data["courier_password"])

        assert response.status_code == expected_status_code, (
            f"Ожидался статус-код {expected_status_code}, получен {response.status_code}"
        )

        # Проверка структуры ответа
        response_json = response.json()
        assert "id" in response_json, "В ответе отсутствует ключ 'id'"

        # Проверка типа значения id (должно быть число)
        assert isinstance(response_json["id"], int), f"ID должен быть числом, получен {type(response_json['id'])}"


class TestDeleteCourier:
    @pytest.mark.parametrize("courier_data", COURIER_DATA_SUCCESS)
    def test_send_delete_courier_request_success(self, courier_data):
        """
        Тест проверяет возможность успешного удаления для ранее созданного аккаунта
        :return:
        """
        client = ApiClient()
        login_resp = client.send_login_to_account_request(courier_login=courier_data["courier_login"],
                                                          courier_password=courier_data["courier_password"])
        assert login_resp.status_code == 200, (
            f"Ожидался статус-код 200, получен {login_resp.status_code}"
        )
        courier_id = str(login_resp.json()["id"])
        delete_resp = client.send_delete_courier_request(courier_id)
        assert delete_resp.status_code == 200
