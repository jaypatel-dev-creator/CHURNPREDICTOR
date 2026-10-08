import warnings
import pandas as pd
from app.models.loader import load_model
from app.core.config import get_settings


def predict_churn(features: dict) -> dict:
    """Score one customer.

    `features` must be keyed by the model's training column names
    (e.g. "Number of Dependents"), which CustomerFeatures.model_dump(by_alias=True) produces.
    """
    model = load_model()
    settings = get_settings()
    threshold = settings.churn_threshold
    high_risk_threshold = settings.high_risk_threshold

    input_df = pd.DataFrame([features])

    # the pipeline's ColumnTransformer drops column names internally — LightGBM warns
    # about missing feature names as a result. the prediction is correct; suppress the noise.
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="X does not have valid feature names")
        proba = model.predict_proba(input_df)[0][1]

    prediction = "Churned" if proba >= threshold else "Stayed"

    if proba >= high_risk_threshold:
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