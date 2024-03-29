#!/usr/bin/env python3
"""Flask server configuration"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def Bienvenue():
    """Bienvenue method for GET requests"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """users method for POST requests"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """login method for POST requests"""
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email, password):
        session = AUTH.create_session(email)
        js = jsonify({"email": email, "message": "logged in"})
        js.set_cookie("session_id", session)
        return js
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """logout method for DELETE requests"""
    session = request.cookies.get("session_id")
    if session is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session)
    if user:
        AUTH.destroy_session(user.id)
    else:
        abort(403)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile():
    """profile method for GET requests"""
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """get_reset_password_token method for POST requests"""
    email = request.form.get("email")
    if email is None:
        abort(403)
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """update_password method for PUT requests"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    if email is None or reset_token is None or new_password is None:
        abort(403)
    try:
        token = AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
