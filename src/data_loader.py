import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats
import time
import os

def get_season_stats(season_str):
    """Fetch player per-game stats for a given NBA season."""
    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season_str,
        season_type_all_star='Regular Season',
        per_mode_detailed='PerGame'
    )
    df = stats.get_data_frames()[0]
    df['SEASON'] = season_str
    return df

def fetch_multiple_seasons(start_year=2017, end_year=2023):
    """Fetch stats from start_year to end_year (inclusive) and return combined DataFrame."""
    season_list = [f"{year}-{str(year+1)[-2:]}" for year in range(start_year, end_year + 1)]
    all_data = []
    
    for season in season_list:
        print(f"Fetching season {season}...")
        df = get_season_stats(season)
        all_data.append(df)
        time.sleep(1)  # Pause to avoid rate limits

    full_df = pd.concat(all_data, ignore_index=True)
    return full_df



def save_to_csv(df, path="../data/player_stats.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)  # <-- this line creates the folder!
    df.to_csv(path, index=False)
    print(f"Saved data to {path}")


