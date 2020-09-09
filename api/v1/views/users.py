#!/usr/bin/python3
"""Api States """
from flask import Flask, request, abort
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """get states"""
    return jsonify([users.to_dict() for users in storage.all('User').values()])

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """save a state"""
    query = request.get_json()
    if query is None:
        abort(400, 'Not a JSON')
    if "name" not in query.keys():
        abort(400, 'Missing name')
    user = User(**query)
    user.save()
    return (jsonify(user.to_dict()), 201)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """get state"""
    query = storage.all(User)
    if "User.{}".format(user_id) not in query:
        abort(404)
    user_ = storage.get("User", user_id)
    if user_ is None:
        abort(404)
    return jsonify(user_.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """delete state"""
    query = storage.all(User)
    if "User.{}".format(user_id) not in query:
        abort(404)
    storage.delete(query["User.{}".format(user_id)])
    storage.save()
    return jsonify({})

@app_views.route('/users/<user_id>', methods=['PUT'],strict_slashes=False)
def put_user(user_id):
    """update state"""
    query = storage.all(User)
    if "User.{}".format(user_id) not in query:
        abort(404)
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for i in request.json:
        if i not in ['id', 'created_at', 'updated_at']:
            setattr(user, i, request.json[i])
    user.save()
    return jsonify(user.to_dict())

