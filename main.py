import dotenv as _dotenv

import config as _conf
import services as _serv

_dotenv.load_dotenv()
config = _conf.Config()
_serv.AllSportsService(config)(time_frame="recent")
