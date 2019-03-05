from flask import Flask
from datetime import datetime
from .. import database
from werkzeug.security import generate_password_hash, check_password_hash

class NewUsers():
    def __init__(self, fullname, username, email, password):
        self.fullname= fullname
        self.username=username
        self.email=email
        self.password=self.encrypt_password(password)


    def create_new_user(self):
        """Query to insert new user"""
        add_new_user="""
        INSERT INTO users(fullname, username, email, password) VALUES('{}', '{}', '{}', '{}')
        """.format(self.fullname, self.username, self.email, self.password)
        database.add_data_to_db(add_new_user)
        
    def encrypt_password(self, password):
        hashed_password=generate_password_hash(str(password))
        return hashed_password

    @staticmethod
    def compare_password_hash_and_password(password_hash, password):
        return check_password_hash(password_hash, str(password))
    @staticmethod
    def get_user_by_mail(email):
        select_user_by_email = """
        SELECT id, username, password FROM users
        WHERE users.email = '{}'""".format(email)

        return database.select_data_from_db(select_user_by_email)
class GroupDiscussions():
    def __init__(self, group_title, group_description):
        self.group_title= group_title
        self.description= group_description

    def create_new_group(self):
        create_group_query="""
         INSERT INTO groups(group_title, group_description) VALUES('{}', '{}')
         """.format(self.group_title, self.description)

        database.add_data_to_db(create_group_query)

    def fetch_all_groups(self):
        
        query = """SELECT * FROM groups"""
        return database.select_data_from_db(query)
  
    def delete_group(self, group_id):
        delete_group_query = """DELETE FROM groups WHERE id = '{}' """.format(group_id)
        return database.select_data_from_db(delete_group_query)
