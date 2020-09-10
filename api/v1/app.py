#!/usr/bin/python3
""" app doc """
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from os import getenv
from models import storage
from flask_cors import CORS

app = Flask(__name__)


app.register_blueprint(app_views, url_prefix="/api/v1")
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_session(self):
    """ close_session
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """not_found"""
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, debug=True, threaded=True)
