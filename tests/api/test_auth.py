import json
import os as _os

import pytest

from api.endpoints import app


def test_login_ok(client):
    data = {"username": _os.getenv("USER_NAME"), "password": _os.getenv("PASSWORD")}
    response = client.post("/login", json=data)

    assert response.status_code == 200
    json_response = response.get_json()
    assert "token" in json_response


def test_login_ko(client):
    data = {"username": "wronguser", "password": "wrongpass"}
    response = client.post("/login", json=data)

    assert response.status_code == 401
    json_response = response.get_json()
    assert "message" in json_response
    assert json_response["message"] == "Invalid credentials"
