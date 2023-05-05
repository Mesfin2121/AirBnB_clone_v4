#!/usr/bin/python3
"""
view for User object that handles all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def all_users():
    """ Retrieves the list of all User objects """
    response = []
    # all_object = storage.all('State')
    for value in storage.all('User').values():
        response.append(value.to_dict())
    return jsonify(response)


@app_views.route('/users/<user_id>', methods=['GET'])
def user_by_id(user_id):
    """ Retrieves a User object by id """
    response = storage.get('User', user_id)
    if response is not None:
        return jsonify(response.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ Deletes a User object by id """
    del_object = storage.get('User', user_id)
    if del_object is not None:
        del_object.delete()
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/users', methods=['POST'])
def create_user():
    """ Creates a User """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    # if data.get('name') is None:
    #     abort(400, 'Missing name')
    if data.get('email') is None:
        abort(400, 'Missing email')
    if data.get('password') is None:
        abort(400, 'Missing password')

    new_state_obj = User(**data)
    new_state_obj.save()
    return jsonify(new_state_obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """ Updates a User object by id """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    ignore = ['id', 'email', 'created_at', 'updated_at']
    update_object = storage.get('User', user_id)
    if update_object is not None:
        for key, value in data.items():
            if key not in ignore:
                setattr(update_object, key, value)
        storage.save()
        return jsonify(update_object.to_dict()), 200
    else:
        abort(404)
