#!/usr/bin/python3
"""States"""
from flask import Flask, jsonify, abort, make_response, request
from api.v1.views import app_views
from models.state import *
from models import storage
from base_model import *


@app_views.route('/states/', methods=['POST', 'GET'])
def states():
    """states"""
    if request.method == 'GET':
        all_states = storage.all(State)
        states_list = []
        for key, value in all_states.items():
            states_list.append(value.to_dict())
        return jsonify(states_list)

    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return make_response(jsonify({'error': 'Not a Json'}), 400)
        elif 'name' in data:
            state = State(**data)
            state.save()
            return make_response(jsonify(data), 201)
        return make_response(jsonify({'error': 'Missing name'}), 400)


@app_views.route('/states/<state_id>', methods=['DELETE', 'GET', 'PUT'])
def state(state_id):
    """states"""
    state = storage.get(State, state_id)
    if request.method == 'GET':
        if state is None:
            abort(404)
        return jsonify(state.to_dict())

    if request.method == 'DELETE':
        if state is None:
            abort(404)
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a Json'}), 400)
        if state is None:
            abort(404)
        data = request.get_json()
        ignorekey = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignorekey:
                setattr(state, key, value)
        state.save()
        return make_response(jsonify(state.to_dict()), 200)
