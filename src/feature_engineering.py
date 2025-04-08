import pandas as pd

def prepare_training_data(df, target_columns):
    #sort by player and season
    df = df.sort_values(by=['PLAYER_ID', 'SEASON'])

    #shift target stats to next season
    shifted = df[['PLAYER_ID', 'SEASON'] + target_columns].copy()
    shifted[target_columns] = shifted[target_columns]
    shifted = shifted.rename(columns={col: f"NEXT_{col}" for col in target_columns})
    # keep same season string so we can join
    shifted['SEASON'] = shifted['SEASON']

    # merge original and shifted by PLAYER_ID + SEASON
    merged = pd.merge(
        df, 
        shifted,
        how='inner',
        on=['PLAYER_ID', 'SEASON'],
        suffixes=('', '_next')
    )

    team_features = []

    for idx, row in merged.iterrows(): 
        team = row["TEAM_ID"]
        season = row["SEASON"]
        player_id = row["PLAYER_ID"]

        teammates = merged [
            (merged["TEAM_ID"] == team) &
            (merged["SEASON"] == season) &
            (merged["PLAYER_ID"] != player_id)
        ]

        usage_sum = teammates["USG_PCT"].sum() if "USG_PCT" in merged.columns else 0 
        avg_usage = teammates["USG_PCT"].mean() if "USG_PCT" in merged.columns else 0
        avg_ast = teammates["AST"].mean()
        avg_reb = teammates["REB"].mean()

        team_features.append({
            "TEAM_USAGE_TOTAL": usage_sum,
            "TEAMMATE_AVG_USAGE": avg_usage,
            "TEAMMATE_AVG_AST": avg_ast,
            "TEAMMATE_AVG_REB": avg_reb
        })

    teammate_context = pd.DataFrame(team_features)
    merged = pd.concat([merged.reset_index(drop=True), teammate_context], axis=1)

    #add time aware features
    merged["SEASON_NUM"] = merged["SEASON"].apply(lambda x: int(x.split("-")[0]))

    #compute league-wide season averages for all target stats
    league_avg = merged.groupby("SEASON_NUM")[[f"NEXT_{col}" for col in target_columns]].mean().reset_index()
    league_avg.columns = ["SEASON_NUM"] + [f"LEAGUE_AVG_NEXT_{col}" for col in target_columns]

    merged = pd.merge(merged, league_avg, on="SEASON_NUM", how="left")

    return merged


