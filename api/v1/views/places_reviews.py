#!/usr/bin/python3
"""Documentation"""
from flask import Flask, jsonify, abort, make_response, request
from api.v1.views import app_views
from models.city import City
from models import storage
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def reviews(place_id):
    """all reviews"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        all_reviews = []
        for key, value in storage.all(Review).items():
            all_reviews.append(value.to_dict())
        return jsonify(all_reviews)

    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return (jsonify({"error": "Not a JSON"}), 400)
        if 'user_id' not in data:
            return (jsonify({"error": "Missing user_id"}), 400)
        if storage.get(User, data['user_id']) is None:
            abort(404)
        if 'text' not in data:
            return (jsonify({"error": "Missing text"}), 400)
        data['place_id'] = place_id
        review = Review(**data)
        review.save()
        return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def review(review_id):
    """review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return (jsonify({"error": "Not a JSON"}), 400)
        ignorekey = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignorekey:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
