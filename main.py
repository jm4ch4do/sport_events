from datetime import datetime

import dotenv as _dotenv

import config as _conf
import domain.match as _d_match
import services as _serv
from core import SessionLocal as _db_local

# initial config
_dotenv.load_dotenv()
config = _conf.Config()
db = _db_local()

# request data and save to db
recent_matches = _serv.AllSportsService(config)(time_frame="recent")
_d_match.Match.delete_all(db)
[match.save(db) for match in recent_matches]

# retrieve data from db and print
stored_matches = _d_match.Match.get_all(db)
match_cards = [match.get_match_card() for match in stored_matches]
[print(card) for card in match_cards]
