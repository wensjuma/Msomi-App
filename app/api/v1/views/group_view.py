import os
import psycopg2
from flask import Flask, Blueprint, make_response, jsonify, abort, request
from app.api.v1.models.data_models import GroupDiscussions, AddMembers
from app.api.v1 import utils
from app.api.v1 import database
from app.api.v1.utils import token_required

group_blueprint= Blueprint('group', __name__, url_prefix='/api/v1/groups')

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
            "Group Added":new_group.group_title
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
#not yet done 
@group_blueprint.route('/updategroup', methods=['PUT'])
def edit_group():
    try:
        data = request_json()
        title =data['group_title']
        desc= data['group_description']
    except:
      return utils.res_method(400, "error", "Something went wrong")
    
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
#should pick members in a users table on adding member to a group
@group_blueprint.route('/addmembers', methods=['POST'])
def add_members():
    
    try:
        data=request.get_json()
        email= data['email']
        group_name= data['group_name']
        
    except KeyError:
        return utils.res_method(400, "error", "Wrong data format!!")
    utils.check_existing_item_in_table({"email": email}, "users")
    utils.check_existing_item_in_table({"group_title": group_name}, "groups")
    utils.check_matching_items_in_db_table({"group_name":group_name}, "members")
    newmember = AddMembers(email, group_name)
    newmember.add_members_in_group()
    
    return utils.res_method(201, "data",[{
        "Messsage": "Member Added to {} group".format(group_name)
    }])

