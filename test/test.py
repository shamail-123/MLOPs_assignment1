import pytest
import requests
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Base URL for the Flask app
BASE_URL = "http://127.0.0.1:5000"

# Load the trained model and encoders for test data preparation
model = joblib.load("../model.pkl")
scaler = joblib.load("../scaler.pkl")
label_encoder = joblib.load("../label_encoder.pkl")

# Sample input data for testing
def get_sample_input():
    return {
        "time_occ": 1200,
        "vict_age": 30,
        "premis_cd": 101,
        "weapon_used_cd": 400,
        "lat": 34.0522,
        "lon": -118.2437,
    }

# Test the home route (GET request)
def test_home_route():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert "LA Crime Prediction System" in response.text  # Verify the page loads correctly
    assert "Predict Crime" in response.text  # Ensure the form button exists


# Test the prediction (POST request)
def test_prediction():
    # Prepare input data
    input_data = get_sample_input()

    # Send POST request to the Flask app
    response = requests.post(f"{BASE_URL}/", data=input_data)

    # Check if the response is successful
    assert response.status_code == 200

    # Check if the prediction result is displayed in the response
    assert "Predicted Crime Category:" in response.text

    # Verify the prediction logic
    # Convert input data to DataFrame
    features = ["TIME OCC", "Vict Age", "Premis Cd", "Weapon Used Cd", "LAT", "LON"]
    df_input = pd.DataFrame([list(input_data.values())], columns=features)

    # Scale input data
    df_input_scaled = scaler.transform(df_input)

    # Predict using the model
    prediction = model.predict(df_input_scaled)
    predicted_class = label_encoder.inverse_transform(prediction)[0]

    # Check if the predicted class is in the response
    assert predicted_class in response.text
# Test invalid input
def test_invalid_input():
    # Prepare invalid input data
    invalid_input = {
        "time_occ": "invalid",  # Invalid type (should be integer)
        "vict_age": 30,
        "premis_cd": 101,
        "weapon_used_cd": 400,
        "lat": 34.0522,
        "lon": -118.2437,
    }

    # Send POST request to the Flask app
    response = requests.post(f"{BASE_URL}/", data=invalid_input)

    # Check if the response is successful
    assert response.status_code == 200

    # Check if the error message is displayed
    assert "Error in input values" in response.text