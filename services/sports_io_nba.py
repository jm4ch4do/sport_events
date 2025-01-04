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


class ServiceForFootball(BaseSportsApi):
    def __init__(self):
        pass


class SportsIoMMA(BaseSportsApi):
    def __init__(self):
        pass


class SportsIoNBA(BaseSportsApi):

    def __init__(self, sport_data):
        super().__init__(sport_data)

    def __call__(self):
        headers = {"x-rapidapi-key": _os.getenv("API_KEY")}
        today = _dt.date.today()

        for team in self.teams:
            params = {
                "team": team.get("team_id"),
                "league": team.get("league"),
                "season": team.get("season"),
            }
            response = _r.get(self.url, params=params, headers=headers)
            data = response.json()["response"]
            one_week_away = _dt.date.today() + _dt.timedelta(weeks=1)
            two_weeks_away = _dt.date.today() + _dt.timedelta(weeks=1)
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


# class for selecting right class
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
