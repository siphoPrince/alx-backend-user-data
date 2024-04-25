#!/usr/bin/env python3

"""Custom API Implementation codebase"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

# Instantiate the Auth object
AUTH = Auth()

# Create a Flask app
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """GET /
    Returns a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/register', methods=['POST'], strict_slashes=False)
def register_users():
    """POST /register
    Registers a new user.

    JSON body:
        - email: The email of the user to register.
        - password: The password of the user to register.

    Returns:
        - JSON object containing the
        email of the registered user and a success message.
        - 400 status code if the email is already registered.
    """
    user_data = request.form
    try:
        user = AUTH.register_user(
            user_data['email'],
            user_data['password'])
        return jsonify({"email": user.email, "message": "Success register."})
    except ValueError:
        return jsonify({"message": "Email is already registered"}), 400


@app.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """POST /login
    Logs in a user.

    JSON body:
        - email: The email of the user.
        - password: The password of the user.

    Returns:
        - JSON object containing the email of the logged-in user and a succe
        ss message.
        - Sets a session cookie with the session ID.
        - 401 status code if login fails.
    """
    user_data = request.form

    user_email = user_data.get('email', '')
    user_password = user_data.get('password', '')
    is_valid_login = AUTH.valid_login(user_email, user_password)
    if not is_valid_login:
        abort(401)
    response = jsonify({"email": user_email, "message": "Login successful"})
    response.set_cookie('session_id', AUTH.create_session(user_email))
    return response


@app.route('/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """DELETE /logout
    Logs out a user by destroying their session.

    Returns:
        - Redirects the user to the welcome page after successfully loggin
        - 403 status code if the session ID is invalid.
    """
    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)
    if session_id is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """GET /profile
    Retrieves the profile of the logged-in user.

    Returns:
        - JSON object containing the email of the logged-in user.
        - 403 status code if the session ID is invalid.
    """
    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)
    if session_id is None or user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token_route() -> str:
    """POST /reset_password
    Generates a reset token for resetting the password.

    JSON body:
        - email: The email of the user.

    Returns:
        - JSON object containing the email of the user and the reset token.
        - 403 status code if the email is not registered.
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
    """PUT /reset_password
    Updates the password using the reset token.

    JSON body:
        - email: The email of the user.
        - reset_token: The reset token.
        - new_password: The new password.

    Returns:
        - JSON object containing the email of the user and a success message.
        - 403 status code if the reset token is invalid.
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


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """POST /users
    Registers a new user.

    JSON body:
        - email: The email of the user to register.
        - password: The password of the user to register.

    Returns:
        - JSON object containing th
        e email of the registered user and a success message.
        - 400 status code if the email is already registered.
    """
    user_data = request.form
    try:
        user = AUTH.register_user(
            user_data['email'],
            user_data['password'])
        return jsonify({"email": user.email, "message": "New user created"})
    except ValueError:
        return jsonify({"message": "Email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
