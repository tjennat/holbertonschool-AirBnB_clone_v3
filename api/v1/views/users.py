#!/usr/bin/python3
"""Script that's gonna handle Users view for the API."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_users():
    """Retrieving the list of all User objects"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=["GET"])
def get_user(user_id):
    """Retrieving a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deleting a User object with id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()

    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creating a new User"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """Updating a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        request_http = request.get_json()
        if request_http is None:
            abort(400, 'Not a JSON')

    for key, value in request_http.items():
        if key not in ['id', 'email', 'created_at', 'updated_at', 'password']:
            setattr(user, key, value)

    storage.save()

    return jsonify(user.to_dict()), 200
