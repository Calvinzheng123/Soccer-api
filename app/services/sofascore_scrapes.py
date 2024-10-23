import requests
from datetime import datetime, timedelta
from typing import List

# Define the Big 5 leagues
BIG_5_LEAGUES = [
    "Premier League",
    "LaLiga",
    "Bundesliga",
    "Serie A",
    "Ligue 1"
]

def date_query(start_date: str, end_date: str) -> List[dict]:
    date_format = "%Y-%m-%d"
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)
    delta = timedelta(days=1)
    all_events = []

    while start <= end:
        date_str = start.strftime(date_format)
        
        print(f"Checking data for date: {date_str}")
        
        url = f"https://www.sofascore.com/api/v1/sport/football/scheduled-events/{date_str}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            events = data.get('events', [])

            for event in events:
                tournament_name = event.get('tournament', {}).get('name')

                tournament_name = event.get('tournament', {}).get('name')
                
                if tournament_name in BIG_5_LEAGUES:
                    all_events.append({
                        "homeTeam": event.get('homeTeam', {}).get('name', 'Unknown'),
                        "awayTeam": event.get('awayTeam', {}).get('name', 'Unknown'),
                        "eventID": event.get('id', 0),
                        "homeScore": event.get('homeScore', {}).get('current', 0),
                        "awayScore": event.get('awayScore', {}).get('current', 0),
                        "tournamentName": tournament_name,
                        "seasonID": event.get('season', {}).get('id', 0),
                        "tournamentID": event.get('tournament', {}).get('id', 0),
                        "eventDate": date_str
                    })
        else:
            print(f"Failed to fetch data for {date_str}. Status code: {response.status_code}")

        start += delta

    return all_events
