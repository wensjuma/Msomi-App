from flask import Flask, Blueprint, make_response, jsonify, abort, request
from app.api.v1.models import profile_model

# an instance of the user_model
user = profile_model.Profile()

profile_blueprint = Blueprint('user', __name__, url_prefix='/api/v1')

@profile_blueprint.route('/', methods=['GET'])
def index():
    return make_response(jsonify({
        "Message":"Welcome Msomi",
        "status":200
    }), 200)

@profile_blueprint.route('profile', methods = ['POST'])
def create_profile():
    """ Create a user profile """
    try:
        data = request.get_json()
    except:
        abort(400, "An error occured")
    created_user = user.create_profile(data)
    return make_response(jsonify({
        "status":200,
        "data":created_user
    }))

@profile_blueprint.route('profile/<int:user_id>',methods = ['PATCH'])
def update_profile(user_id):
    """ Update an existing user profile """
    try:
        data = request.get_json()
    except:
        abort(400,"An error occurred")
    updated_user = user.update_profile(user_id, data)
    return make_response(jsonify({
        "status":200,
        "data":updated_user
    }))

@profile_blueprint.route('profile',methods = ['GET'])
def get_profiles():
    profiles = user.get_profiles()
    return make_response(jsonify({
        "status":200,
        "data":profiles
    }))

@profile_blueprint.route('profile/<int:user_id>',methods = ['GET'])
def get_specific_profile(user_id):
    profile = user.get_specific_profile(user_id)
    if profile:
        return make_response(jsonify({
            "status":200,
            "data":profile
        }))
    return make_response(jsonify({
        "status":404, 
        "error":"No Such User, kindly, Try again"
    }))

@profile_blueprint.route('profile/<int:user_id>',methods = ['DELETE'])
def delete_profile(user_id):
    profile = user.delete_profile(user_id)
    if profile:
        return make_response(jsonify({
            "status":200,
            "data":profile
        }))
    return make_response(jsonify({
        "status":400, 
        "error":"Something Went wrong"
    }))

