import unicodedata
from database import create_connection

def normalize_team_names(team_name):
    return unicodedata.normalize('NFD', team_name).encode('ascii', 'ignore').decode('utf-8').lower().strip()

def get_match_id(home_team, away_team, tournament_name):
    # Normalize team names
    normalized_home_team = normalize_team_names(home_team)
    normalized_away_team = normalize_team_names(away_team)
    normalized_tournament_name = normalize_team_names(tournament_name)

def get_shots(home_team, away_team, date):
    connection = create_connection()
    