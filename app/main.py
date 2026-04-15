from fastapi import FastAPI, Depends
from app.validator import validate_input
from app.rules import evaluate_risk
from app.database import SessionLocal
from app.models import Customer
import logging
from prometheus_fastapi_instrumentator import Instrumentator 
import numpy as np
import time
from app.ml_model import ml_model

app = FastAPI()
Instrumentator().instrument(app).expose(app)
logging.basicConfig(level=logging.INFO)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/predict")
def predict(data: dict, db=Depends(get_db)):
    data = validate_input(data)
    risk = evaluate_risk(data)

    customer = Customer(
        tenure=data["tenure"],
        monthly_charges=data["MonthlyCharges"],
        contract=data.get("Contract", "")
    )
    db.add(customer)
    db.commit()

    logging.info(f"Prediction: {risk}")

    return {"risk": risk}

@app.post("/ml_predict")
def ml_predict(data: dict, db=Depends(get_db)):
    try:
        result = ml_model.predict(data)
        
        customer = Customer(
            tenure=data.get("tenure", 0),
            monthly_charges=data.get("MonthlyCharges", 0.0),
            contract=data.get("Contract", "")
        )
        db.add(customer)
        db.commit()
        
        logging.info(f"ML Prediction: {result['risk']} (Prob: {result['probability']:.2f})")
        return result
    except Exception as e:
        logging.error(f"ML Prediction error: {e}")
        return {"error": str(e)}


# Generate & Display Dataset
@app.get("/dataset")
def get_dataset(n: int = 10):
    start = time.time()
    np.random.seed(42)
    data = [
        {
            "id": i,
            "tenure": int(np.random.randint(1, 72)),
            "MonthlyCharges": float(np.random.uniform(20, 120))
        }
        for i in range(n)
    ]

    end = time.time()

    return {
        "total_records": n,
        "execution_time_seconds": round(end - start, 4),
        "data": data
    }

# Batch Prediction 
@app.get("/batch_predict")
def batch_predict(n: int = 10):
    start = time.time()

    np.random.seed(42)

    data = [
        {
            "id": i,
            "tenure": int(np.random.randint(1, 72)),
            "MonthlyCharges": float(np.random.uniform(20, 120))
        }
        for i in range(n)
    ]

    results = []
    summary = {"High Risk": 0, "Medium Risk": 0, "Low Risk": 0}

    for d in data:
        risk = evaluate_risk(d)

        results.append({
            "id": d["id"],
            "tenure": d["tenure"],
            "MonthlyCharges": d["MonthlyCharges"],
            "risk": risk
        })

        summary[risk] += 1

    end = time.time()

    return {
        "total_records": n,
        "execution_time_seconds": round(end - start, 4),
        "summary": summary,
        "results": results
    }

# ML Batch Prediction 
@app.get("/ml_batch_predict")
def ml_batch_predict(n: int = 10):
    start = time.time()

    np.random.seed(42)

    data = [
        {
            "id": i,
            "tenure": int(np.random.randint(1, 72)),
            "MonthlyCharges": float(np.random.uniform(20, 120)),
            "Contract": np.random.choice(["Month-to-month", "One year", "Two year"]),
            "InternetService": np.random.choice(["DSL", "Fiber optic", "No"])
        }
        for i in range(n)
    ]

    results = []
    summary = {"High Risk": 0, "Medium Risk": 0, "Low Risk": 0}

    for d in data:
        res = ml_model.predict(d)
        risk = res["risk"]

        results.append({
            "id": d["id"],
            "tenure": d["tenure"],
            "MonthlyCharges": d["MonthlyCharges"],
            "risk": risk,
            "probability": round(res["probability"], 4)
        })

        summary[risk] += 1

    end = time.time()

    return {
        "total_records": n,
        "execution_time_seconds": round(end - start, 4),
        "summary": summary,
        "results": results
    }