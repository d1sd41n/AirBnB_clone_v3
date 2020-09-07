#!/usr/bin/python3
"""indxex doc"""
from api.v1.views import app_views
from models import storage
from flask import Flask, Blueprint, jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """status"""
    return jsonify({"status": "OK"})

