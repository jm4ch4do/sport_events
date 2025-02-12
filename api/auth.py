import datetime as _dt
import functools as _funct
import os as _os

import flask as _flask
import jwt as _jwt


def generate_token(username):
    payload = {
        "user": username,
        "exp": _dt.datetime.now(_dt.UTC) + _dt.timedelta(hours=1),
    }
    return _jwt.encode(payload, _os.getenv("SECRET_KEY"), algorithm="HS256")


def require_token(f):
    @_funct.wraps(f)
    def decorated(*args, **kwargs):
        token = _flask.request.headers.get("Authorization")
        if not token:
            return _flask.jsonify({"message": "Token required"}), 401
        try:
            decoded_token = _jwt.decode(
                token.split(" ")[1], _os.getenv("SECRET_KEY"), algorithms=["HS256"]
            )
        except _jwt.ExpiredSignatureError:
            return _flask.jsonify({"message": "Token expired"}), 401
        except _jwt.InvalidTokenError:
            return _flask.jsonify({"message": "Invalid token"}), 401
        return f(*args, **kwargs)

    return decorated


def login():
    auth = _flask.request.json
    if (
        auth
        and auth.get("username") == _os.getenv("USER_NAME")
        and auth.get("password") == _os.getenv("PASSWORD")
    ):
        token = generate_token(auth["username"])
        return _flask.jsonify({"token": token})
    return _flask.jsonify({"message": "Invalid credentials"}), 401
