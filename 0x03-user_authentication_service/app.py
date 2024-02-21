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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
