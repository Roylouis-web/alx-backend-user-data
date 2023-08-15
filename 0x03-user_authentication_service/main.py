#!/usr/bin/env python3
"""
    Module for an integration test for the flask app
"""
import requests
import json


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """
        tests for correct output of
        of the POST /users route
        :params
            -> email: user's email
            -> password: user's password
    """

    data = {"email": email, "password": password}
    response = requests.post("http://localhost:5000/users", data=data)

    assert response.status_code == 200
    assert type(response.text) == str
    assert type(json.loads(response.text)) == dict


def log_in_wrong_password(email: str, password: str) -> None:
    """
        tests for correct output
        with wrong credentials of POST /sessions route
        :params
            -> email: user's email
            -> password: user's password
    """

    data = {"email": email, "password": password}
    response = requests.post("http://localhost:5000/sessions", data=data)

    assert response.status_code == 401
    assert type(response.text) == str
    assert response.cookies.get("session_id") is None


def log_in(email: str, password: str) -> str:
    """
        tests for correct output
        with correct credentials of POST /sessions route
    :params
        -> email: user's email
        -> password: user's password
    """

    data = {"email": email, "password": password}
    response = requests.post("http://localhost:5000/sessions", data=data)

    assert response.status_code == 200
    assert type(response.text) == str
    assert type(json.loads(response.text)) == dict
    assert json.loads(response.text).get('email') == email
    assert json.loads(response.text).get('message') == 'logged in'
    assert response.cookies.get("session_id")
    assert type(response.cookies.get("session_id")) == str
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """
        tests for correct output of GET /profile route
        with wrong credentials
    """

    response = requests.get("http://localhost:5000/profile")
    assert response.status_code == 403
    assert type(response.text) == str


def profile_logged(session_id: str) -> None:
    """
        tests for correct output of GET /profile route
        with correct credentials
        :params
            -> session_id: users's session id
    """

    cookies = requests.cookies.RequestsCookieJar()
    cookies.set("session_id", session_id)
    response = requests.get("http://localhost:5000/profile", cookies=cookies)

    assert response.status_code == 200
    assert type(response.text) == str
    assert type(json.loads(response.text)) == dict
    assert type(json.loads(response.text).get('email')) == str


def log_out(session_id: str) -> None:
    """
        tests for correct output of DELETE /sessions route
        :params
            -> session_id: users's session id
    """

    cookies = requests.cookies.RequestsCookieJar()
    cookies.set("session_id", session_id)
    response = requests.delete("http://localhost:5000/sessions",
                               cookies=cookies, allow_redirects=False)

    assert response.is_redirect
    assert response.status_code == 302


def reset_password_token(email: str) -> str:
    """
        tests for correct output of POST /reset_password route
        :params
            -> email: user's email
    """

    data = {"email": email}
    response = requests.post("http://localhost:5000/reset_password", data=data)
    assert type(json.loads(response.text)) == dict
    assert json.loads(response.text).get('email') == email
    assert type(response.text) == str
    assert type(json.loads(response.text).get('reset_token')) == str
    assert json.loads(response.text).get('reset_token')
    assert response.status_code == 200

    return json.loads(response.text).get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
        tests for correct output of PUT /reset_password route
        :params
            -> email: user's email
            -> reset_token: user's reset token
            -> new_password: user's new password
    """

    data = {
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
           }
    response = requests.put("http://localhost:5000/reset_password", data=data)
    assert response.status_code == 200
    assert type(json.loads(response.text)) == dict
    assert type(response.text) == str
    assert type(json.loads(response.text).get('email')) == str
    assert json.loads(response.text).get('email')
    assert json.loads(response.text).get('message') == "Password updated"
    assert json.loads(response.text).get('message')


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
