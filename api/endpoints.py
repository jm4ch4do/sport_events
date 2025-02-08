
import flask as _flask
import os as _os
from core import SessionLocal as _db_local
from . import auth as _auth
import application as _app


app = _flask.Flask(__name__)
app.config["SECRET_KEY"] = _os.getenv("SECRET_KEY")
db = _db_local()


@app.route("/login", methods=["POST"])
def login():
    return _auth.login()


@app.route("/ok", methods=["GET"])
def health_check():
    return _flask.jsonify({"status": "OK", "message": "API is healthy!"})


@app.route("/matches", methods=["GET"])
@_auth.require_token
def get_matches():
    matches = _app.GetAllMatches(db)(print_cards=False)
    return _flask.jsonify({"response": [match.to_dict() for match in matches]})


if __name__ == "__main__":
    app.run(debug=True)
