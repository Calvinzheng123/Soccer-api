from LionAPI.services.database import create_connection
from LionAPI.services.sofascore_client import fetch_json
import pandas as pd

def get_shots(home_team, away_team, match_date):
    """
    Fetches shot data for a soccer match from the SofaScore API.

    Parameters:
        home_team (str): Name of the home team.
        away_team (str): Name of the away team.
        match_date (str): Date of the match in 'YYYY-MM-DD' format.

    Returns:
        pd.DataFrame: DataFrame containing shot data, or None if there was an error.
    """
    connection = create_connection()
    if connection is not None:
        cursor = connection.cursor()
        try:
            query = """
                SELECT event_id
                FROM events
                WHERE home_team = ? AND away_team = ? AND event_date = ?;
            """
            cursor.execute(query, (home_team, away_team, match_date))
            result = cursor.fetchone()

            if result is None:
                print("No game found for the given parameters.")
                return None
            
            event_id = result["event_id"]
            url = f"https://sofascore.com/api/v1/event/{event_id}/shotmap"

            try:
                shots = fetch_json(url)
                if 'shotmap' not in shots:
                    print("Invalid response structure.")
                    return None

                df = pd.json_normalize(shots['shotmap'])
                df = df[df['situation'] != 'shootout']

                selected_columns = [
                    'isHome', 'shotType', 'situation', 'bodyPart', 'goalMouthLocation',
                    'xg', 'id', 'time', 'addedTime', 'timeSeconds', 'reversedPeriodTime',
                    'reversedPeriodTimeSeconds', 'incidentType', 'player.name', 'player.position', 
                    'player.jerseyNumber', 'player.id', 'playerCoordinates.x', 'playerCoordinates.y', 
                    'playerCoordinates.z', 'goalMouthCoordinates.x', 'goalMouthCoordinates.y', 
                    'goalMouthCoordinates.z', 'blockCoordinates.x', 'blockCoordinates.y', 
                    'blockCoordinates.z', 'draw.start.x', 'draw.start.y', 'draw.block.x', 
                    'draw.block.y', 'draw.end.x', 'draw.end.y', 'draw.goal.x', 'draw.goal.y', 
                    'goalType', 'xgot'
                ]

                result_df = df[selected_columns]
                return result_df

            except Exception as e:
                print(f"Request error: {e}")
                return None

        except Exception as e:
            print(f"Error querying data: {e}")
            return None

        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to create the database connection.")
        return None
