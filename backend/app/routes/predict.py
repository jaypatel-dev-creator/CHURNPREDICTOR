import logging
from fastapi import APIRouter, HTTPException
from app.schemas.churn import CustomerFeatures, PredictionResponse
from app.services.predictor import predict_churn

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict(customer: CustomerFeatures):
    try:
        features = customer.model_dump(by_alias=True)
        return predict_churn(features)
    except Exception:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail="Internal server error")