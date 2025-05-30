# test_predict.py
import requests

res = requests.post("http://localhost:5000/predict", json={"features": [28, 34.1]})
print(res.json())
