import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, roc_auc_score, precision_score, recall_score, classification_report
import joblib
import os
import requests

DATA_URL = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
DATA_FILE = "Telco-Customer-Churn.csv"

def download_data():
    if not os.path.exists(DATA_FILE):
        print("Downloading dataset...")
        response = requests.get(DATA_URL)
        with open(DATA_FILE, 'wb') as f:
            f.write(response.content)
        print("Download complete.")
    else:
        print("Dataset already exists.")

def preprocess_and_train():
    df = pd.read_csv(DATA_FILE)
    
    # Preprocessing based on standard telco churn dataset
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'] = df['TotalCharges'].fillna(df['TotalCharges'].median())
    
    # Drop customerID
    df.drop('customerID', axis=1, inplace=True)
    
    # Target variable
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
    
    # Categorical encoding
    cat_cols = df.select_dtypes(include=['object']).columns
    le_dict = {}
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        le_dict[col] = le
        
    X = df.drop('Churn', axis=1)
    y = df['Churn']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Model
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train_scaled, y_train)
    
    # Evaluation
    predictions = model.predict(X_test_scaled)
    probabilities = model.predict_proba(X_test_scaled)[:, 1]
    
    f1 = f1_score(y_test, predictions)
    roc_auc = roc_auc_score(y_test, probabilities)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    
    print("--- ML Model Evaluation ---")
    print(f"F1 Score: {f1:.4f}")
    print(f"ROC-AUC: {roc_auc:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    
    # Save the artifacts
    os.makedirs('ml_artifacts', exist_ok=True)
    joblib.dump(model, 'ml_artifacts/model.joblib')
    joblib.dump(scaler, 'ml_artifacts/scaler.joblib')
    joblib.dump(le_dict, 'ml_artifacts/label_encoders.joblib')
    joblib.dump(list(X.columns), 'ml_artifacts/features.joblib')
    
    print("Model and preprocessing artifacts saved to ml_artifacts/")

if __name__ == "__main__":
    download_data()
    preprocess_and_train()
