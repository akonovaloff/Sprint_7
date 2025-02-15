import pytest
from scooter_api.scooter_api import ApiClient
from faker import Faker
from random import randint, choice


@pytest.fixture(scope='session')
def client():
    """
    Фикстура для работы с API
    """
    client = ApiClient()
    return client


@pytest.fixture()
def user_data(client):
    """
    Фикстура возвращает валидные данные для регистрации нового курьера.
    Если после теста курьер остаётся в системе, то фикстура его удаляет
    :param client: фикстура
    """
    print("Подготовка данных курьера:")
    faker = Faker()
    while True:
        # Генерируем данные курьера
        created_user = {"login": faker.email(),
                        "password": faker.password(10),
                        "first_name": faker.first_name()}

        login_resp = client.send_login_request(login=created_user["login"],
                                               password=created_user["password"])
        if login_resp.status_code == client.LOGIN_NOT_FOUND_CODE:
            break
    print(f"Курьер успешно создан")
    yield created_user

    # Если пользователь существует, то удалить его после теста
    print("Удаление курьера после теста:")
    login_resp = client.send_login_request(login=created_user["login"], password=created_user["password"])
    if login_resp.status_code == client.LOGIN_SUCCESS_CODE:
        created_user['id'] = str(login_resp.json()['id'])
        client.delete(created_user)
        print(f"Курьер удалён")
    else:
        print(f"Курьер не найден")


@pytest.fixture()
def registered_user(client, user_data):
    """
    Фикстура, которая возвращает курьера, зарегистрированного в системе
    :param client:
    :param user_data:
    :return:
    """
    client.register(user_data)
    user_data['id'] = client.login(user_data)
    return user_data


@pytest.fixture()
def order_data():
    fake = Faker("ru_RU")
    ordr_data = {"firstName": fake.first_name(),
                 "lastName": fake.last_name(),
                 "address": fake.address(),
                 "metroStation": str(randint(1, 20)),
                 "phone": fake.phone_number(),
                 "rentTime": str(randint(1, 8)),
                 "deliveryDate": fake.date_between(start_date='today', end_date='+7d').strftime('%Y-%m-%d'),
                 "comment": fake.sentence(),
                 "color": choice([[], ["BLACK"], ["GRAY"], ["BLACK", "GREY"], ["GREY", "BLACK"]])}
    return ordr_data
