#!/usr/bin/python3
"""Documentation"""
from flask import Flask, jsonify, abort, make_response, request
from api.v1.views import app_views
from models.state import *
from models import storage


@app_views.route('/states/', methods=['POST', 'GET'], strict_slashes=False)
def states():
    """Methods to State"""
    if request.method == 'GET':
        all_states = storage.all(State)
        states_list = []
        for key, value in all_states.items():
            states_list.append(value.to_dict())
        return jsonify(states_list)

    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return (jsonify({"error": "Not a JSON"}), 400)
        if 'name' in data:
            state = State(**data)
            state.save()
            data2 = storage.get(State, state.id).to_dict()
            return make_response(jsonify(data2), 201)
        return (jsonify({"error": "Missing name"}), 400)


@app_views.route('/states/<state_id>', methods=['DELETE', 'GET', 'PUT'],
                 strict_slashes=False)
def state(state_id):
    """Methods to State"""
    if request.method == 'GET':
        try:
            state = storage.get(State, state_id).to_dict()
            return jsonify(state)
        except:
            abort(404)

    if request.method == 'DELETE':
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return (jsonify({"error": "Not a JSON"}), 400)
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        ignorekey = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignorekey:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
