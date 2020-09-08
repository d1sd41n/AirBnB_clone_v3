#!/usr/bin/python3
"""Api Cities."""
from flask import Flask, request, abort
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """get cities by state id."""
    query = storage.all(State)
    if "State.{}".format(state_id) not in query:
        abort(404)
    return jsonify([city.to_dict() for city in storage.get('State', state_id).cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """get city by id."""
    query = storage.all(City)
    if "City.{}".format(city_id) not in query:
        abort(404)
    city_ = storage.get("City", city_id)
    if city_ is None:
        abort(404)
    return jsonify(city_.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """delete city by id."""
    query = storage.all(City)
    if "City.{}".format(city_id) not in query:
        abort(404)
    storage.delete(query["City.{}".format(city_id)])
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """create a city in state by state id."""

    query = request.get_json()
    if query is None:
        abort(400, 'Not a JSON')
    if "name" not in query.keys():
        abort(400, 'Missing name')

    query2 = storage.all(State)
    if "State.{}".format(state_id) not in query2:
        abort(404)

    query["state_id"] = state_id
    city = City(**query)
    city.save()
    return (jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],strict_slashes=False)
def put_city(city_id):
    """update city."""
    query = storage.all(City)
    if "City.{}".format(city_id) not in query:
        abort(404)
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for i in request.json:
        if i not in ['id', 'created_at', 'updated_at']:
            setattr(city, i, request.json[i])
    city.save()
    return jsonify(city.to_dict())

