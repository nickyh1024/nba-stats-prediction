import pandas as pd
import json

# Load your dataset
df = pd.read_csv("nba_stats_2015_to_2024.csv")

# Drop rows with missing features
df.dropna(subset=[
    "AGE_prev", "MPG_prev", "FG%_prev", "FT%_prev", "3PM_prev",
    "PTS_prev", "REB_prev", "AST_prev", "STL_prev", "BLK_prev", "TO_prev"
], inplace=True)

# Keep the most recent row for each player (sorted by PLAYER_ID and season info)
df = df.sort_values(by=["PLAYER_ID"], ascending=True)

# For each PLAYER_ID, keep only the row with the latest AGE_prev (as a proxy for recency)
latest = df.sort_values(by="AGE_prev").drop_duplicates("PLAYER_ID", keep="last")

# Format into list of dicts for frontend
players = []
for _, row in latest.iterrows():
    players.append({
        "name": row["PLAYER_NAME"],
        "features": [
            row["AGE_prev"], row["MPG_prev"], row["FG%_prev"], row["FT%_prev"],
            row["3PM_prev"], row["PTS_prev"], row["REB_prev"], row["AST_prev"],
            row["STL_prev"], row["BLK_prev"], row["TO_prev"]
        ]
    })

# Save to JS
with open("frontend/src/players.js", "w") as f:
    f.write("export const players = " + json.dumps(players, indent=2) + ";")

print(f"✅ Exported {len(players)} recent players to frontend/src/players.js")
