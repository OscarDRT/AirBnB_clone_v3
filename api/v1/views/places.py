#!/usr/bin/python3
"""Documentation"""
from flask import Flask, jsonify, abort, make_response, request
from api.v1.views import app_views
from models.city import City
from models import storage
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def places_li(city_id):
    """Places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        places_list = []

        for key, value in storage.all('Place').items():
            if value.city_id == str(city_id):
                places_list.append(value.to_dict())
        return jsonify(places_list)

    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return (jsonify({"error": "Not a JSON"}), 400)
        if 'user_id' not in data:
            return (jsonify({"error": "Missing user_id"}), 400)
        if storage.get(User, data['user_id']) is None:
            abort(404)
        if 'name' not in data:
            return (jsonify({"error": "Missing name"}), 400)
        if storage.get(User, data['user_id']) is None:
            abort(404)
        data['city_id'] = city_id
        place = Place(**data)
        place.save()
        return make_response(jsonify(place.to_dict()), 201)

@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def my_places(place_id):
    """places"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return (jsonify({"error": "Not a JSON"}), 400)
        ignorekey = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignorekey:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
