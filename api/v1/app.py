#!/usr/bin/python3
"""
Flask api app base
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
import os


host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', '5000')


app = Flask(__name__)
app.url_map.strict_slashes = False
# CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_handler(self):
    """ close current SQLAlchemy Session """
    storage.close()


@app.errorhandler(404)
def error_404(ex):
    """ handle error for 404 """
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)
