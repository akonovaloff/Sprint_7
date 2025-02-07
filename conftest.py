import pytest
from scooter_api.scooter_api import ApiClient


@pytest.fixture(scope='session', autouse=True)
def client() -> ApiClient:
    return ApiClient()

@pytest.fixture()
def delete_courier_before_test(self, client):
    for courier_data in self.COURIER_DATA_REGISTER_SUCCESS:
        response = client.send_login_to_account_request(courier_login=courier_data["courier_login"],
                                                        courier_password=courier_data["courier_password"])
        if response.status_code == client.LOGIN_SUCCESS_CODE:
            """Удалить аккаунт перед тестом"""
            courier_id = str(response.json()["id"])
            delete_resp = client.send_delete_courier_request(courier_id)
            assert delete_resp.status_code == client.DELETE_SUCCESS_CODE