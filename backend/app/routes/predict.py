import logging
from fastapi import APIRouter, HTTPException
from app.schemas.churn import CustomerFeatures, PredictionResponse
from app.services.predictor import predict_churn

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict(customer: CustomerFeatures):
    try:
        # by_alias=True renames fields to the model's training column names
        # (e.g. Number_of_Dependents -> "Number of Dependents"); predict_churn expects a dict
        features = customer.model_dump(by_alias=True)
        return predict_churn(features)
    except Exception:
        # full traceback goes to the server logs only; the client gets a generic message
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail="Internal server error")