from flask import current_app
from . import base_test

class TestApp(base_test.TestBaseClass):


    def test_server_startup(self):
        
        response = self.app_test_client.get('/')

        self.assertEqual(response.status_code, 404)
