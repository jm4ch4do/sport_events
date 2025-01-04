import dotenv as _dotenv

import config as _conf
import services as _serv

_dotenv.load_dotenv()
conf = _conf.Config()
_serv.SportsIoNBA(conf=conf)()
