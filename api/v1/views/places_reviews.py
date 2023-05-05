#!/usr/bin/python3
"""
view for Review object that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def review_by_place(place_id):
    """ Retrieves the list of all Review objects of a Place """
    response = []
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    for review in place.reviews:
        response.append(review.to_dict())
    return jsonify(response)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def review_by_id(review_id):
    """ Retrieves a Review object by id """
    response = storage.get('Review', review_id)
    if response is not None:
        return jsonify(response.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ Deletes a Review object by id """
    del_object = storage.get('Review', review_id)
    if del_object is not None:
        del_object.delete()
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """ Creates a Review """
    place = storage.get('Place', place_id)
    data = request.get_json()
    if place is None:
        abort(404)
    if data is None:
        abort(400, 'Not a JSON')
    if data.get('text') is None:
        abort(400, 'Missing text')
    if data.get('user_id') is None:
        abort(400, 'Missing user_id')

    user = storage.get('User', data['user_id'])
    if user is None:
        abort(404)
    data['place_id'] = place_id
    new_state_obj = Review(**data)
    new_state_obj.save()
    return jsonify(new_state_obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """ Updates a Review object by id """
    update_object = storage.get('Review', review_id)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    if update_object is not None:
        for key, value in data.items():
            if key not in ignore:
                setattr(update_object, key, value)
        storage.save()
        return jsonify(update_object.to_dict()), 200
    else:
        abort(404)
