#!/usr/bin/env python3
"""
New session auth
"""

from flask import Flask, request, jsonify
from api.v1.app import auth
from models.user import User

app = Flask(__name__)


@app.route('/api/v1/auth_session/logout', methods=['DELETE'])
def auth_session_logout():
    """
    Use auth.destroy_session(request) to delete the Session ID
    from the request's cookie
    """
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200


@app.route('/api/v1/auth_session/login', methods=['POST'])
def auth_session_login():
    """Retrieve email and password from request.form"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})

    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)

    """Return the dictionary representation of the User"""
    user_dict = user.to_json()

    """Set the cookie to the response"""
    cookie_name = app.config.get('SESSION_NAME')
    response = jsonify(user_dict)
    response.set_cookie(cookie_name, session_id)

    return response
