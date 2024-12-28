import requests as _r
import datetime as _dt
import dotenv as _dotenv
import os as _os

_dotenv.load_dotenv()
URL = "https://v2.nba.api-sports.io/games" 
headers = { 'x-rapidapi-key': _os.getenv('API_KEY') }

today = _dt.date.today()
end_date = today + _dt.timedelta(weeks=4)
dates = [today + _dt.timedelta(days=i) for i in range((end_date - today).days + 1)]
params = {
    'league': "standard",  # nba
    'season': 2024,
    'team': 11,  # warriors
    #'date': dates[0]
}

response = _r.get(URL, params=params, headers=headers)
data = response.json()['response']
for i, game in enumerate(data):
    visitors = game['teams']['visitors']['name']
    home = game['teams']['home']['name']
    start_time = game['date']['start']
    print(f"{home} vs {visitors} at {start_time}")
