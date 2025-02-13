import sqlalchemy as _alc
from sqlalchemy import orm as _alc_orm

from . import base_db

DATABASE_URL = "sqlite:///sports_events.db"


class Match(base_db.BaseDB):
    __tablename__ = "matches"

    id = _alc.Column(_alc.Integer, primary_key=True, autoincrement=True)
    sport = _alc.Column(_alc.String, nullable=False)
    league = _alc.Column(_alc.String, nullable=False)
    home = _alc.Column(_alc.String, nullable=False)
    away = _alc.Column(_alc.String, nullable=False)
    start = _alc.Column(_alc.DateTime, nullable=False)
    details = _alc.Column(_alc.String, nullable=True)


engine = _alc.create_engine(DATABASE_URL, echo=False)
SessionLocal = _alc_orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
Match.metadata.create_all(bind=engine)
