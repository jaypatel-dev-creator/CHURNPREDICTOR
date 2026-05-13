

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routes.predict import router
from app.models.loader import load_model
from dotenv import load_dotenv
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model() ## load the model on application startup
    yield

origins = [
    "https://churnpredictor-zeta.vercel.app", # deployed link of frontend on vercel. 
]

if os.getenv("ENV") == "development": # for local , we set env to development
    origins.append("http://localhost:5173")

app = FastAPI(
    title="Customer Churn Prediction API",
    description="Predicts customer churn probability for a telecom provider",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # allow only localhost and deployed frontend origin. 
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    try:
        model = load_model()
        return {"status": "ok", "model": "loaded"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Model not loaded: {str(e)}")

app.include_router(router)