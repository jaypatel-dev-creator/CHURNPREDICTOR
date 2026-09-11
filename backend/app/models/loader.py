from functools import lru_cache
from pathlib import Path
import joblib
from app.core.config import get_settings


@lru_cache(maxsize=1)
def load_model():
    settings = get_settings()
    # resolve relative to backend root (where churn_model.pkl lives)
    model_path = Path(__file__).parent.parent.parent / settings.model_path
    return joblib.load(model_path)