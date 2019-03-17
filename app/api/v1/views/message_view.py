from flask import Flask, make_response, jsonify, make_response, Blueprint, abort
from flask import request
from app.api.v1.models import message_model

message = message_model.Message()

message_blueprint = Blueprint('message',__name__,url_prefix='/api/v1')

@message_blueprint.route('send',methods=['POST'])
def send_message():
    """send a direct message"""

    try:
        data = request.get_json()
    except:
        abort(400,"an error occured")

    sent_message = message.create_message(data)

    return make_response(jsonify({
        "status":200,
        "data":sent_message
    }))

@message_blueprint.route('chat',methods=['GET'])
def fetch_messages():
    """fetch users' messages"""

    messages = message.fetch_messages()
    return make_response(jsonify({
        "status":200,
        "data":messages
    }))