from flask import Flask, jsonify, make_response, abort, request
import re
import os
from functools import wraps
from app.api.v1 import database
from app.api.v1.database import select_data_from_db
from flask_jwt import jwt


KEY = os.getenv('SECRET_KEY')

"""
consists of utilities required by 
different files in v2 of this app
"""

def validate_ints(data):
    """
    Method to validate data of type integer
    :params: data
    :response: True, False
    """
    if not isinstance(data, int):
        return False
    return True

def validate_string(data):
    """
    Method to validate data of type string
    :params: user input
    :response: True, False 
    """
    if not isinstance(data, str):
        return False
    return True

def check_field_is_not_empty(input_data):

    if input_data == "":
        return False

def PasswordsMatch(first_pass, sec_pass):
    """
        this function checks if the passwords.
    """
    if(first_pass!= sec_pass):
        abort(res_method(400, "error", "passwords dont match"))
    return True


def is_phone_number_valid(phone):
    """
        This checks if a number phone number is valid
    """
    if not re.match('^[0-9]*$', phone):
        abort(res_method(400, "Error", "Phone number should be integers only"))


def isEmailValid(email):
    """
        this function checks if the email is valid
        via regex
    """
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        abort(res_method(400, "error", "email is invalid"))
    return True


def check_matching_items_in_db_table(params, table_name):
    """
        check if a value of key provided is 
        available in the database table
        if there's a duplicate then the test fails
    """
    for key, value in params.items():
        query = """
        SELECT {} from {} WHERE {}.{} = '{}'
        """.format(key, table_name, table_name, key, value)
        duplicated = select_data_from_db(query)
        if duplicated:
            abort(res_method(409, "error",
                              "Error. '{}' '{}' is already in use".format(key, value)))


def token_required(f):
    """
        Checks for token in the request header
    """
    
def verify_tokens():
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
    if not token:
        abort(make_response(jsonify({
                                "Message": "You need to login"}), 401))

    query = """SELECT token FROM auth WHERE  token = '{}'""".format(token)
    blacklisted = database.select_data_from_db(query)
    if blacklisted:
        abort(make_response(jsonify({
                        "Message": "Kindly login again"}), 401))
    try:
        data = jwt.decode(token, os.getenv('JWT_SECRET_KEY', default='SdaHv342nx!jknr837bjwd?c,lsajjjhw673hdsbgeh'))
        return data["email"], data["user_id"]

    except:
        abort(make_response(jsonify({
            "Message": "The token is either expired or wrong"
        }), 403))   

def res_method(status,key, message):
    dict ={
        "status":status
    }
    dict[key]=message
    return make_response(jsonify(dict), status)

        
# def retrieve_all_data(model, type):
#     if(type=="questions"):
#         return model.retrieve_all_questions()
#     elif(type=="data"):
#         return model.retrieve_all_data()
#     return []
# def retrieve_specific_data(model, type, id):
#     if(type=="questions"):
#         return model.retrieve_questions(id)
#     elif (type=="data"):
#         return model.retrieve_data(id)
#     return []


def sanitize_input(input_data):
    """check if input is of alphanumeric characters"""
    if input_data.isalpha() == False:
        return False

def validate_string_data_type(data_passed):
    """ensures the input passed is of str type."""
    if not isinstance(data_passed, str):
        return False
    return True

def return_error(status_code, message):
    """ function to format the response """
    response = {
        "status": status_code,
        "error": message,
    }
    return make_response(jsonify(response), status_code)
def return_response(status_code, message, data=list()):
    """ function to format the response """
    response = {
        "status": status_code,
        "message": message,
        "data": data,
    }
    return make_response(jsonify(response), status_code)



