#!/usr/bin/python3
"""
view for City objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def city_by_state(state_id):
    """ Retrieves the list of all City objects of a State """
    all_states = storage.get('State', state_id)
    if all_states is None:
        abort(404)

    response = []
    all_cities = storage.all('City')
    for city in all_cities.values():
        if city.state_id == state_id:
            response.append(city.to_dict())
    return jsonify(response)


@app_views.route('/cities/<city_id>', methods=['GET'])
def city_by_id(city_id):
    """ Retrieves a City object by id """
    response = storage.get('City', city_id)
    if response is not None:
        return jsonify(response.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ Deletes a City object by id """
    del_object = storage.get('City', city_id)
    if del_object is not None:
        del_object.delete()
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """ Creates a City that linked with state """
    state = storage.get('State', state_id)
    data = request.get_json()
    if state is None:
        abort(404)
    if data is None:
        abort(400, 'Not a JSON')
    elif data.get('name') is None:
        abort(400, 'Missing name')
    data['state_id'] = state_id
    new_state_obj = City(**data)
    new_state_obj.save()
    return jsonify(new_state_obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """ Updates a City object by id """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    elif data.get('name') is None:
        abort(400, 'Missing name')

    update_object = storage.get('City', city_id)
    if update_object is not None:
        update_object.name = data.get('name')
        storage.save()
        return (jsonify(update_object.to_dict()))
    else:
        abort(404)
