#!/usr/bin/env python3
"""
API entry point and request handling
"""

from os import getenv

from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)

app = Flask(__name__)

# Register API blueprints (assuming blueprints reside in a subfolder "api.v1")
from api.v1 import views  # Assuming views.py holds API endpoints

app.register_blueprint(views.bp)

CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Configure authentication based on environment variable
auth_manager = None
auth_type = getenv("AUTH_TYPE")
if auth_type:
    auth_module_path = f"api.v1.auth.{auth_type.lower()}"  # Adapt path based on naming convention
    auth_module = __import__(auth_module_path, fromlist=[auth_type.lower()])
    if auth_type.lower() == "session_auth":
        auth_manager = getattr(auth_module, auth_type.lower())()  # Instantiate SessionAuth
    else:
        # Handle other auth types using existing mechanism (adapt as needed)
        auth_manager = getattr(auth_module, auth_type.lower())()

@app.errorhandler(404)
def not_found(error) -> dict:
    """ Handles 404 Not Found errors """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_error(error) -> dict:
    """ Handles 401 Unauthorized errors """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_error(error) -> dict:
    """ Handles 403 Forbidden errors """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """ Performs actions before handling each request """

    exempt_routes = [
        "/api/v1/status/",
        "/api/v1/unauthorized/",
        "/api/v1/forbidden/",
        "/api/v1/auth_session/login/",
    ]

    # Check for authentication if enabled
    if auth_manager:
        if auth_manager.requires_auth(request.path, exempt_routes):
            if not (auth_manager.authorization_header(request) or auth_manager.get_current_user(request)):
                abort(401)  # Unauthorized

            # Attach user object to request context (adapt method name as needed)
            request.current_user = auth_manager.get_authenticated_user(request)

            if not request.current_user:
                abort(403)  # Forbidden

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
