from functools import lru_cache
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    frontend_url: str = "http://localhost:5173"     # prod: set to deployed Vercel URL on Render dashboard

    # Model
    model_path: str = "churn_model.pkl"             # path to the serialized LightGBM pipeline artifact

    # decision boundary tuned via Precision-Recall curve — Medium Risk floor
    churn_threshold: float = Field(default=0.5784, ge=0.0, le=1.0)

    # probabilities at or above this are classified as High Risk
    high_risk_threshold: float = Field(default=0.75, ge=0.0, le=1.0)

    # cross-field rule: needs both values, so it can't be a per-field constraint
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