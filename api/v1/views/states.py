#!/usr/bin/python3
"""Script that's gonna handle the states view for the API."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states():
    States = storage.all(State)
    dict_json = []
    for state in States.values():
        dict_json.append(state.to_dict())
    return jsonify(dict_json)


@app_views.route('/states/<state_id>', methods=["GET"])
def get_states_id(state_id):
    """Retrieving a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deleting a State object with id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()

    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def post_state():
    """Creating a State"""
    body = request.get_json()

    if body is None:
        abort(400, "Not a JSON")

    if "name" not in body:
        abort(400, "Missing name")

    state = State(**body)
    storage.new(state)
    storage.save()

    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """Updating the State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        request_htpp = request.get_json()
        if request_htpp is None:
            abort(400, 'Not a JSON')

    for key, value in request_htpp.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    storage.save()

    return jsonify(state.to_dict()), 200
