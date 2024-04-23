from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
auth = Auth()

@app.route('/')
def welcome():
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'])
def register_user():
    data = request.form
    email = data.get('email')
    password = data.get('password')
    try:
        user = auth.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@app.route('/sessions', methods=['POST'])
def login():
    data = request.form
    email = data.get('email')
    password = data.get('password')
    if auth.valid_login(email, password):
        session_id = auth.create_session(email)
        return jsonify({"email": email, "message": "logged in"}), 200, {'Set-Cookie': 'session_id={}; Path=/'.format(session_id)}
    else:
        return jsonify({"message": "Unauthorized"}), 401

@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    data = request.form
    email = data.get('email')
    try:
        reset_token = auth.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

