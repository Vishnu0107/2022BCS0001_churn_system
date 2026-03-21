from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict():
    response = client.post("/predict", json={
        "tenure": 5,
        "MonthlyCharges": 80
    })
    assert response.status_code == 200