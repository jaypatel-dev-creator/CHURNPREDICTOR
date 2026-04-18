from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import CustomerFeatures, PredictionResponse
from model import predict_churn, load_model

app = FastAPI(
    title="Customer Churn Prediction API",
    description="Predicts customer churn probability for a telecom provider",
    version="1.0.0"
)

## CORS — allows React frontend to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## preload model at startup
@app.on_event("startup")
async def startup_event():
    load_model()

## health check
@app.get("/health")
def health():
    return {"status": "ok"}

## prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
def predict(customer: CustomerFeatures):
    try:
        features = customer.model_dump()
        result = predict_churn(features)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))