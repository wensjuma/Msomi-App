import os 
import sys
from flask import Flask, request, abort
from flask_jwt import jwt
from datetime import datetime
from app.api.v1 import utils
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
    @staticmethod
    def get_single_user(user_id):
        select_user_query = """
        SELECT fullname, username, email FROM users
        WHERE users.id = '{}'""".format(user_id)
        return database.select_data_from_db(select_user_query)
    @staticmethod
    def format_user_data(iterable):
        user_data=[]
        for item in iterable:
             f_data={
                "fullname":item[0],
                "username":item[1],
                "email":item[2]
            }
        user_data.append(f_data)
        return user_data
    @staticmethod
    def sendmail(email):
        """
            This function is responsible for sending an email 
            to the address provided as a parameter so that the user
            concerned can receive a notification via mail on 
            how to update their password.
        """
        try:
            username = UserModel.get_user_by_mail(email)[0][1]
        except:
            abort(utils.res_method(404, "error",
                                    "You are not a registered user of the app"))
        token = jwt.encode({"email": email},
                           os.getenv('SECRET_KEY'), algorithm='HS256').decode('UTF-8')
        link = "https://127.0.0.1:5000/auth/reset?token={}".format(
            token)

        try:

            sg = sendgrid.SendGridAPIClient(
                apikey=os.environ.get('SENDGRID_API_KEY'))
            from_email = Email("admin-noreply@politico.com")
            to_email = Email(email)
            subject = "Password reset instructions"
            content = Content(
                "text/plain",
                "Hey {} click this link to go and reset your password {}".format(username, link))
            mail = Mail(from_email, subject, to_email, content)
            sg.client.mail.send.post(request_body=mail.get())
        except:
            print('Unknown error detected:')
            # Info about unknown error that caused exception.
            a = sys.exc_info()
            print('    ', a)
            b = [str(p) for p in a]
            print('    ', b)
            abort(utils.res_method(400, "error", "Something went wrong"))


class GroupDiscussions():
    def __init__(self, group_title, group_description):
        self.group_title= group_title
        self.description= group_description
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    @staticmethod
    def formatGroupData(iterable):
        """
            This function will help in formatting the groups data 
            in a record format
        """
        data = []
        for group in iterable:
            formattedgroup= {
                              'group_title': group[0],
                              'group_description': group[1]
            }  

            data.append(formattedgroup)
        return data
    def create_new_group(self):
        create_group_query="""
         INSERT INTO groups(group_title, group_description, created_on) VALUES('{}', {}', '{}')
         """.format(self.group_title, self.description, self.timestamp)

        database.add_data_to_db(create_group_query)
    @staticmethod
    def fetch_all_groups(): 
        query = """
        SELECT group_title, group_description FROM groups
        """
        return GroupDiscussions.formatGroupData(database.select_data_from_db(query))
    @staticmethod
    def fetch_specific_group_from_db(id): 
        query = """
        SELECT * FROM groups WHERE groups.group_id= '{}'
        """. format(id)
        return GroupDiscussions.formatGroupData(database.select_data_from_db(query))

    def delete_group(self, group_id):
        delete_group_query = """
        DELETE FROM groups WHERE group_id = '{}' 
        """.format(group_id)
        return database.select_data_from_db(delete_group_query)

    #=======Add members in a  group======
  
