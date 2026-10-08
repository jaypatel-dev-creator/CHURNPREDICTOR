from functools import lru_cache
from pathlib import Path
import joblib
from app.core.config import get_settings


@lru_cache(maxsize=1)
def load_model():
    settings = get_settings()
   
    model_path = Path(__file__).parent.parent.parent / settings.model_path # moving to backend folder cause churn_model.plk lives there and so settings.model_path works, without that , it will crash
    return joblib.load(model_path)