import os
import sqlite3
from pathlib import Path

import pandas as pd


DEFAULT_DB_PATH = Path(__file__).resolve().parents[2] / "lionapi.db"


def get_database_path() -> Path:
    return Path(os.getenv("LIONAPI_DB_PATH", DEFAULT_DB_PATH)).expanduser().resolve()


def create_connection():
    db_path = get_database_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    initialize_database(connection)
    return connection


def initialize_database(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            home_team TEXT NOT NULL,
            away_team TEXT NOT NULL,
            event_id INTEGER PRIMARY KEY,
            home_score INTEGER NOT NULL,
            away_score INTEGER NOT NULL,
            tournament_name TEXT NOT NULL,
            season_id INTEGER NOT NULL,
            tournament_id INTEGER NOT NULL,
            event_date TEXT NOT NULL
        )
        """
    )
    connection.commit()
    cursor.close()


def insert_event(event):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT OR REPLACE INTO events (
                home_team,
                away_team,
                event_id,
                home_score,
                away_score,
                tournament_name,
                season_id,
                tournament_id,
                event_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event["homeTeam"],
                event["awayTeam"],
                event["eventID"],
                event["homeScore"],
                event["awayScore"],
                event["tournamentName"],
                event["seasonID"],
                event["tournamentID"],
                event["eventDate"],
            ),
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def query_events(start_date: str, end_date: str):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT
                home_team,
                away_team,
                event_id,
                home_score,
                away_score,
                tournament_name,
                season_id,
                tournament_id,
                event_date
            FROM events
            WHERE event_date BETWEEN ? AND ?
            ORDER BY event_date, event_id
            """,
            (start_date, end_date),
        )
        result = [dict(row) for row in cursor.fetchall()]
        return pd.DataFrame(result)
    finally:
        cursor.close()
        connection.close()
