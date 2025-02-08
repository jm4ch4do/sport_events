import click as _click
import dotenv as _dotenv

import api as _api
import application as _app
import config as _conf
from core import SessionLocal as _db_local

# # initial config
_dotenv.load_dotenv()
config = _conf.Config()
db = _db_local()


@_click.group()
def cli():
    """Groups commands for command line"""
    pass


@cli.command()
def webserver():
    """Start Flask web server."""
    _api.app.run(debug=True)


@cli.command()
def tasks():
    """Run tasks"""
    _app.CreateMatches(db, config)()
    matches = _app.GetAllMatches(db)(print_cards=True)


if __name__ == "__main__":
    cli()
