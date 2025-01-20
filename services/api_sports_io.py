import abc as _abc
import datetime as _dt
import os as _os
import typing as _t

import requests as _r

import core as _core
import domain.match as _d_match


class BaseSportApi(_abc.ABC):
    """Base class common for all sport api implementations"""

    def __init__(self, sport_data):
        self.url = sport_data["url"]
        self.teams = sport_data["teams"]
        self.api_key = _os.getenv(sport_data["api_key_name"])

    @_abc.abstractmethod
    def __call__(self, sport_data):
        pass

    @staticmethod
    def get_week_dates():
        today = _dt.date.today()
        one_week_away = _dt.date.today() + _dt.timedelta(weeks=1)
        two_weeks_away = _dt.date.today() + _dt.timedelta(weeks=2)
        return today, one_week_away, two_weeks_away


class RapidApiFootball(BaseSportApi):
    """Requests football matches data"""

    def __init__(self, sport_data):
        super().__init__(sport_data)

    def __call__(self):
        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
        }

        matches = []
        for team in self.teams:
            params = {
                "team": team.get("team_id"),
                "league": team.get("league"),
                "season": team.get("season"),
            }
            response = _r.get(self.url, params=params, headers=headers)
            data = response.json()["response"]
            team_matches = [self._create_match(game) for game in data]
            matches.extend(team_matches)
        return matches

    @staticmethod
    def _create_match(game):
        """Fits request data to Match object"""
        return _d_match.Match(
            sport="football",
            league="La Liga",
            home=game["teams"]["home"]["name"],
            away=game["teams"]["away"]["name"],
            start=game["fixture"]["date"],
        )


class SportsIoMMA(BaseSportApi):
    """Requests MMA fights data"""

    def __init__(self, sport_data):
        super().__init__(sport_data)

    def __call__(self):
        headers = {"x-rapidapi-key": self.api_key}
        today, one_week_away, two_weeks_away = self.get_week_dates()

        matches = []
        for team in self.teams:
            params = {
                "season": team.get("season"),
            }
            response = _r.get(self.url, params=params, headers=headers)
            data = response.json()["response"]

            team_matches = []
            for date, slug in self._get_dates_per_event(data):
                colon_pos, vs_pos = slug.find(":"), slug.find("vs.")
                missing_data = True if colon_pos == -1 or vs_pos == -1 else False
                if missing_data:
                    continue
                else:
                    team_matches.append(
                        self._create_match(slug, colon_pos, vs_pos, date)
                    )
            matches.extend(team_matches)
        return matches

    @staticmethod
    def _create_match(slug, colon_pos, vs_pos, date):
        """Fits request data to Match object"""
        return _d_match.Match(
            sport="MMA",
            league="UFC",
            home=slug[colon_pos + 1 : vs_pos].strip(),
            away=slug[vs_pos + 3 :].strip(),
            start=date,
        )

    @classmethod
    def _get_dates_per_event(cls, data) -> _t.List[_t.Tuple[str, str]]:
        """Returns a list (date, slug) for events found in data"""
        numbered_fights_per_event = {}
        for fight in data:
            if cls.is_event_numbered(fight["slug"]) and fight["is_main"]:
                numbered_fights_per_event.setdefault(fight["slug"], []).append(fight)
        dates_per_event = []
        for slug, details in numbered_fights_per_event.items():
            dates_per_event.append((details[0]["date"], slug))
        return dates_per_event

    @staticmethod
    def is_event_numbered(slug) -> bool:
        """Returns true for numbered events like UFC 311 (UFC + number)"""
        company, event = slug.split()[:2]
        return True if company.lower() == "ufc" and event[:-1].isdigit() else False


class SportsIoNBA(BaseSportApi):
    """Requests NBA matches data"""

    def __init__(self, sport_data):
        super().__init__(sport_data)

    def __call__(self):
        headers = {"x-rapidapi-key": self.api_key}

        matches = []
        for team in self.teams:
            params = {
                "team": team.get("team_id"),
                "league": team.get("league"),
                "season": team.get("season"),
            }
            response = _r.get(self.url, params=params, headers=headers)
            data = response.json()["response"]

            team_matches = [self._create_match(game) for game in data]
            matches.extend(team_matches)
        return matches

    @staticmethod
    def _create_match(game):
        """Fits request data to Match object"""
        return _d_match.Match(
            sport="basketball",
            league="NBA",
            home=game["teams"]["home"]["name"],
            away=game["teams"]["visitors"]["name"],
            start=game["date"]["start"],
        )


class SportApiFactory:
    """Selects the appropiate service to get sport data"""

    _MAP = {
        _core.Sports.NBA: SportsIoNBA,
        _core.Sports.MMA: SportsIoMMA,
        _core.Sports.FOOTBALL: RapidApiFootball,
    }

    @classmethod
    def __call__(cls, config, sport_name):
        sport = _core.Sports(sport_name)
        sport_data = config.data["sport"][sport.value]
        sport_service = cls._MAP[sport]
        return sport_service(sport_data)


class AllSportsService:
    """Handles processed match data from classes that implement BaseSportsApi"""

    def __init__(self, config):

        self.active = ("football", "mma", "nba")  # choose values from Sports enum
        self.matches = self._get_matches(self.active, config)

    def __call__(self, time_frame: str = "recent"):
        """Prints information about all sports

        Args
            time_frame(str): one of 'old, this_week, next_week, later'
                             also accepts 'recent' = 'this_week' + 'next_week'
                             and 'all' = 'old' + 'this week' + 'next_week' + 'later'
        """

        selected_matches = []
        for match in self.matches:
            if match.meets_time_frame(time_frame):
                selected_matches.append(match)

        print(f"-------------------{time_frame.upper()} MATCHES----------------------")
        selected_matches.sort(key=lambda x: x.start)
        selected_matches = self._remove_duplicated_matches(selected_matches)
        match_cards = [
            match.get_match_card(show_time_label=True) for match in selected_matches
        ]
        self._print_cards(match_cards)
        return selected_matches

    @staticmethod
    def _get_matches(active, config):
        """Gets matches for active teams"""
        matches = []
        for sport in active:
            matches_by_sport = SportApiFactory()(config, sport)()
            matches.extend(matches_by_sport)
        return matches

    @staticmethod
    def _print_cards(match_cards):
        """Prints match cards avoiding duplicates
        Duplicates appear when both home and away teams are selected in config
        """
        previous = ""
        for match_card in match_cards:
            if match_card == previous:
                continue
            previous = match_card
            print(match_card)

    # TODO: implement method
    @staticmethod
    def _remove_duplicated_matches(matches):
        """ "Makes sure there are no duplicated matches were away=home of next match"""
        return matches
