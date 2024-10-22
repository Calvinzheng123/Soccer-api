import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import List

def date_query(start_date: str, end_date: str) -> List[dict]:
    date_format = "%Y-%m-%d"
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)
    delta = timedelta(days=1)
    all_events = []

    while start <= end:
        date_str = start.strftime(date_format)
        url = f"https://www.sofascore.com/api/v1/sport/football/scheduled-events/{date_str}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            events = data.get('events', [])

            for event in events:
                # Append each event's relevant information directly
                all_events.append({
                    "Home Team": event.get('homeTeam', {}).get('name'),
                    "Away Team": event.get('awayTeam', {}).get('name'),
                    "Event ID": event.get('id'),
                    "Home Score": event.get('homeScore', {}).get('current', 0),
                    "Away Score": event.get('awayScore', {}).get('current', 0),
                    "Tournament Name": event.get('tournament', {}).get('name'),
                    "Season ID": event.get('season', {}).get('id'),
                    "Tournament ID": event.get('tournament', {}).get('id'),
                    "Date": date_str
                })
        else:
            print(f"Failed to fetch data for {date_str}. Status code: {response.status_code}")

        start += delta

    return all_events  # Return a list of event dictionaries
