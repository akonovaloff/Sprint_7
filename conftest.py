import pytest
from scooter_api.scooter_api import ApiClient
from faker import Faker

@pytest.fixture(scope='session', autouse=True)
def client():
    client = ApiClient()
    return client

@pytest.fixture
def test_user():
    faker = Faker()
    created_user = {"login": faker.email(),
            "password": faker.password(10),
            "first_name": faker.first_name()}
    yield created_user

@pytest.fixture
def registered_user(client, test_user):
    client.register(test_user)
    yield test_user
    client.delete(test_user)