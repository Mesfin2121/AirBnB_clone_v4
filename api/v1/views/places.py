#!/usr/bin/python3
"""
view for Place objects that handles all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def place_by_city(city_id):
    """ Retrieves the list of all Place objects of a City """
    response = []
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    for value in city.places:
        response.append(value.to_dict())
    return jsonify(response)


@app_views.route('/places/<place_id>', methods=['GET'])
def place_by_id(place_id):
    """ Retrieves a Place object by id """
    response = storage.get('Place', place_id)
    if response is not None:
        return jsonify(response.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_places(place_id):
    """ Deletes a Place object by id """
    del_object = storage.get('Place', place_id)
    if del_object is not None:
        del_object.delete()
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """ Creates a Place """
    city = storage.get('City', city_id)
    data = request.get_json()
    if city is None:
        abort(404)
    if data is None:
        abort(400, 'Not a JSON')
    if data.get('name') is None:
        abort(400, 'Missing name')
    if data.get('user_id') is None:
        abort(400, 'Missing user_id')

    user = storage.get('User', data['user_id'])
    if user is None:
        abort(404)
    data['city_id'] = city_id
    new_state_obj = Place(**data)
    new_state_obj.save()
    return jsonify(new_state_obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """ Updates a Place object by id """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    update_object = storage.get('Place', place_id)
    if update_object is not None:
        for key, value in data.items():
            if key not in ignore:
                setattr(update_object, key, value)
        storage.save()
        return jsonify(update_object.to_dict()), 200
    else:
        abort(404)
