#!/usr/bin/env python3
"""
    a new Flask view that handles all
    routes for the Session authentication.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def login() -> str:
    """
        route for login
    """

    email = request.form.get('email')
    password = request.form.get('password')
    if not email or email == '':
        return jsonify({'error': 'email missing'}), 400
    elif not password or password == '':
        return jsonify({'error': 'password missing'}), 400
    user = User.search({'email': email})
    if not user:
        return jsonify({
                        'error': 'no user found for this email'
                        }), 404
    is_valid_password = user[0].is_valid_password(password)
    if not is_valid_password:
        return jsonify({'error': 'wrong password'}), 401
    else:
        from api.v1.app import auth
        SESSION_NAME = os.getenv('SESSION_NAME')
        session_id = auth.create_session(user[0].id)
        json = user[0].to_json()
        response = jsonify(json)
        response.set_cookie(SESSION_NAME, session_id)
        return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """
        return an empty JSON dictionary
        with the status code 200
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
