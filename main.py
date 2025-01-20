from datetime import datetime

import dotenv as _dotenv

import config as _conf
import core.match as _c_match
import domain.match as _d_match
import services as _serv
from core import SessionLocal as _db_local

_dotenv.load_dotenv()
config = _conf.Config()
db = _db_local()

recent_matches = _serv.AllSportsService(config)(time_frame="recent")
if len(recent_matches) > 0:
    _d_match.Match.delete_all(db)
    [match.save(db) for match in recent_matches]
