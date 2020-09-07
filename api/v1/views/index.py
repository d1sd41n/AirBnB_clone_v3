#!/usr/bin/python3
"""indxex doc"""
from api.v1.views import app_views
from models import storage
from flask import Flask, Blueprint, jsonify
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.amenity import Amenity


@app_views.route('/status', strict_slashes=False)
def status():
    """status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """stats"""
    counter = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
        }
    return jsonify(**counter)
