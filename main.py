import dotenv as _dotenv

import application as _app
import config as _conf
import domain.match as _d_match
import services as _serv
from core import SessionLocal as _db_local

# initial config
_dotenv.load_dotenv()
config = _conf.Config()
db = _db_local()

_app.CreateMatches(db, config)()
matches = _app.GetAllMatches(db)(print_cards=True)
