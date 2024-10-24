import mysql.connector
from mysql.connector import Error
import pandas as pd

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',    
            password='Zheng123',  
            database='soccer_api'      
        )
        if connection.is_connected():
            print("Connection successful")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def insert_event(event):
    connection = create_connection()
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO events (home_team, away_team, event_id, home_score, away_score,
                                    tournament_name, season_id, tournament_id, event_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (event['homeTeam'], event['awayTeam'], event['eventID'],
                  event['homeScore'], event['awayScore'], event['tournamentName'],
                  event['seasonID'], event['tournamentID'], event['eventDate']))
            connection.commit()
        except Error as e:
            print(f"Error inserting data: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to create the database connection.")
        
def query_events(start_date: str, end_date: str):
    connection = create_connection()
    if connection is not None:
        cursor = connection.cursor(dictionary=True)  # Fetch results as dictionaries
        try:
            query = """
                SELECT home_team, away_team, event_id, home_score, away_score,
                       tournament_name, season_id, tournament_id, event_date
                FROM events
                WHERE event_date BETWEEN %s AND %s;
            """
            cursor.execute(query, (start_date, end_date))
            result = cursor.fetchall()
            
            # Convert the result into a DataFrame
            df = pd.DataFrame(result)
            return df
        except Error as e:
            print(f"Error querying data: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to create the database connection.")
        return None

