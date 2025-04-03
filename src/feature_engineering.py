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

    return merged


