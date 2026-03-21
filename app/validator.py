def validate_input(data):
    if "tenure" not in data:
        raise ValueError("tenure missing")
    if "MonthlyCharges" not in data:
        raise ValueError("MonthlyCharges missing")
    return data