from functools import lru_cache
from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    app_env: str = "development"                    # prod: set to "production" on Render dashboard
    frontend_url: str = "http://localhost:5173"     # prod: set to deployed Vercel URL on Render dashboard

    # Model
    model_path: str = "churn_model.pkl"             # path to the serialized LightGBM pipeline artifact
    churn_threshold: float = 0.5784                 # decision boundary tuned via Precision-Recall curve — Medium Risk floor
    high_risk_threshold: float = 0.75               # probabilities at or above this are classified as High Risk

    @field_validator("churn_threshold", "high_risk_threshold")
    @classmethod
    def threshold_must_be_valid(cls, v: float) -> float:
        if not (0.0 <= v <= 1.0):
            raise ValueError(f"threshold must be between 0.0 and 1.0, got {v}")
        return v

    @model_validator(mode="after")
    def high_risk_must_exceed_churn_threshold(self) -> "Settings":
        if self.high_risk_threshold <= self.churn_threshold:
            raise ValueError(
                f"high_risk_threshold ({self.high_risk_threshold}) must be greater than "
                f"churn_threshold ({self.churn_threshold})"
            )
        return self

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()