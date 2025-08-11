# build_dataset.py
import pandas as pd
from pathlib import Path
import re
import sys

# === Paths (anchored to this script's folder) ===
BASE_DIR = Path(__file__).resolve().parent          # .../nba-stats-prediction/data
FOLDER   = BASE_DIR                                  # CSVs live here
OUT      = BASE_DIR / "player_seasons.csv"           # merged output

print("Script dir:", BASE_DIR)
print("Looking for CSVs in:", FOLDER)

def end_year_from_name(name: str) -> int:
    """
    Extract season end year from filenames like:
    '2017-2018_stats.csv' -> 2018
    '2023-2024_stats.csv' -> 2024
    Also supports 'NBA_2024_*.csv' -> 2024
    """
    m = re.search(r'(\d{4})-(\d{4})', name)
    if m:
        return int(m.group(2))
    m = re.search(r'NBA_(\d{4})', name)
    if m:
        return int(m.group(1))
    raise ValueError(f"Cannot parse season from filename: {name}")

def clean_br_df(df: pd.DataFrame, season_end: int) -> pd.DataFrame:
    # Remove repeated header rows (BR sometimes repeats 'Rk' row)
    if 'Rk' in df.columns:
        df = df[df['Rk'] != 'Rk']

    # Standardize columns we care about
    new_cols = []
    for c in df.columns:
        c2 = c.strip()
        c2 = (c2.replace('Player','player_name')
                 .replace('Age','age')
                 .replace('Pos','pos')
                 .replace('Tm','team'))
        new_cols.append(c2)
    df.columns = new_cols

    df['season'] = season_end

    # Clean player names (drop asterisks)
    if 'player_name' in df.columns:
        df['player_name'] = (
            df['player_name'].astype(str)
            .str.replace(r'\*', '', regex=True)
            .str.strip()
        )

    # Best‑effort numeric conversion
    for col in df.columns:
        if col not in ['player_name', 'team', 'pos', 'season']:
            df[col] = pd.to_numeric(df[col], errors='ignore')
    return df

# --- Find CSVs ---
csv_paths = sorted([p for p in FOLDER.glob("*.csv") if p.name != OUT.name])
print(f"Found {len(csv_paths)} files:")
for p in csv_paths:
    print(" •", p.name)

if not csv_paths:
    print("\nNo CSVs found in the data folder. Make sure your season files are here, e.g.:")
    print("  2017-2018_stats.csv, 2018-2019_stats.csv, ...")
    sys.exit(1)

# --- Read & clean each file ---
all_dfs = []
for p in csv_paths:
    try:
        raw = pd.read_csv(p)
    except Exception as e:
        print(f"Failed to read {p.name}: {e}")
        continue
    try:
        season_end = end_year_from_name(p.name)
        df = clean_br_df(raw, season_end)
        all_dfs.append(df)
    except Exception as e:
        print(f"Skipping {p.name}: {e}")

if not all_dfs:
    print("No valid CSVs after cleaning. Check file formats/headers.")
    sys.exit(1)

# --- Merge all seasons ---
big = pd.concat(all_dfs, ignore_index=True)

# Prefer 'TOT' row when a player was traded (keep TOT, otherwise keep individual team rows)
if {'player_name','season','team'}.issubset(big.columns):
    has_tot_flag = big.assign(is_tot=(big['team'] == 'TOT'))
    keep_tot = has_tot_flag[has_tot_flag['is_tot']]
    no_tot = (has_tot_flag.groupby(['player_name','season'])['is_tot'].transform('max') == 0)
    keep_notot = has_tot_flag[no_tot]
    big = pd.concat([keep_tot, keep_notot], ignore_index=True).drop(columns=['is_tot'])

# Lightweight surrogate id (replace with real ids later if you have them)
big['player_id'] = (
    big['player_name'].astype(str).str.lower().str.replace(r'[^a-z]', '', regex=True)
    + "_" + big['season'].astype(str)
).factorize()[0]

# Reorder convenience columns
front = [c for c in ['player_id','player_name','season','age','team','pos'] if c in big.columns]
big = big[front + [c for c in big.columns if c not in front]]

# Save
big.to_csv(OUT, index=False)
print(f"\nWrote: {OUT}  shape: {big.shape}")
