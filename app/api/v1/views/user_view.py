import os
import json
import psycopg2
from flask import Flask, Blueprint, make_response, jsonify, abort, request
from app.api.v1.models.data_models import NewUsers
from app.api.v1 import utils
import datetime
from flask_jwt import jwt
user_blueprint= Blueprint('users', __name__, url_prefix='/api/v1/auth')

@user_blueprint.route('/', methods=['GET'])
def index():
    return make_response(jsonify({
        "Message":"Welcome Msomi",
        "status":200
    }), 200)

@user_blueprint.route('/register', methods=['GET', 'POST'])
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
@user_blueprint.route('/login', methods=['POST'])
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

@user_blueprint.route('/users/<int:user_id>', methods=['GET'])
def fetch_user_by_id(user_id):
    
    fetched= NewUsers.get_single_user(user_id)
    data_fetched= NewUsers.format_user_data(fetched)
    if data_fetched:
        return utils.res_method(200, "data", data_fetched)
    return utils.res_method(404, "error", "User not found!")
# can be easily consumed When the UI is implemented
@user_blueprint.route("/reset", methods=["POST"])
def reset_password():
    try:
        data = request.get_json()
        email = data["email"]
    except KeyError:
        abort(utils.res_method(400, "error", "Should be email"))
    #checking email validity
    utils.isEmailValid(email)
    link = "https://127.0.0.1/5000/api/v1/auth/securereset"

    # send a request to the endpoint that will send the mail
    request.post(
        link, data=json.dumps({"email": email}),
        headers={'Content-Type': 'application/json'}
    )
    return utils.res_method(200, "data", [{
        "message": "Check your email for password reset link",
        "email": email
    }])

# send the email securely from server
@user_blueprint.route("/auth/securereset", methods=["POST"])
def secure_reset():
    """
        this endpoint is to be requested 
        from the server only via the 
        /auth/reset view. Client browsers accessing this view will
        be forbidden and hence the mail will not be sent
        view https://sendgrid.com/docs/for-developers/sending-email/cors/
        for more details on the reasons this implementation is necessary
    """
    try:
        data = request.get_json()
        email = data["email"]
    except KeyError:
        abort(utils.res_method(400, "error", "Should be email"))
    # check if email is valid
    utils.isEmailValid(email)
    NewUsers.sendmail(email)
    return utils.res_method(200, "data", [{
        "message": "Check your email for password reset link",
        "email": email
    }])
