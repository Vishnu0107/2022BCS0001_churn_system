def evaluate_risk(data):
    tenure = int(data["tenure"])
    monthly = float(data["MonthlyCharges"])

    if tenure < 6 and monthly > 70:
        return "High Risk"
    elif tenure < 12:
        return "Medium Risk"
    else:
        return "Low Risk"