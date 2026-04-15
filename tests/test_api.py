from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict():
    response = client.post("/predict", json={
        "tenure": 5,
        "MonthlyCharges": 80
    })
    assert response.status_code == 200

def test_high_risk_output():
    response = client.post("/predict", json={
        "tenure": 5,
        "MonthlyCharges": 80
    })
    assert response.status_code == 200
    assert response.json()["risk"] == "High Risk"


def test_medium_risk_output():
    response = client.post("/predict", json={
        "tenure": 10,
        "MonthlyCharges": 50
    })
    assert response.status_code == 200
    assert response.json()["risk"] == "Medium Risk"


def test_low_risk_output():
    response = client.post("/predict", json={
        "tenure": 20,
        "MonthlyCharges": 40
    })
    assert response.status_code == 200
    assert response.json()["risk"] == "Low Risk"


def test_missing_tenure():
    response = client.post("/predict", json={
        "MonthlyCharges": 50
    })
    assert response.status_code == 400


def test_missing_monthly_charges():
    response = client.post("/predict", json={
        "tenure": 10
    })
    assert response.status_code == 400


def test_ml_predict():
    response = client.post("/ml_predict", json={
        "tenure": 10,
        "MonthlyCharges": 20,
        "Contract": "Month-to-month",
        "InternetService": "Fiber optic"
    })
    assert response.status_code == 200
    assert "risk" in response.json()
    assert "probability" in response.json()


def test_ml_batch_predict():
    response = client.get("/ml_batch_predict?n=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total_records"] == 10
    assert len(data["results"]) == 10
