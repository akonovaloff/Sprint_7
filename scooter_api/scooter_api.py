import requests
import json


class ApiClient:
    BASE_API_URL = "https://qa-scooter.praktikum-services.ru/"
    LOGIN_COURIER_URL = BASE_API_URL + "api/v1/courier/login"
    REGISTER_COURIER_URL = BASE_API_URL + "api/v1/courier"
    DELETE_COURIER_URL = BASE_API_URL + "api/v1/courier/"
    CREATE_ORDER_URL = BASE_API_URL + "api/v1/orders"

    LOGIN_SUCCESS_CODE = 200
    LOGIN_NOT_FOUND_CODE = 404
    LOGIN_UNFILLED_CODE = 400

    REGISTER_CONFLICT_CODE = 409
    REGISTER_UNFILLED_CODE = 400
    REGISTER_SUCCESS_CODE = 201

    DELETE_SUCCESS_CODE = 200
    DELETE_NOT_FOUND_CODE = 404

    CREATE_ORDER_SUCCESS_CODE = 201
    ORDERS_SUCCESS_CODE = 200

    @staticmethod
    def pretty_json(data: dict):
        return json.dumps(data, indent=4, ensure_ascii=False).encode('utf8').decode()

    def send_register_raw_data(self, payload) -> requests.Response:
        """
        Отправляет произвольные данные на ручку регистрации
        :param payload: словарь данных
        :return: ответ сервера
        """
        print(f"--> register.POST: {json.dumps(payload)}")
        response = requests.post(url=self.REGISTER_COURIER_URL, data=payload)
        print(f"<-- {response.json()}")
        return response

    def send_register_request(self, login: str, password: str, first_name: str) -> requests.Response:
        """
        Отправляет запрос на регистрацию курьера, возвращает ответ сервера

        :param login: Логин курьера
        :param password: Пароль курьера
        :param first_name: Имя курьера

        :return: Ответ сервера
        """
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        print(f"--> register.POST: {json.dumps(payload)}")
        response = requests.post(url=self.REGISTER_COURIER_URL, data=payload)
        print(f"<-- {response.json()}")
        return response

    def register(self, courier_data):
        """
        Отправляет запрос на регистрацию курьера; проверят, что сервер вернул успешный статус-код
        :param courier_data: Словарь с данными курьера (login, password, first_name)
        """
        resp = self.send_register_request(login=courier_data["login"],
                                          password=courier_data["password"],
                                          first_name=courier_data["first_name"])
        assert resp.status_code == self.REGISTER_SUCCESS_CODE, (
            f"Не удалось зарегистрировать пользователя: {courier_data["login"]}"
            f"\tОжидался статус-код {self.REGISTER_SUCCESS_CODE}, получен {resp.status_code}"
        )

    def send_login_request(self,
                           login: str,
                           password: str) -> requests.Response:
        """
        Отправляет запрос на регистрацию курьера, возвращает ответ сервера
        :param login: Логин курьера
        :param password: Пароль курьера
        :return: Ответ сервера
        """
        payload = {
            "login": login,
            "password": password,
        }
        headers = {"Content-Type": "application/json"}
        print(f"--> login.POST: {json.dumps(payload)}")
        response = requests.post(self.LOGIN_COURIER_URL, json=payload, headers=headers)
        print(f"<-- {response.json()}")
        return response

    def login(self, courier_data) -> str:
        """
        Отправляет запрос на вход курьера; проверяет, что сервер вернул успешный статус-код, возвращает id
        :param courier_data: Словарь с данными курьера (login, password, first_name)
        :return: идентификатор пользователя
        """
        resp = self.send_login_request(login=courier_data["login"],
                                       password=courier_data["password"])
        assert resp.status_code == self.LOGIN_SUCCESS_CODE, (
            f"Не удалось залогинить пользователя: {courier_data["login"]}"
            f"\tОжидался статус-код {self.REGISTER_SUCCESS_CODE}, получен {resp.status_code}"
        )
        # Проверяем, что в ответе есть ожидаемые данные
        assert "id" in resp.json(), (
            f"В ответе отсутствует ID созданного курьера.\n"
            f"Ответ сервера: {resp.text}"
        )
        return str(resp.json()["id"])

    def send_delete_request(self, courier_id: str) -> requests.Response:
        """
        Отправляет запрос на удаление курьера, возвращает ответ сервера
        :param courier_id: идентификатор, возвращаемый сервером при входе пользователя
        :return: Ответ сервера
        """
        payload = {"id": courier_id}
        print(f"--> delete_courier.DELETE: {json.dumps(payload)}")
        response = requests.delete(url=self.DELETE_COURIER_URL + courier_id, params=payload, data=payload)
        print(f"<-- {response.json()}")
        return response

    def send_delete_raw_data(self, payload):
        print(f"--> delete_courier.DELETE: {json.dumps(payload)}")
        response = requests.delete(url=self.DELETE_COURIER_URL, params=payload, data=payload)
        print(f"<-- {response.json()}")
        return response

    def delete(self, courier_data):
        """
        Логинит пользователя в системе, чтобы получить id; отправляет запрос на удаление курьера; проверяет, что сервер вернул успешный статус-код
        :param courier_data:
        :return:
        """
        if 'id' in courier_data.keys():
            courier_id = courier_data['id']
        else:
            courier_id = self.login(courier_data)
        del_resp = self.send_delete_request(courier_id)
        assert del_resp.status_code == self.DELETE_SUCCESS_CODE, (
            f"Не удалось удалить пользователя {courier_data["login"]}:"
            f"Ожидаемый статус-код: {self.DELETE_SUCCESS_CODE}, получен {del_resp.status_code}"
        )
        assert del_resp.json() == {'ok': True}, "Формат ответ сервера не совпадает с ожидаемым"

    def send_raw_data_to_create_order(self, payload):
        print(f"\n--> create_order.POST: {self.pretty_json(payload)}")
        resp = requests.post(self.CREATE_ORDER_URL, data=payload)
        print(f"<-- {resp.json()}")
        return resp

    def send_raw_data_to_get_orders_list(self, payload):
        print(f"\n--> get_orders.GET: {self.pretty_json(payload)}")
        resp = requests.get(self.CREATE_ORDER_URL, params=payload)
        print(f"<-- {self.pretty_json(resp.json())}")
        return resp
