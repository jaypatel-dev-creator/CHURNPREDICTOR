import pandas as pd
from app.models.loader import load_model
from app.core.config import get_settings

# pydantic schema used underscore in fields cause pydantic dont allows spaces in field names,
# but model was trained on spaces in column names, so COLUMN_MAP remaps underscore_keys to
# spaced column names — otherwise the model pipeline won't recognise the input features.
COLUMN_MAP = {
    "Gender": "Gender",
    "Age": "Age",
    "Married": "Married",
    "Number_of_Dependents": "Number of Dependents",
    "Number_of_Referrals": "Number of Referrals",
    "Tenure_in_Months": "Tenure in Months",
    "Offer": "Offer",
    "Phone_Service": "Phone Service",
    "Avg_Monthly_Long_Distance_Charges": "Avg Monthly Long Distance Charges",
    "Multiple_Lines": "Multiple Lines",
    "Internet_Service": "Internet Service",
    "Internet_Type": "Internet Type",
    "Avg_Monthly_GB_Download": "Avg Monthly GB Download",
    "Online_Security": "Online Security",
    "Online_Backup": "Online Backup",
    "Device_Protection_Plan": "Device Protection Plan",
    "Premium_Tech_Support": "Premium Tech Support",
    "Streaming_TV": "Streaming TV",
    "Streaming_Movies": "Streaming Movies",
    "Streaming_Music": "Streaming Music",
    "Unlimited_Data": "Unlimited Data",
    "Contract": "Contract",
    "Paperless_Billing": "Paperless Billing",
    "Payment_Method": "Payment Method",
    "Monthly_Charge": "Monthly Charge",
    "Total_Charges": "Total Charges",
    "Total_Refunds": "Total Refunds",
    "Total_Extra_Data_Charges": "Total Extra Data Charges",
    "Total_Long_Distance_Charges": "Total Long Distance Charges",
    "Total_Revenue": "Total Revenue",
}


def predict_churn(features: dict) -> dict:
    model = load_model()
    settings = get_settings()
    threshold = settings.churn_threshold

    mapped = {COLUMN_MAP[k]: v for k, v in features.items()}
    # dict does not represent rows and cols — DataFrame wraps input into the shape
    # the sklearn pipeline expects (single-row, named columns matching training data)
    input_df = pd.DataFrame([mapped])

    # predict_proba returns [[prob_class_0, prob_class_1]] — index [0][1] gives churn probability
    proba = model.predict_proba(input_df)[0][1]
    prediction = "Churned" if proba >= threshold else "Stayed"

    if proba >= 0.75:
        risk_level = "High Risk"
    elif proba >= threshold:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"

    return {
        "churn_probability": round(float(proba), 4),
        "prediction": prediction,
        "risk_level": risk_level,
    }