import abc as _abc
import datetime as _dt
import os as _os
import typing as _t
import zoneinfo as _zi

import requests as _r

import core as _core


class BaseSportsApi(_abc.ABC):
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


class Match:
    """All services use this class to store match data"""

    def __init__(
        self,
        sport: str,
        home: str,
        away: str,
        start: _t.Union[str, _dt.datetime],
        league: str,
        details: str = "",
    ):
        self.sport = sport
        self.home = home
        self.away = away
        self.start = self.format_date(start)
        self.league = league
        self.details = details

        self.date = self.start.date()
        self.time = f"{self.start.time().hour}:{self.start.time().minute}"
        self.day_of_week = self.start.strftime("%a").upper()

        now = _dt.datetime.now()
        now_date, start_date = now.date(), self.start.date()
        now_weekday, start_weekday = now.weekday(), self.start.weekday()
        current_week_start = now_date - _dt.timedelta(days=now.weekday())
        current_week_end = current_week_start + _dt.timedelta(days=6)
        next_week_start = current_week_end + _dt.timedelta(days=1)
        next_week_end = current_week_end + _dt.timedelta(days=6)

        self.in_current_week = current_week_start <= start_date <= current_week_end
        self.in_next_week = next_week_start <= start_date <= next_week_end
        self.in_next_7_days = now_date <= start_date <= now_date + _dt.timedelta(7)
        self.in_next_15_days = now_date <= start_date <= now_date + _dt.timedelta(15)
        self.is_old = now_date > start_date

    def __str__(self) -> str:
        return f"{self.home} vs {self.away} at {self.start} ({self.day_of_week})"

    @staticmethod
    def format_date(date: str | _dt.datetime) -> _dt.datetime:
        """Converts date to expected format"""
        if isinstance(date, str):
            date.replace("Z", "+00:00")
            date = _dt.datetime.fromisoformat(date)
        local_timezone = _zi.ZoneInfo("America/New_York")
        return date.astimezone(local_timezone)

    def print_details(self, show_old=False):
        if self.is_old and show_old:
            print("--is_old ->", self)
        elif self.in_current_week:
            print("--current_week ->", self)
        elif self.in_next_week:
            print("--next_week ->", self)
        else:
            print("--later ->", self)


class ServiceForFootball(BaseSportsApi):
    """Requests football matches data"""

    def __init__(self, sport_data):
        super().__init__(sport_data)

    def __call__(self):
        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
        }

        print(
            f"------------------------------SERVICE FOOTBALL------------------------------"
        )

        for team in self.teams:
            print(f"--------------------TEAM {team.get("id")}--------------------")
            params = {
                "team": team.get("team_id"),
                "league": team.get("league"),
                "season": team.get("season"),
            }
            response = _r.get(self.url, params=params, headers=headers)
            data = response.json()["response"]

            matches = [
                Match(
                    sport="football",
                    league="La Liga",
                    home=game["teams"]["home"]["name"],
                    away=game["teams"]["away"]["name"],
                    start=game["fixture"]["date"],
                )
                for game in data
            ]
            matches.sort(key=lambda x: x.start)
            [match.print_details(show_old=True) for match in matches]


class SportsIoMMA(BaseSportsApi):
    """Requests MMA fights data"""

    def __init__(self, sport_data):
        super().__init__(sport_data)

    def __call__(self):
        headers = {"x-rapidapi-key": self.api_key}
        today, one_week_away, two_weeks_away = self.get_week_dates()

        print(
            f"------------------------------SERVICE MMA------------------------------"
        )

        for team in self.teams:
            params = {
                "season": team.get("season"),
            }
            response = _r.get(self.url, params=params, headers=headers)
            data = response.json()["response"]

            matches = []
            for date, slug in self._get_dates_per_event(data):
                colon_pos, vs_pos = slug.find(":"), slug.find("vs.")
                missing_data = True if colon_pos == -1 or vs_pos == -1 else False
                if missing_data:
                    continue
                else:
                    match = Match(
                        sport="MMA",
                        league="UFC",
                        home=slug[colon_pos + 1 : vs_pos].strip(),
                        away=slug[vs_pos + 3 :].strip(),
                        start=date,
                    )
                    matches.append(match)
            matches.sort(key=lambda x: x.start)
            [match.print_details(show_old=True) for match in matches]

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


class SportsIoNBA(BaseSportsApi):
    """Requests NBA matches data"""

    def __init__(self, sport_data):
        super().__init__(sport_data)

    def __call__(self):
        headers = {"x-rapidapi-key": self.api_key}

        print(
            f"------------------------------SERVICE NBA------------------------------"
        )

        for team in self.teams:
            print(f"--------------------TEAM {team.get("id")}--------------------")
            params = {
                "team": team.get("team_id"),
                "league": team.get("league"),
                "season": team.get("season"),
            }
            response = _r.get(self.url, params=params, headers=headers)
            data = response.json()["response"]

            matches = [
                Match(
                    sport="basketball",
                    league="NBA",
                    home=game["teams"]["home"]["name"],
                    away=game["teams"]["visitors"]["name"],
                    start=game["date"]["start"],
                )
                for game in data
            ]
            matches.sort(key=lambda x: x.start)
            [match.print_details(show_old=True) for match in matches]


class SportApiFactory:
    """Selects the appropiate service to get sport data"""

    _MAP = {
        _core.Sports.NBA: SportsIoNBA,
        _core.Sports.MMA: SportsIoMMA,
        _core.Sports.FOOTBALL: ServiceForFootball,
    }

    @classmethod
    def __call__(cls, config, sport_name):
        sport = _core.Sports(sport_name)
        sport_data = config.data["sport"][sport.value]
        sport_service = cls._MAP[sport]
        return sport_service(sport_data)
