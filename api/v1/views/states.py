#!/usr/bin/python3
"""
view for State objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def all_states():
    """ Retrieves the list of all State object """
    response = []
    # all_object = storage.all('State')
    for value in storage.all('State').values():
        response.append(value.to_dict())
    return jsonify(response)


@app_views.route('/states/<state_id>', methods=['GET'])
def state_by_id(state_id):
    """ Retrieves a State object by id """
    response = storage.get('State', state_id)
    if response is not None:
        return jsonify(response.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a State object by id """
    del_object = storage.get('State', state_id)
    if del_object is not None:
        del_object.delete()
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states', methods=['POST'])
def create_state():
    """ Creates a State """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    elif data.get('name') is None:
        abort(400, 'Missing name')

    new_state_obj = State(**data)
    new_state_obj.save()
    return jsonify(new_state_obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ Updates a State object by id """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    elif data.get('name') is None:
        abort(400, 'Missing name')

    update_object = storage.get('State', state_id)
    if update_object is not None:
        update_object.name = data.get('name')
        storage.save()
        return (jsonify(update_object.to_dict()))
    else:
        abort(404)
