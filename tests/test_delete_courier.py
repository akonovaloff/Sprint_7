from conftest import client, registered_user, user_data

class TestDeleteCourier:
    def test_delete_courier_success(self, client, registered_user):
        """
        Тест проверяет возможность удаления курьера
        :param client:
        :param registered_user:
        """
        client.delete(registered_user)