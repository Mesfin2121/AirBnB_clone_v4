#!/usr/bin/python3
"""
route that returns json status response
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """ route that returns the status """
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def obj_status():
    """ retrieves the number of each objects by type """
    response = {}
    object_format = {
        'Amenity': 'amenities',
        'City': 'cities',
        'Place': 'places',
        'Review': 'reviews',
        'State': 'states',
        'User': 'users'
    }
    for key, value in object_format.items():
        response[value] = storage.count(key)
    return jsonify(response)
