#!/usr/bin/env python3
"""main modeule for testing"""
import requests


localhost = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """test for /users route"""
    url = localhost + "/users"
    res = requests.post(url, {"email": email, "password": password})
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """test for /sessions route with wrong password"""
    url = localhost + "/sessions"
    res = requests.post(url, {"email": email, "password": password})
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """test for /sessions route with right password"""
    url = localhost + "/sessions"
    res = requests.post(url, {"email": email, "password": password})
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    session_id = res.cookies.get("session_id")
    return session_id


def profile_unlogged() -> None:
    """test for /profile route"""
    url = localhost + "/profile"
    res = requests.get(url)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """test for /profile route"""
    url = localhost + "/profile"
    res = requests.get(url, cookies={"session_id": session_id})
    assert res.status_code == 200
    email = res.json()["email"]
    assert res.json() == {"email": email}


def log_out(session_id: str) -> None:
    """test for /sessions route"""
    url = localhost + "/sessions"
    res = requests.delete(url, cookies={"session_id": session_id})
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """test for /reset_password route"""
    url = localhost + "/reset_password"
    res = requests.post(url, {"email": email})
    assert res.status_code == 200
    token = res.json()["reset_token"]
    assert res.json() == {"email": email, "reset_token": token}
    reset_token = res.json()["reset_token"]
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """test for /reset_password route"""
    url = localhost + "/reset_password"
    js = {"email": email,
          "reset_token": reset_token,
          "new_password": new_password
          }
    res = requests.put(url, js)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
