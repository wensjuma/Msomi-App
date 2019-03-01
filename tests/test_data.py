from tests import TestUsers
class TestUserData(TestUsers):
    def test_users(self):
        response= self.client.post('api/v1/users')
        return