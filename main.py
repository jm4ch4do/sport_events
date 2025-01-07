import dotenv as _dotenv

import config as _conf
import services as _serv

_dotenv.load_dotenv()
config = _conf.Config()
mma_service = _serv.SportApiFactory()(config, "mma")
nba_service = _serv.SportApiFactory()(config, "nba")
mma_service()
nba_service()
