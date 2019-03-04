import os
import psycopg2
from flask import Flask, Blueprint, make_response, jsonify, abort, request
from app.api.v1.models.data_models import GroupDiscussions
from app.api.v1 import utils


group_blueprints= Blueprint('group', __name__, url_prefix='/api/v1/auth')
@group_blueprints.route('/newgroup', methods=['POST'])
def create_groups():
    try:
        data= request.get_json()
        group_title= data['group_title']
        group_description= data['group_description']

    except:
        return abort(400, "error", "Wrong input for groups!")

    new_group= GroupDiscussions(group_title, group_description)
    new_group.create_new_group()

    return utils.res_method(201,"data", [{
        "group":{
            "group_title":new_group.group_title
        }
    }])
