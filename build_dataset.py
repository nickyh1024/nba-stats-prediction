import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats
import time

def get_season_stats(season):
    print(f"Fetching {season}...")
    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        per_mode_detailed="PerGame"
    )
    df = stats.get_data_frames()[0]
    df = df[[
        "PLAYER_ID", "PLAYER_NAME", "AGE", "GP", "MIN", "FG_PCT", "FT_PCT",
        "FG3M", "PTS", "REB", "AST", "STL", "BLK", "TOV"
    ]]
    df.columns = [
        "PLAYER_ID", "PLAYER_NAME", "AGE", "GP", "MPG", "FG%", "FT%",
        "3PM", "PTS", "REB", "AST", "STL", "BLK", "TO"
    ]
    df["SEASON"] = season
    time.sleep(1.5)  # avoid throttling
    return df

# Loop from 2015–16 through 2023–24
all_rows = []

for year in range(2015, 2024):
    season_1 = f"{year}-{str(year+1)[-2:]}"
    season_2 = f"{year+1}-{str(year+2)[-2:]}"
    
    try:
        df_1 = get_season_stats(season_1)
        df_2 = get_season_stats(season_2)
        
        # Merge consecutive seasons by PLAYER_ID
        merged = pd.merge(df_1, df_2, on="PLAYER_ID", suffixes=("_prev", "_next"))
        
        # Only keep necessary fields
        merged = merged[[
            "PLAYER_ID", "PLAYER_NAME_prev", "AGE_prev", "MPG_prev", "FG%_prev", "FT%_prev",
            "3PM_prev", "PTS_prev", "REB_prev", "AST_prev", "STL_prev", "BLK_prev", "TO_prev",
            "PTS_next", "AST_next", "REB_next", "FG%_next", "FT%_next", "3PM_next", "STL_next", "BLK_next", "TO_next"
        ]]
        
        all_rows.append(merged)
    except Exception as e:
        print(f"⚠️ Failed for {season_1} → {season_2}: {e}")

# Combine all rows
full_df = pd.concat(all_rows, ignore_index=True)
full_df.rename(columns={"PLAYER_NAME_prev": "PLAYER_NAME"}, inplace=True)

# Save
full_df.to_csv("nba_stats_2015_to_2024.csv", index=False)
print("✅ Dataset saved to nba_stats_2015_to_2024.csv")
