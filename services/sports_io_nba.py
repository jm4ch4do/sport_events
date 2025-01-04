import datetime as _dt
import os as _os

import requests as _r


class SportsIoNBA:

    def __init__(self, conf):

        nba_data = conf.data["sport"]["nba"]

        # these attributes will go into parent class and only league name will be define here
        self.api_key = _os.getenv("API_KEY")
        self.url = nba_data["url"]
        self.teams = nba_data["teams"]


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
