import domain.match as _d_match
import services as _serv


class CreateMatches:
    """Imports matches from services to db"""

    def __init__(self, db, config):
        self.db = db
        self.config = config

    def __call__(self):
        recent_matches = _serv.AllSportsService(self.config)(time_frame="recent")
        _d_match.Match.delete_all(self.db)
        [match.save(self.db) for match in recent_matches]


class GetAllMatches:
    """Retrieves all matches stored in db"""

    def __init__(self, db):
        self.db = db

    def __call__(self, print_cards=False):
        stored_matches = _d_match.Match.get_all(self.db)
        if print_cards:
            match_cards = [match.get_match_card() for match in stored_matches]
            [print(card) for card in match_cards]
        return stored_matches
