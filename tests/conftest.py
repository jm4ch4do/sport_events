import pytest

import api as _api
from api.endpoints import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()
    token = _api.auth.generate_token("testuser")
    client.token = token
    yield client
    app.config["TESTING"] = False
