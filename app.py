import pickle
from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

# =====================================================
# 🔥 LOAD TRAINED FILES (MUST BE FITTED IN NOTEBOOK)
# =====================================================
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pickle

# create scaler
scaler = StandardScaler()

# ✅ FIT FIRST (MOST IMPORTANT LINE)
X_scaled = scaler.fit_transform(X)

# train model
rf = RandomForestClassifier()
rf.fit(X_scaled, y)

# ✅ SAVE AFTER FITTING
pickle.dump(scaler, open("scaling.pkl", "wb"))
pickle.dump(rf, open("churn_model.sav", "wb"))


# =====================================================
# Home Route
# =====================================================
@app.route('/')
def home():
    return render_template('home.html')


# =====================================================
# API Prediction (JSON)
# =====================================================
@app.route('/predict_api', methods=['POST'])
def predict_api():
    try:
        if scaler is None or rf is None:
            return jsonify({"error": "Model or scaler not loaded properly"})

        data = request.get_json(force=True)
        values = list(data.values())

        arr = np.array(values).reshape(1, -1)
        scaled = scaler.transform(arr)
        output = rf.predict(scaled)[0]

        return jsonify({"prediction": int(output)})

    except Exception as e:
        return jsonify({"error": str(e)})


# =====================================================
# Web Form Prediction
# =====================================================
@app.route('/predict', methods=['POST'])
def predict():
    try:
        if scaler is None or rf is None:
            return render_template(
                "home.html",
                prediction_text="Model not loaded properly."
            )

        form = request.form.to_dict()

        # ===== manual encoding (must match training) =====
        telecom_map = {"Airtel": 0, "Jio": 1, "Vi": 2}
        gender_map = {"Male": 0, "Female": 1}
        city_map = {"Bengaluru": 0, "Hyderabad": 1, "Chennai": 2}
        state_map = {"Karnataka": 0, "Telangana": 1, "Tamil Nadu": 2}

        data = [
            float(form["Age"]),
            float(form["pincode"]),
            float(form["Num_dependents"]),
            float(form["estimated_salary"]),
            float(form["calls_made"]),
            float(form["sms_sent"]),
            float(form["data_use"]),
            float(form["tenure_days"]),
            telecom_map.get(form["telecom_partner"], 0),
            gender_map.get(form["gender"], 0),
            city_map.get(form["city"], 0),
            state_map.get(form["state"], 0),
        ]

        final_input = scaler.transform(np.array(data).reshape(1, -1))
        output = rf.predict(final_input)[0]

        result_text = (
            "Customer is likely to churn ❌"
            if output == 1
            else "Customer is not likely to churn ✅"
        )

        return render_template(
            "home.html",
            prediction_text=result_text
        )

    except Exception as e:
        return render_template(
            "home.html",
            prediction_text=f"Error: {e}"
        )


# =====================================================
# Run App
# =====================================================
if __name__ == "__main__":
    app.run(debug=True)