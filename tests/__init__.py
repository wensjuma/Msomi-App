import os 
import json
import unittest
from flask import Flask
from app import start_app

class TestUsers(unittest.TestCase):
    def setUp(self):
        self.app = start_app(os.getenv('FLASK_ENV'))
        self.client = self.app.test_client()
        self.app.testing = True

        self.USERS= {
            "id":1,
            "username":"wens",
            "email":"wens@gmail.com",
            "firstname":"wenslaus",
            "lastname":"juma",
            
        }
        return