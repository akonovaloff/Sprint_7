import requests


class ApiClient:
    BASE_API_URL = "https://qa-scooter.praktikum-services.ru/"
    LOGIN_COURIER_URL = BASE_API_URL + "/api/v1/courier/login"
    CREATE_COURIER_URL = BASE_API_URL + "api/v1/courier"
    DELETE_COURIER_URL = BASE_API_URL + "/api/v1/courier/"

    def send_register_new_courier_request(self,
                                          courier_login: str,
                                          courier_password: str,
                                          courier_first_name: str) -> requests.Response:
        """
        Создает курьера
        :param courier_login: Логин курьера
        :param courier_password: Пароль курьера
        :param courier_first_name: Имя курьера
        :return: Ответ сервера
        """
        courier_data = {
            "login": courier_login,
            "password": courier_password,
            "firstName": courier_first_name
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.CREATE_COURIER_URL, json=courier_data, headers=headers)
        return response

    def send_login_to_account_request(self,
                                      courier_login: str,
                                      courier_password: str) -> requests.Response:
        """
        Залогинить курьера
        :param courier_login: Логин курьера
        :param courier_password: Пароль курьера
        :return: Ответ сервера
        """
        courier_data = {
            "login": courier_login,
            "password": courier_password,
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.LOGIN_COURIER_URL, json=courier_data, headers=headers)
        return response

    def send_delete_courier_request(self, courier_id: str) -> requests.Response:
        """
        Удаляет курьера по его id
        :param courier_id:
        :return:
        """
        payload = {"id": courier_id}
        response = requests.delete(url=self.DELETE_COURIER_URL + courier_id, data=payload)
        return response
