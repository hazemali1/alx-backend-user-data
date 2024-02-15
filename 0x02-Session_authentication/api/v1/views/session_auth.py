#!/usr/bin/env python3
""" Module of Session authentication views
"""
from flask import request, jsonify
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """ POST /api/v1/auth_session/login
    Return:
      - the auth_session of the API
    """
    from api.v1.app import auth


    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({ "error": "email missing" }), 400
    if not password:
        return jsonify({ "error": "password missing" }), 400
    obj = User()
    if len(obj.search({'email': email})) == 0:
        return jsonify({ "error": "no user found for this email" }), 404
    user = obj.search({'email': email})[0]
    if user.is_valid_password(password) is False:
        return jsonify({ "error": "wrong password" }), 401
    session_id = auth.create_session(user.id)
    js = jsonify(user.to_json())
    session_name = os.environ.get('SESSION_NAME')
    js.set_cookie(session_name, session_id)
    return js
