from fastapi import APIRouter, HTTPException
from app.schemas.churn import CustomerFeatures, PredictionResponse
from app.services.predictor import predict_churn

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict(customer: CustomerFeatures):
    try:
        # by_alias=True renames fields to the model's training column names
        # (e.g. Number_of_Dependents -> "Number of Dependents"); predict_churn expects a dict
        features = customer.model_dump(by_alias=True)
        return predict_churn(features)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))