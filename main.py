from datetime import datetime

import dotenv as _dotenv

import config as _conf
import core.match as _d_match
import services as _serv
from core import SessionLocal as _db_local

_dotenv.load_dotenv()
config = _conf.Config()
db = _db_local()

_serv.AllSportsService(config)(time_frame="recent")


random_match = _d_match.Match(
    sport="Soccer",
    league="Test League",
    home="Team A",
    away="Team B",
    start=datetime(2025, 1, 20, 15, 0),
    details="Sample match",
)
random_match.save(db)
