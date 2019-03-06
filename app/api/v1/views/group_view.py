import os
import psycopg2
from flask import Flask, Blueprint, make_response, jsonify, abort, request
from app.api.v1.models.data_models import GroupDiscussions
from app.api.v1 import utils
from app.api.v1 import database
from app.api.v1.utils import token_required

group_blueprint= Blueprint('group', __name__, url_prefix='/api/v1')

@group_blueprint.route('/newgroup', methods=['POST'])
@token_required
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
@group_blueprint.route('/fetchgroups', methods=['GET'])
@token_required
def get_all_groups():
    group_data= GroupDiscussions.fetch_all_groups()   
    if group_data:
        return utils.res_method(200, "data", group_data)
    return utils.res_method(404, "error", "No groups available")

@group_blueprint.route('/fetchgroup/<int:group_id>', methods=['GET'])
def fetch_specific_group(group_id):
    group_data= GroupDiscussions.fetch_specific_group_from_db(group_id)   
    if group_data:
        return utils.res_method(200, "data", group_data)
    return utils.res_method(404, "error", "Specified group couldn't be found!!")

@group_blueprint.route('/newgroup', methods=['PUT'])
def edit_group():
    return 

@group_blueprint.route('/delete/<int:id>', methods=['DELETE'])
def delete_group(id):
    query = """
    SELECT * FROM groups WHERE id = {}
    """.format(id)
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
