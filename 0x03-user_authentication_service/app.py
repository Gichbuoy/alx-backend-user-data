#!/usr/bin/env python3
"""Basic Flask app"""

from flask import Flask, abort, jsonify, redirect, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=["GET"], strict_slashes=False)
def welcome():
    """Return a dummy JSON payload"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_users():
    """
    Endpoint for user registration.

    Expects form data fields:
    - "email": The email of the user to be registered.
    - "password": The password of the user.

    Returns:
    - If user is successfully registered:
      JSON payload: {"email": "<registered email>", "message": "user created"}
      Status Code: 200

    - If user is already registered:
      JSON payload: {"message": "email already registered"}
      Status Code: 400
    """
    email, password = request.form.get('email'), request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    Validate user login credentials.

    Args:
        email (str): The email of the user.
        password (str): The password entered by the user.

    Returns:
        bool: True if login is valid, False otherwise.
    """
    email, password = request.form.get('email'), request.form.get('password')
    if AUTH.valid_login(email, password):
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", AUTH.create_session(email))
        return response
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Logout route: Handles the DELETE /sessions route.

    The request is expected to contain the session ID as a cookie
    with key "session_id".

    Find the user with the requested session ID. If the user exists,
    destroy the session and redirect
    the user to GET /. If the user does not exist, respond with a 403
    HTTP status.

    Returns:
    - Response: A redirect response or a 403 HTTP status.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    Profile route: Handles the GET /profile route.

    The request is expected to contain a session_id cookie.
    Use it to find the user.
    If the user exists, respond with a 200 HTTP status and the
    following JSON payload:
    {
        "user_id": <user_id>,
        "email": "<user_email>"
    }
    If the user does not exist, respond with a 403 HTTP status.

    Returns:
    - Response: A JSON response with user information or a 403 HTTP status.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        return jsonify({"email": user.email})
    abort(403)


@app.route('/reset_password ', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
    Reset Password route: Handles the POST /reset_password route.

    The request is expected to contain form data with the "email" field.

    If the email is not registered, respond with a 403 status code.
    Otherwise, generate a token and respond with a 200 HTTP status and
    the following JSON payload:
    {
        "reset_token": "<generated_reset_token>"
    }

    Returns:
    - Response: A JSON response with the reset token or a 403 HTTP status.
    """
    try:
        email = request.form.get("email")
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token})


@app.route('/reset_password ', methods=['PUT'], strict_slashes=False)
def update_password():
    """
    Update Password route: Handles the PUT /reset_password route.

    The request is expected to contain form data with fields "email",
    "reset_token", and "new_password".

    Update the password. If the token is invalid, catch the exception
    and respond with a 403 HTTP code.
    If the token is valid, respond with a 200 HTTP code and the
    following JSON payload:
    {
        "email": "<user_email>",
        "message": "Password updated"
    }

    Returns:
    - Response: A JSON response with the user email and a message or a
    403 HTTP status.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    is_password_changed = False
    try:
        AUTH.update_password(reset_token, new_password)
        is_password_changed = True
    except ValueError:
        is_password_changed = False
    if not is_password_changed:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
