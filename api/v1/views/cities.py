#!/usr/bin/python3
"""Documentation"""
from flask import Flask, jsonify, abort, make_response, request
from api.v1.views import app_views
from models.state import *
from models.city import *
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'], strict_slashes=False)
def cities_li(state_id):
    """cities"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        cities_list = []

        for key, value in storage.all('City').items():
            if value.state_id == str(state_id):
                cities_list.append(value.to_dict())
        return jsonify(cities_list)

    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return (jsonify({"error": "Not a JSON"}), 400)
        if 'name' in data:
            data['state_id'] = state_id
            city = City(**data)
            city.save()
            data2 = storage.get(City, city.id).to_dict()
            return make_response(jsonify(data2), 201)
        return (jsonify({"error": "Missing name"}), 400)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def my_city(city_id):
    """city"""
    city = storage.get(City, city_id)
    if city is None:
            abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())
    
    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return (jsonify({"error": "Not a JSON"}), 400)
        ignorekey = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignorekey:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200