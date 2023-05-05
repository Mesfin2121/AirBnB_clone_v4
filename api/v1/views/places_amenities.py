#!/usr/bin/python3
"""
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.amenity import Amenity
import os


db_type = os.getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def amenity_by_place(place_id):
    """  """
    response = []
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if db_type == "db":
        amenities = place.amenities
    else:
        amenities = place.amenity_ids
    for value in amenities:
        response.append(value.to_dict())
    return jsonify(response)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """  """
    place = storage.get('Place', place_id)
    amenity = storage.get('Amenity', amenity_id)
    if place is None:
        abort(404)
    if amenity is None:
        abort(404)
    if db_type == "db":
        amenities = place.amenities
    else:
        amenities = place.amenity_ids
    amenities.remove(amenity)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'])
def post_place_amenity(place_id, amenity_id):
    """  """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if db_type == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity in place_amenities:
        return jsonify(amenity.to_dict())
    place_amenities.append(amenity)
    place.save()
    return (jsonify(amenity.to_dict()), 201)
