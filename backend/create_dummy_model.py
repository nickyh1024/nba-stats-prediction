import pickle
import numpy as np
from sklearn.linear_model import LinearRegression

# Features: [age, mpg]
X = np.array([
    [28, 34.1],  # Jokic
    [35, 31.4],  # Curry
    [24, 34.8],  # Luka
    [36, 35.2],  # Durant
    [29, 34.6],  # Giannis
])

# Target: [FG%, FT%, 3PM, PTS, REB, AST, STL, BLK, TO]
y = np.array([
    [0.575, 0.822, 1.8, 26.4, 12.7, 10.1, 1.5, 0.6, 3.2],  # Jokic
    [0.458, 0.925, 4.9, 28.0, 4.8, 6.2, 1.1, 0.5, 3.0],   # Curry
    [0.464, 0.774, 3.6, 29.1, 9.0, 8.1, 1.8, 0.5, 3.5],   # Luka
    [0.516, 0.840, 2.2, 26.6, 6.6, 4.9, 0.8, 1.2, 3.3],   # Durant
    [0.614, 0.582, 0.6, 29.1, 11.8, 5.7, 0.7, 1.0, 3.4],  # Giannis
])

# Train model
model = LinearRegression().fit(X, y)

# Save model
with open("nba_model.pkl", "wb") as f:
    pickle.dump(model, f)
