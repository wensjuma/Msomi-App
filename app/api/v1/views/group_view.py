import os
import psycopg2
from flask import Flask, Blueprint, make_response, jsonify, abort, request
from app.api.v1.models.data_models import GroupDiscussions
from app.api.v1 import utils
from app.api.v1 import database


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
@group_blueprints.route('/newgroup', methods=['PUT'])
def edit_group():
    return 

@group_blueprints.route('/delete/<int:id>', methods=['DELETE'])
def delete_group(id):
    query = """SELECT * FROM groups WHERE id = {}""".format(id)
    group = database.select_data_from_db(query)
        
    if not group:
            return make_response(jsonify({
            "message": "group with id {} does not exist".format(id)
            }), 404)

    group = group.GroupDiscussions(id=id)
    group.delete()

    return make_response(jsonify({
            "message": "Group deleted successfully"
        }), 200)
