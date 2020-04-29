#!/usr/bin/python3
"""Documentation"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models.state import *
from models.city import *
from models.amenity import *
from models import storage


@app_views.route('/amenities', methods=['GET', 'POST'],
                 strict_slashes=False)
def amenities_list():

    if request.method == 'GET':
        all_amenities = storage.all(Amenity)
        amenities = []
        for key, value in all_amenities.items():
            amenities.append(value.to_dict())
        return jsonify(amenities)

    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return (jsonify({"error": "Not a JSON"}), 400)
        if 'name' in data:
            amenity = Amenity(**data)
            amenity.save()
            data2 = storage.get(Amenity, amenity.id).to_dict()
            return jsonify(data2), 201
        return (jsonify({"error": "Missing name"}), 400)


@app_views.route('amenities/<amenity_id>', methods=['DELETE', 'GET', 'PUT'],
                 strict_slashes=False)
def amenity(amenity_id):
    """Methods to Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if request.method == 'GET':
        return(amenity.to_dict())

    if request.method == 'DELETE':
        storage.delete(Amenity)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return (jsonify({"error": "Not a JSON"}), 400)
        ignorekey = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignorekey:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
