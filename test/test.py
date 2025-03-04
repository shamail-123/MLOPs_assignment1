import requests
import joblib
import pandas as pd

# Base URL for the Flask app
BASE_URL = "http://127.0.0.1:5000"

# Load the trained model and encoders for test data preparation
model = joblib.load("../model.pkl")
scaler = joblib.load("../scaler.pkl")
label_encoder = joblib.load("../label_encoder.pkl")


def get_sample_input():
    """Returns sample input data for testing."""
    return {
        "time_occ": 1200,
        "vict_age": 30,
        "premis_cd": 101,
        "weapon_used_cd": 400,
        "lat": 34.0522,
        "lon": -118.2437,
    }


def test_home_route():
    """Tests if the home page loads correctly."""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert "LA Crime Prediction System" in response.text
    assert "Predict Crime" in response.text


def test_prediction():
    """Tests the prediction endpoint with valid input."""
    input_data = get_sample_input()
    response = requests.post(f"{BASE_URL}/", data=input_data)
    assert response.status_code == 200
    assert "Predicted Crime Category:" in response.text

    # Verify the model prediction
    features = ["TIME OCC", "Vict Age", "Premis Cd", "Weapon Used Cd", "LAT", "LON"]
    df_input = pd.DataFrame([list(input_data.values())], columns=features)
    df_input_scaled = scaler.transform(df_input)
    prediction = model.predict(df_input_scaled)
    predicted_class = label_encoder.inverse_transform(prediction)[0]

    assert predicted_class in response.text


def test_invalid_input():
    """Tests the prediction endpoint with invalid input."""
    invalid_input = {
        "time_occ": "invalid",  # Invalid type
        "vict_age": 30,
        "premis_cd": 101,
        "weapon_used_cd": 400,
        "lat": 34.0522,
        "lon": -118.2437,
    }

    response = requests.post(f"{BASE_URL}/", data=invalid_input)
    assert response.status_code == 200
    assert "Error in input values" in response.text


# Ensure a newline at the end of the file
