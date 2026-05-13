from fastapi import APIRouter, HTTPException
from app.schemas.churn import CustomerFeatures, PredictionResponse
from app.services.predictor import predict_churn

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict(customer: CustomerFeatures):
    try:
        features = customer.model_dump() # converting pydantic object to py dictionary cause predict_churn expects dictionary 
        result = predict_churn(features)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    