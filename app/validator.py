from fastapi import HTTPException

def validate_input(data):
    if "tenure" not in data:
        raise HTTPException(status_code=400, detail="tenure missing")
    if "MonthlyCharges" not in data:
        raise HTTPException(status_code=400, detail="MonthlyCharges missing")
    return data