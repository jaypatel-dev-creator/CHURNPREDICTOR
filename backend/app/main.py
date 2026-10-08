from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.predict import router
from app.models.loader import load_model
from app.core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()  # load the model on application startup
    yield


settings = get_settings()

app = FastAPI(
    title="Customer Churn Prediction API",
    description="Predicts customer churn probability for a telecom provider",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],  
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(router)