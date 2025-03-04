from flask import Flask, request, render_template
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib

app = Flask(__name__)

# Load and preprocess dataset
def load_and_preprocess_data():
    df = pd.read_csv("dataset.csv")  
    
    # Handling missing values
    df = df.dropna()
    
    # Selecting features
    features = ["TIME OCC", "Vict Age", "Premis Cd", "Weapon Used Cd", "LAT", "LON"]
    target = "Crm Cd Desc"
    df = df[features + [target]]
    
    # Encoding target variable
    le = LabelEncoder()
    df[target] = le.fit_transform(df[target])
    
    # Splitting data
    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scaling numerical features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save model and encoders
    joblib.dump(model, "model.pkl")
    joblib.dump(scaler, "scaler.pkl")
    joblib.dump(le, "label_encoder.pkl")

# Run preprocessing and model training once
load_and_preprocess_data()

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None  # Default: No prediction
    
    if request.method == "POST":
        try:
            # Get user input from the form
            time_occ = int(request.form["time_occ"])
            vict_age = int(request.form["vict_age"])
            premis_cd = int(request.form["premis_cd"])
            weapon_used_cd = int(request.form["weapon_used_cd"])
            lat = float(request.form["lat"])
            lon = float(request.form["lon"])

            # Load trained model and encoders
            model = joblib.load("model.pkl")
            scaler = joblib.load("scaler.pkl")
            label_encoder = joblib.load("label_encoder.pkl")

            # Convert input to DataFrame
            features = ["TIME OCC", "Vict Age", "Premis Cd", "Weapon Used Cd", "LAT", "LON"]
            df_input = pd.DataFrame([[time_occ, vict_age, premis_cd, weapon_used_cd, lat, lon]], columns=features)

            # Scale input
            df_input = scaler.transform(df_input)

            # Predict
            prediction = model.predict(df_input)
            predicted_class = label_encoder.inverse_transform(prediction)[0]
        except Exception as e:
            predicted_class = "Error in input values"

        return render_template("index.html", prediction=predicted_class)

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
