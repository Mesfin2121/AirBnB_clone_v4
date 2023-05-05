#!/usr/bin/python3
"""
view for Amenity objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def all_amenities():
    """ Retrieves the list of all Amenity objects """
    response = []
    # all_object = storage.all('State')
    for value in storage.all('Amenity').values():
        response.append(value.to_dict())
    return jsonify(response)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenity_by_id(amenity_id):
    """ Retrieves a Amenity object by id """
    response = storage.get('Amenity', amenity_id)
    if response is not None:
        return jsonify(response.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ Deletes a Amenity object by id """
    del_object = storage.get('Amenity', amenity_id)
    if del_object is not None:
        del_object.delete()
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """ Creates a Amenity """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    elif data.get('name') is None:
        abort(400, 'Missing name')
    new_state_obj = Amenity(**data)
    new_state_obj.save()
    return jsonify(new_state_obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """ Updates a Amenity object by id """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    elif data.get('name') is None:
        abort(400, 'Missing name')
    ignore = ['id', 'created_at', 'updated_at']
    update_object = storage.get('Amenity', amenity_id)
    if update_object is not None:
        for key, value in data.items():
            if key not in ignore:
                setattr(update_object, key, value)
        storage.save()
        return (jsonify(update_object.to_dict()))
    else:
        abort(404)
