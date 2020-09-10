#!/usr/bin/python3
"""Api Cities."""
from flask import Flask, request, abort
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place_id(place_id):
    """get reviews by place_id."""
    query = storage.all(Place)
    if "Place.{}".format(place_id) not in query:
        abort(404)
    return jsonify([review.to_dict() for review in
                   storage.get('Place', place_id).reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """get review by id."""
    query = storage.all(Review)
    if "Review.{}".format(review_id) not in query:
        abort(404)
    review_ = storage.get("Review", review_id)
    if review_ is None:
        abort(404)
    return jsonify(review_.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """delete review by id."""
    query = storage.all(Review)
    if "Review.{}".format(review_id) not in query:
        abort(404)
    storage.delete(query["Review.{}".format(review_id)])
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """create a review in place by place id."""

    query = request.get_json()
    if query is None:
        abort(400, 'Not a JSON')
    if "user_id" not in query.keys():
        abort(400, 'Missing user_id')
    if "text" not in query.keys():
        abort(400, 'Missing text')

    # query3 = storage.all(User)
    # if "User.{}".format(query["user_id"]) not in query3:
    #     abort(404)
    query3 = storage.get('User', query['user_id'])
    if query3 is None:
        abort(404)
    query2 = storage.all(Place)
    if "Place.{}".format(place_id) not in query2:
        abort(404)

    query["place_id"] = place_id
    review = Review(**query)
    review.save()
    return (jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """update Review object."""
    query = storage.all(Review)
    if "Review.{}".format(review_id) not in query:
        abort(404)
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for i in request.json:
        if i not in ['id', 'created_at', 'updated_at', 'user_id', 'place_id']:
            setattr(review, i, request.json[i])
    review.save()
    return jsonify(review.to_dict())
