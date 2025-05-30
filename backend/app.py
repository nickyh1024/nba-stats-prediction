from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

print("Starting Flask app...")

app = Flask(__name__)
CORS(app)

# Load the dummy model
model = pickle.load(open("nba_model.pkl", "rb"))

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    features = np.array(data["features"]).reshape(1, -1)  # expects 11 inputs
    prediction = model.predict(features)[0]

    return jsonify({
        "fg_pct": float(prediction[0]),
        "ft_pct": float(prediction[1]),
        "three_pm": float(prediction[2]),
        "pts": float(prediction[3]),
        "reb": float(prediction[4]),
        "ast": float(prediction[5]),
        "stl": float(prediction[6]),
        "blk": float(prediction[7]),
        "to": float(prediction[8]),
    })



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)


@app.route("/")
def home():
    return "Server is working!"
