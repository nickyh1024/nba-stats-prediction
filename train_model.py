import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor

# Load the dataset
df = pd.read_csv("nba_stats_2015_to_2024.csv")

# Drop rows with missing values
df.dropna(inplace=True)

# Input features from previous season
X = df[[
    "AGE_prev", "MPG_prev", "FG%_prev", "FT%_prev", "3PM_prev",
    "PTS_prev", "REB_prev", "AST_prev", "STL_prev", "BLK_prev", "TO_prev"
]]

# Targets: next-season stats to predict
y = df[[
    "FG%_next", "FT%_next", "3PM_next", "PTS_next", "REB_next",
    "AST_next", "STL_next", "BLK_next", "TO_next"
]]

# Optional: Train/test split just to evaluate performance
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(
    n_estimators=100,     # number of trees
    max_depth=None,       # let trees grow fully
    random_state=42,
    n_jobs=-1             # use all CPU cores
)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"✅ Model trained. RMSE: {rmse:.3f}")

# Save model
with open("backend/nba_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model saved to backend/nba_model.pkl")
