from flask import Flask, Blueprint, make_response, jsonify


user_blueprint = Blueprint('users', __name__, url_prefix='/api/v1')

@user_blueprint.route('/', methods=['GET'])
def index():
    return make_response(jsonify({
        "Message":"Welcome Msomi",
        "status":200
    }), 200)


