#!/usr/bin/python3
"""Api States """
from flask import Flask, request, abort
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """get amenities."""
    return jsonify([amenity.to_dict() for amenity in
                   storage.all(Amenity).values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """get amenity by id."""
    query = storage.all(Amenity)
    if "Amenity.{}".format(amenity_id) not in query:
        abort(404)
    amenity_ = storage.get("Amenity", amenity_id)
    if amenity_ is None:
        abort(404)
    return jsonify(amenity_.to_dict())


@app_views.route('/amenity/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete amenity."""
    query = storage.all(Amenity)
    if "Amenity.{}".format(amenity_id) not in query:
        abort(404)
    storage.delete(query["Amenity.{}".format(amenity_id)])
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenities():
    """Creates an Amenity object."""
    query = request.get_json()
    if query is None:
        abort(400, 'Not a JSON')
    if "name" not in query.keys():
        abort(400, 'Missing name')
    amenity = Amenity(**query)
    amenity.save()
    return (jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """update Amenity object."""
    query = storage.all(Amenity)
    if "Amenity.{}".format(amenity_id) not in query:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for i in request.json:
        if i not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, i, request.json[i])
    amenity.save()
    return jsonify(amenity.to_dict())
