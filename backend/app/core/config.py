from functools import lru_cache
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    app_env: str = "development"                    # prod: set to "production" on Render dashboard
    frontend_url: str = "http://localhost:5173"     # prod: set to deployed Vercel URL on Render dashboard

    # Model
    model_path: str = "churn_model.pkl"             # path to the serialized LightGBM pipeline artifact
    churn_threshold: float = 0.5784                 # decision threshold tuned via Precision-Recall curve

    @field_validator("churn_threshold")
    @classmethod
    def threshold_must_be_valid(cls, v: float) -> float:
        if not (0.0 <= v <= 1.0):
            raise ValueError(f"churn_threshold must be between 0.0 and 1.0, got {v}")
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()