import dotenv as _dotenv
import flask as _flask

import application as _app
import config as _conf
from core import SessionLocal as _db_local

app = _flask.Flask(__name__)
db = _db_local()


@app.route("/ok", methods=["GET"])
def health_check():
    return _flask.jsonify({"status": "OK", "message": "API is healthy!"})


@app.route("/matches", methods=["GET"])
def get_matches():
    matches = _app.GetAllMatches(db)(print_cards=False)
    return _flask.jsonify({"response": [match.to_dict() for match in matches]})


if __name__ == "__main__":
    app.run(debug=True)
