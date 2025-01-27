import dotenv as _dotenv

import application as _app
import config as _conf
from api import app
from core import SessionLocal as _db_local

# # initial config
# _dotenv.load_dotenv()
# config = _conf.Config()
# db = _db_local()

# _app.CreateMatches(db, config)()
# matches = _app.GetAllMatches(db)(print_cards=True)
# a = 1


if __name__ == "__main__":
    app.run(debug=True)
