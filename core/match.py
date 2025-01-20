import sqlalchemy as _alc

from . import base_db


class Match(base_db.BaseDB):
    __tablename__ = "matches"

    id = _alc.Column(_alc.Integer, primary_key=True, autoincrement=True)
    sport = _alc.Column(_alc.String, nullable=False)
    league = _alc.Column(_alc.String, nullable=False)
    home = _alc.Column(_alc.String, nullable=False)
    away = _alc.Column(_alc.String, nullable=False)
    start = _alc.Column(_alc.DateTime, nullable=False)
    details = _alc.Column(_alc.String, nullable=True)
