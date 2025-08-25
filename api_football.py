import requests
import pandas as pd

BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {}  # API key set dynamically from Streamlit

def get_fixtures(league_ids=None, days_ahead=2):
    from datetime import datetime, timedelta
    fixtures_list = []
    today = datetime.utcnow().date()
    end_date = today + timedelta(days=days_ahead)
    for league_id in league_ids or []:
        url = f"{BASE_URL}/fixtures"
        params = {"league": league_id, "season": 2025, "from": str(today), "to": str(end_date)}
        r = requests.get(url, headers=HEADERS, params=params)
        data = r.json()
        for f in data.get("response", []):
            fixture = f["fixture"]
            home = f["teams"]["home"]["name"]
            away = f["teams"]["away"]["name"]
            fixture_time = fixture["date"]
            fixtures_list.append({"fixture_id": fixture["id"], "league_id": league_id, "event": f"{home} vs {away}", "event_time": fixture_time})
    return pd.DataFrame(fixtures_list)

def get_odds(fixture_ids):
    odds_list = []
    for fid in fixture_ids:
        url = f"{BASE_URL}/odds"
        params = {"fixture": fid}
        r = requests.get(url, headers=HEADERS, params=params)
        data = r.json()
        for o in data.get("response", []):
            for book in o.get("bookmakers", []):
                for mkt in book.get("bets", []):
                    if mkt["name"] == "Match Winner":
                        for sel in mkt["values"]:
                            odds_list.append({"fixture_id": fid, "bookmaker": book["name"], "market": "1X2", "selection": sel["value"], "odds": sel["odd"]})
    return pd.DataFrame(odds_list)