import pytest
from conftest import client, user_data, registered_user


class TestCreateCourier:
    def test_create_courier_success(self, client, user_data):
        """
        Тест проверяет статус-код и формат ответа сервера при успешном создании курьера
        """

        # Отправляем запрос на регистрацию
        resp = client.send_register_request(**user_data)

        # Поверяем статус-код ответа
        assert resp.status_code == client.REGISTER_SUCCESS_CODE, (
            f"Не удалось зарегистрировать пользователя: {user_data["login"]}"
            f"\tОжидался статус-код {client.REGISTER_SUCCESS_CODE}, получен {resp.status_code}"
            f"\tОтвет сервера: {resp.text}"
        )

        # Проверяем, формат ответа
        assert resp.json() == {'ok': True}, f"Ответ сервера не совпадает с ожидаемым"

    def test_creating_duplicates_of_courier_is_prohibited(self, client, registered_user):
        """
        Тест проверяет статус-код и формат ответа сервера при создании дубликатов курьера
        """
        # Логинимся, чтобы проверить, что пользователь создан и получить его id
        src_id = registered_user['id']

        # Отправляем запрос на повторную регистрацию пользователя
        resp = client.send_register_request(login=registered_user['login'],
                                            password=registered_user['password'],
                                            first_name=registered_user['first_name'])

        # Поверяем статус-код ответа
        assert resp.status_code == client.REGISTER_CONFLICT_CODE, (
            f"Возникла проблема при дублировании пользователя: {registered_user["login"]}"
            f"\tОжидался статус-код {client.REGISTER_SUCCESS_CODE}, получен {resp.status_code}"
            f"\tОтвет сервера: {resp.text}"
        )

    @pytest.mark.parametrize("required_field", ["login", "password", "firstName"])
    def test_creating_courier_without_required_fields(self, client, user_data, required_field):
        """
        Тест проверяет статус-код и формат ответа сервера при создании дубликатов курьера
        """
        # Создаём копию данных пользователя, чтобы не потерять исходные данные
        user = user_data.copy()
        # Переименовать ключ "first_name" в "firstName"
        user["firstName"] = user.pop("first_name")
        # Удаляем одно из обязательных полей
        del user[required_field]

        # Отправляем запрос на регистрацию с изменёнными данными
        resp = client.send_register_raw_data(user)

        # Поверяем статус-код ответа
        assert resp.status_code in (client.REGISTER_UNFILLED_CODE, 504), (
            f'Удалось создать пользователя без обязательного поля "{required_field}"\n'
            f"\tДанные пользователя: {user}\n"
            f"\tОжидался статус-код {client.REGISTER_UNFILLED_CODE} или 504, получен {resp.status_code}\n"
            f"\tОтвет сервера: {resp.text}\n"
        )

        # Проверяем, формат ответа
        assert resp.json()['message'] == 'Недостаточно данных для создания учетной записи'
