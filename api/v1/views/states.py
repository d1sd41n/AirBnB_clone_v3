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

