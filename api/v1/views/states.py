#!/usr/bin/python3
"""Api States """
from flask import Flask, request, abort
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """get states"""
    return jsonify([state.to_dict() for state in storage.all(State).values()])


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """save a state"""
    query = request.get_json()
    if query is None:
        abort(400, 'Not a JSON')
    if "name" not in query.keys():
        abort(400, 'Missing name')
    state = State(**query)
    state.save()
    return (jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """get state"""
    query = storage.all(State)
    if "State.{}".format(state_id) not in query:
        abort(404)
    state_ = storage.get("State", state_id)
    if state_ is None:
        abort(404)
    return jsonify(state_.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """delete state"""
    query = storage.all(State)
    if "State.{}".format(state_id) not in query:
        abort(404)
    storage.delete(query["State.{}".format(state_id)])
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """update state"""
    query = storage.all(State)
    if "State.{}".format(state_id) not in query:
        abort(404)
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for i in request.json:
        if i not in ['id', 'created_at', 'updated_at']:
            setattr(state, i, request.json[i])
    state.save()
    return jsonify(state.to_dict())
