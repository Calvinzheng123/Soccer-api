from LionAPI.services import get_shots

if __name__ == "__main__":
    home_team = "Liverpool"
    away_team = "Chelsea"
    match_date = "2024-10-20"  

    result_df = get_shots(home_team, away_team, match_date)

    if result_df is not None:
        print("Shots data retrieved successfully:")
        print(result_df)
    else:
        print("Failed to retrieve shots data.")