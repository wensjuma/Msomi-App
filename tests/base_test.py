import os
import unittest

from app import start_app
from instance.config import config


class TestBaseClass(unittest.TestCase):
    """
    Test class
    """

    def setUp(self):
        """
        instantiate the testbase class
        """
        self.app = start_app(os.getenv('FLASK_ENV'))
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app_test_client = self.app.test_client()
        self.app.testing = True


    
    def tearDown(self):
        """
        stop the tests after completion
        """
        self.app_context.pop()
    

if __name__ == '__main__':
    unittest.main()