import datetime as _dt
import os as _os

import dotenv as _dotenv
import requests as _r

_dotenv.load_dotenv()
URL = "https://v2.nba.api-sports.io/games"
headers = {"x-rapidapi-key": _os.getenv("API_KEY")}

today = _dt.date.today()
end_date = today + _dt.timedelta(weeks=4)
dates = [today + _dt.timedelta(days=i) for i in range((end_date - today).days + 1)]
params = {
    "league": "standard",  # nba
    "season": 2024,
    "team": 11,  # warriors
    #'date': dates[0]
}

response = _r.get(URL, params=params, headers=headers)
data = response.json()["response"]
one_week_away = _dt.date.today() + _dt.timedelta(weeks=1)
two_weeks_away = _dt.date.today() + _dt.timedelta(weeks=1)
games_this_week, games_next_week, games_later = [], [], []
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

print("--------------------GAMES THIS WEEK--------------------")
for game_info in games_this_week:
    print(
        f"{game_info["home"]} vs {game_info["visitors"]} at {game_info["start"]}"
        f" ({game_info["start"].strftime("%a").upper()})"
    )

print("--------------------GAMES NEXT WEEK--------------------")
for game_info in games_next_week:
    print(
        f"{game_info["home"]} vs {game_info["visitors"]} at {game_info["start"]}"
        f" ({game_info["start"].strftime("%a").upper()})"
    )

print("----------------------GAMES LATER----------------------")
for game_info in games_later:
    print(f"{game_info["home"]} vs {game_info["visitors"]} at {game_info["start"]}")
