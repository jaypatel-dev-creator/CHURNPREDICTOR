from fastapi import APIRouter, HTTPException
from app.schemas.churn import CustomerFeatures, PredictionResponse
from app.services.predictor import predict_churn

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict(customer: CustomerFeatures):
    try:
        # converting pydantic object to py dictionary — predict_churn expects a dict
        features = customer.model_dump()
        result = predict_churn(features)
        return result
    except ValueError as e:
        # raised by predict_churn when a feature key has no column mapping
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))