import os
import psycopg2
from flask import Flask, Blueprint, make_response, jsonify, abort, request
from app.api.v1.models.data_models import NewUsers
from app.api.v1 import utils
import datetime
from flask_jwt import jwt




user_blueprint = Blueprint('users', __name__, url_prefix='/api/v1')

@user_blueprint.route('/', methods=['GET'])
def index():
    return make_response(jsonify({
        "Message":"Welcome Msomi",
        "status":200
    }), 200)

@user_blueprint.route('/auth/register', methods=['GET', 'POST'])
def add_user():

    try:
        data = request.get_json()
        fullname = data['fullname']
        username = data['username']
        email = data["email"]  
        password = data["password"]
    except:
         return abort(400, "error", "wrong input!!")

    newuser = NewUsers(fullname, username, email, password)
    newuser.create_new_user()

    return utils.res_method(201, "data", [{
        "user": {
            "email": newuser.email,
            "username": newuser.username
        },
        "token": newuser.password
    }])
@user_blueprint.route("/auth/login", methods=['POST'])
def user_login():
    try:
        data = request.get_json()
        request_email = data['email']
        password = data['password']

    except KeyError:
        abort(utils.res_method(400, "error", "Provide correct values for email & password"))

    utils.isEmailValid(request_email)
    try:
        user =NewUsers.get_user_by_mail(request_email)
        if not user:
            abort(utils.res_method(404, "error", "User does not exist"))

        hashed_password = user[0][2]
        req_email= request_email.strip()

        password = NewUsers.compare_password_hash_and_password(
            hashed_password, password)
        if not password:
            return make_response(jsonify({
            "message": "Try again. E-mail or password is incorrect!"
        }
        ), 403)

        token = jwt.encode({
                "email": req_email,
                
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=3000)
            }, os.getenv('JWT_SECRET_KEY', default='SdaHv342nx!jknr837bjwd?c,lsajjjhw673hdsbgeh'))
        return make_response(jsonify({
                            "message": "Login successful",
                            "token": token.decode("UTF-8"),
                           
                            }), 200)

        
    except psycopg2.DatabaseError as _error:
        abort(utils.res_method(500, "error", "Server error"))


