#!/usr/bin/python3
"""Documentation"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models.user import *
from models import storage


@app_views.route('/users', methods=['GET', 'POST'],
                 strict_slashes=False)
def users():
    """all users"""
    if request.method == 'GET':
        all_users = storage.all(User)
        users_list = []
        for key, value in all_users.items():
            users_list.append(value.to_dict())
        return jsonify(users_list)

    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return (jsonify({"error": "Not a JSON"}), 400)
        if 'email' not in data:
            return (jsonify({"error": "Missing email"}), 400)
        if 'password' not in data:
            return (jsonify({"error": "Missing password"}), 400)
        user = User(**data)
        user.save()
        return make_response(jsonify(user.to_dict()), 201)


@app_views.route('users/<user_id>', methods=['DELETE', 'GET', 'PUT'],
                 strict_slashes=False)
def user(user_id):
    """user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return (jsonify({"error": "Not a JSON"}), 400)
        ignorekey = ['id', 'created_at', 'updated_at', 'email']
        for key, value in data.items():
            if key not in ignorekey:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
