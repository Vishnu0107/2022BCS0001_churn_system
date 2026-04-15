import joblib
import pandas as pd
import numpy as np
import os

ARTIFACTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml_artifacts')

class ChurnModel:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.le_dict = None
        self.features = None
        self.load_artifacts()

    def load_artifacts(self):
        try:
            self.model = joblib.load(os.path.join(ARTIFACTS_DIR, 'model.joblib'))
            self.scaler = joblib.load(os.path.join(ARTIFACTS_DIR, 'scaler.joblib'))
            self.le_dict = joblib.load(os.path.join(ARTIFACTS_DIR, 'label_encoders.joblib'))
            self.features = joblib.load(os.path.join(ARTIFACTS_DIR, 'features.joblib'))
        except Exception as e:
            print(f"Could not load ML artifacts: {e}")

    def predict(self, data_dict):
        if not self.model:
            raise Exception("Model not loaded")

        df = pd.DataFrame([data_dict])
        
        # Ensure all columns exist
        for col in self.features:
            if col not in df.columns:
                # Provide default values if missing
                if col == 'TotalCharges':
                    df[col] = df.get('MonthlyCharges', 0) * df.get('tenure', 0)
                elif col in self.le_dict:
                    df[col] = "No"  # Categorical
                else:
                    df[col] = 0  # Numeric (SeniorCitizen, tenure, etc.)

        df = df[self.features]
        
        # Preprocess TotalCharges
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)

        # Apply label encoders
        for col, le in self.le_dict.items():
            if col in df.columns:
                # Handle unknown categories by mapping to the mode or first class
                # Here we safely transform known classes, or use fallback
                # For simplicity, we assume input categories match training data
                try:
                    df[col] = le.transform(df[col].astype(str))
                except ValueError:
                    df[col] = 0 # Default to 0 if unseen category

        X_scaled = self.scaler.transform(df)
        pred = self.model.predict(X_scaled)[0]
        prob = self.model.predict_proba(X_scaled)[0][1]

        risk = "High Risk" if prob > 0.7 else "Medium Risk" if prob > 0.4 else "Low Risk"
        
        return {
            "prediction": int(pred),
            "probability": float(prob),
            "risk": risk
        }

ml_model = ChurnModel()
