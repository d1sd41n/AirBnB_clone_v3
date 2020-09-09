#!/usr/bin/python3
"""Api Cities."""
from flask import Flask, request, abort
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_cities(city_id):
    """get places by city id."""
    query = storage.all(City)
    if "City.{}".format(city_id) not in query:
        abort(404)
    return jsonify([place.to_dict() for place in
                   storage.get('City', city_id).places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """get city by id."""
    query = storage.all(Place)
    if "Place.{}".format(place_id) not in query:
        abort(404)
    place_ = storage.get('Place', place_id)
    if place_ is None:
        abort(404)
    return jsonify(place_.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """delete city by id."""
    query = storage.all(Place)
    if "Place.{}".format(place_id) not in query:
        abort(404)
    storage.delete(query["Place.{}".format(place_id)])
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """create a city in state by state id."""

    query = request.get_json()
    if query is None:
        abort(400, 'Not a JSON')
    if "name" not in query.keys():
        abort(400, 'Missing name')

    query2 = storage.all(City)
    if "Place.{}".format(city_id) not in query2:
        abort(404)

    query["city_id"] = city_id
    place = Place(**query)
    place.save()
    return (jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """update city."""
    query = storage.all(Place)
    if "Place.{}".format(place_id) not in query:
        abort(404)
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for i in request.json:
        if i not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, i, request.json[i])
    place.save()
    return jsonify(place.to_dict())
