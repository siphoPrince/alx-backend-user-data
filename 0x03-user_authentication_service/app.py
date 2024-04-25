#!/usr/bin/env python3

"""Custom API Implementation
"""

from db import DB
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
from user import User

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """ GET /
    Return:
        Welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/register', methods=['POST'], strict_slashes=False)
def register_users():
    """ POST /register
        JSON body:
            -email
            -password
       return:
       Register a new user
    """
    user_data = request.form
    try:
        user = AUTH.register_user(
            user_data['email'],
            user_data['password'])
        return jsonify({"email": user.email, "message": "succes registered"})
    except ValueError:
        return jsonify({"message": "Email is already registered"}), 400


@app.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /login
            - email
            - password
        Return:
            Data from "email" and "password" fields
    """
    user_data = request.form

    user_email = user_data.get('email', '')
    user_password = user_data.get('password', '')
    is_valid_login = AUTH.valid_login(user_email, user_password)
    if not is_valid_login:
        abort(401)
    response = jsonify({"email": user_email, "message": "Login successfully"})
    response.set_cookie('session_id', AUTH.create_session(user_email))
    return response


@app.route('/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """ DELETE /logout
            - session_id
        Find user with requested session ID. If user exists,
        destroy session and redirect user to GET /
    """
    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)
    if session_id is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ GET /profile
    Return:
        - Use session_id to find the user.
        - 403 if session ID is invalid
    """
    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)
    if session_id is None or user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token_route() -> str:
    """ POST /reset_password
            - email
        Return:
            - Generate a Token
            - 403 if email not registered
    """
    user_data = request.form
    user_email = user_data.get('email', '')
    is_registered = AUTH.create_session(user_email)

    if not is_registered:
        abort(403)

    token = AUTH.get_reset_password_token(user_email)
    return jsonify({"email": user_email, "reset_token": token})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """ PUT /reset_password
            - email
            - reset_token
            - new_password
        Return:
            - Update the password
            - 403 if token is invalid
    """
    user_email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
    except Exception:
        abort(403)

    return jsonify(
        {"email": user_email, "message": "Password updated successfully"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
