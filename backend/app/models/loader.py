from functools import lru_cache
from pathlib import Path
import joblib

MODEL_PATH = Path(__file__).parent.parent.parent / "churn_model.pkl"

@lru_cache(maxsize=1)
def load_model():
    return joblib.load(MODEL_PATH)