import abc as _abc
import datetime as _dt
import os as _os

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


class ServiceForFootball(BaseSportsApi):

    def __init__(self, sport_data):
        super().__init__(sport_data)

    def __call__(self):
        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
        }
        today, one_week_away, two_weeks_away = self.get_week_dates()

        print(
            f"------------------------------SERVICE FOOTBALL------------------------------"
        )

        for team in self.teams:
            params = {
                "team": team.get("team_id"),
                "league": team.get("league"),
                "season": team.get("season"),
            }
            response = _r.get(self.url, params=params, headers=headers)
            data = response.json()["response"]
            games_this_week, games_next_week, games_later = [], [], []

            print(f"--------------------TEAM {team.get("id")}--------------------")
            for i, game in enumerate(data):
                visitors = game["teams"]["away"]["name"]
                home = game["teams"]["home"]["name"]
                start = game["fixture"]["date"].replace("Z", "+00:00")
                start = _dt.datetime.fromisoformat(start)
                game_info = {"visitors": visitors, "home": home, "start": start}
                start_date = start.date()
                if today < start_date <= one_week_away:
                    games_this_week.append(game_info)
                elif one_week_away < start_date <= two_weeks_away:
                    games_next_week.append(game_info)
                else:
                    games_later.append(game_info)

            print("----------GAMES THIS WEEK----------")
            for game_info in games_this_week:
                print(
                    f"{game_info["home"]} vs {game_info["visitors"]} at {game_info["start"]}"
                    f" ({game_info["start"].strftime("%a").upper()})"
                )

            print("----------GAMES NEXT WEEK----------")
            for game_info in games_next_week:
                print(
                    f"{game_info["home"]} vs {game_info["visitors"]} at {game_info["start"]}"
                    f" ({game_info["start"].strftime("%a").upper()})"
                )

            print("------------GAMES LATER------------")
            for game_info in games_later:
                print(
                    f"{game_info["home"]} vs {game_info["visitors"]} at {game_info["start"]}"
                )


class SportsIoMMA(BaseSportsApi):

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

            numbered_fights_per_event = {}
            for fight in data:
                if self.is_event_numbered(fight["slug"]) and fight["is_main"]:
                    numbered_fights_per_event.setdefault(fight["slug"], []).append(
                        fight
                    )

            event_dates = []
            for event, details in numbered_fights_per_event.items():
                date = details[0]["date"].replace("Z", "+00:00")
                date = _dt.datetime.fromisoformat(date)
                event_dates.append((date.date(), event))
            event_dates.sort(key=lambda x: x[0])

            events_this_week, events_next_week, events_later = [], [], []
            for event in event_dates:
                date = event[0]
                if today < date <= one_week_away:
                    events_this_week.append(event)
                elif one_week_away < date <= two_weeks_away:
                    events_next_week.append(event)
                else:
                    events_later.append(event)

            print("----------EVENTS THIS WEEK----------")
            for event_date, event_name in events_this_week:
                print(
                    f"{event_name} at {event_date}",
                    f" ({event_date.strftime("%a").upper()})",
                )

            print("----------EVENTS NEXT WEEK----------")
            for event_date, event_name in events_next_week:
                print(
                    f"{event_name} at {event_date}",
                    f" ({event_date.strftime("%a").upper()})",
                )

            print("----------EVENTS LATER----------")
            for event_date, event_name in events_later:
                print(
                    f"{event_name} at {event_date}",
                    f" ({event_date.strftime("%a").upper()})",
                )

    @staticmethod
    def is_event_numbered(slug):
        """Returns true for numbered events like UFC 311 (UFC + number)"""
        company, event = slug.split()[:2]
        return True if company.lower() == "ufc" and event[:-1].isdigit() else False


class SportsIoNBA(BaseSportsApi):

    def __init__(self, sport_data):
        super().__init__(sport_data)

    def __call__(self):
        headers = {"x-rapidapi-key": self.api_key}
        today, one_week_away, two_weeks_away = self.get_week_dates()

        print(
            f"------------------------------SERVICE NBA------------------------------"
        )

        for team in self.teams:
            params = {
                "team": team.get("team_id"),
                "league": team.get("league"),
                "season": team.get("season"),
            }
            response = _r.get(self.url, params=params, headers=headers)
            data = response.json()["response"]
            games_this_week, games_next_week, games_later = [], [], []
            print(f"--------------------TEAM {team.get("id")}--------------------")
            for i, game in enumerate(data):
                visitors = game["teams"]["visitors"]["name"]
                home = game["teams"]["home"]["name"]
                start = game["date"]["start"].replace("Z", "+00:00")
                start = _dt.datetime.fromisoformat(start)
                game_info = {"visitors": visitors, "home": home, "start": start}
                start_date = start.date()
                if today < start_date <= one_week_away:
                    games_this_week.append(game_info)
                elif one_week_away < start_date <= two_weeks_away:
                    games_next_week.append(game_info)
                else:
                    games_later.append(game_info)

            print("----------GAMES THIS WEEK----------")
            for game_info in games_this_week:
                print(
                    f"{game_info["home"]} vs {game_info["visitors"]} at {game_info["start"]}"
                    f" ({game_info["start"].strftime("%a").upper()})"
                )

            print("----------GAMES NEXT WEEK----------")
            for game_info in games_next_week:
                print(
                    f"{game_info["home"]} vs {game_info["visitors"]} at {game_info["start"]}"
                    f" ({game_info["start"].strftime("%a").upper()})"
                )

            print("------------GAMES LATER------------")
            for game_info in games_later:
                print(
                    f"{game_info["home"]} vs {game_info["visitors"]} at {game_info["start"]}"
                )


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
