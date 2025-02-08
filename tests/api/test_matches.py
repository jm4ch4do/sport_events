import pytest

import api as _api


def test_get_matches_ko_unauthorized(client):
    response = client.get("/matches")

    assert response.status_code == 401
    assert "message" in response.json


def test_get_matches_ok(client):
    response = client.get(
        "/matches", headers={"Authorization": f"Bearer {client.token}"}
    )

    assert response.status_code == 200
    assert "response" in response.json
    assert isinstance(response.json["response"], list)
