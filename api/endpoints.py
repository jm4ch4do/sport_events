import os as _os

import flask as _flask

import application as _appl
import config as _conf
from core import SessionLocal as _db_local

from . import auth as _auth

# we should have a common place where app is created only once, maybe in __init__
app = _flask.Flask(__name__)
app.config["SECRET_KEY"] = _os.getenv("SECRET_KEY")
db = _db_local()
config = _conf.Config()


@app.route("/login", methods=["POST"])
def login():
    return _auth.login()


@app.route("/ok", methods=["GET"])
def health_check():
    return _flask.jsonify({"status": "OK", "message": "API is healthy!"})


@app.route("/matches", methods=["GET"])
@_auth.require_token
def get_matches():
    matches = _appl.GetAllMatches(db)(print_cards=False)
    return _flask.jsonify({"response": [match.to_dict() for match in matches]})


@app.route("/create_matches", methods=["GET"])
def create_matches():
    _appl.CreateMatches(db, config)()
    return _flask.jsonify({"status": "OK", "message": "Matches Created"})


if __name__ == "__main__":
    app.run(debug=True)
