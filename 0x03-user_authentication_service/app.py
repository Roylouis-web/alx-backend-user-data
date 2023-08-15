#!/usr/bin/env python3
"""
    Module for a basic flask app
"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'])
def home_page() -> str:
    """
        GET /
        Returns:
            -> json string
    """

    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """
        GET /users
        Returns:
            -> json signifying a successful sign up or
                user already exists as a 400 error
    """

    try:
        email = request.form.get('email')
        password = request.form.get('password')
        user = AUTH.register_user(email, password)
        return jsonify({"email": f"{user.email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login() -> str:
    """
        POST /sessions
        Returns:
            -> a json with a cookie containing a session_id
                or a 401 error response
    """

    try:
        email = request.form.get('email')
        password = request.form.get('password')
        if not AUTH.valid_login(email, password):
            abort(401)
        session_id = AUTH.create_session(email)
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    except Exception:
        abort(401)


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout() -> None:
    """
        DELETE /sessions
        Returns:
            -> deletes the users session if it exists and redirects
               them to the home page else returns a 401 error
    """

    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for("home_page"))
    abort(403)


@app.route("/profile", methods=['GET'], strict_slashes=False)
def get_profile() -> str:
    """
        GET /profile
        returns a json string containing the user's email
    """

    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": f"{user.email}"})
    abort(403)


@app.route("/reset_password", methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> None:
    """
        GET /reset_token
        Returns:
            -> a json containing the user's email and
               a newly generated reset token
    """

    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{reset_token}"})
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """
        GET /reset_password
        Returns:
            -> a json string indicating password reset successful
               or a 403 error
    """

    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        user = AUTH.update_password(reset_token, new_password)
        return jsonify({"email": f"{email}", "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
