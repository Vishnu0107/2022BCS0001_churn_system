from app.validator import validate_input
from app.rules import evaluate_risk
from app.database import SessionLocal
from app.models import Customer
from fastapi import FastAPI, Depends
from app.validator import validate_input
from app.rules import evaluate_risk
from app.database import SessionLocal
from app.models import Customer
import logging
from prometheus_fastapi_instrumentator import Instrumentator 

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