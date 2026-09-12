# Customer Churn Predictor

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135.3-009688?logo=fastapi&logoColor=white)
![LightGBM](https://img.shields.io/badge/LightGBM-4.6.0-0175C2?logoColor=white)
![scikit--learn](https://img.shields.io/badge/scikit--learn-1.6.1-F7931E?logo=scikit-learn&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-Containerised-2496ED?logo=docker&logoColor=white)
![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?logo=render&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-Deployed-000000?logo=vercel&logoColor=white)

A full-stack ML inference application that predicts customer churn for a telecom provider. A pre-trained LightGBM pipeline is serialized as a joblib artifact and served via a FastAPI backend — containerized with Docker and deployed on Render. The React frontend collects 30 customer features and displays the churn probability, prediction label, and risk tier.

- **Frontend:** [churnpredictor-zeta.vercel.app](https://churnpredictor-zeta.vercel.app/)
- **Backend API:** [churnpredictor-6vzb.onrender.com](https://churnpredictor-6vzb.onrender.com/)
- **API Docs:** [churnpredictor-6vzb.onrender.com/docs](https://churnpredictor-6vzb.onrender.com/docs)

> ⚠️ Hosted on Render free tier — first request may take 30–60 seconds to cold start.

---

## How It Works

1. User fills in 29 customer feature fields across five sections — personal info, account, phone services, internet services, and billing. `Total_Revenue` is the 30th feature but is computed automatically from the four billing component fields — the user never enters it directly
2. React frontend sends a POST request to `/predict`
3. FastAPI validates input via Pydantic — enforcing feature consistency with the training data at the schema level:
   - **Numeric features** — every field has both a floor and ceiling matching the exact range seen during training (e.g. `Age: 19–80`, `Tenure_in_Months: 1–72`, `Total_Charges: 0–8684.80`). Out-of-range values return a `422` before reaching the model
   - **Categorical features** — every field is a strict `Literal` type accepting only the exact values the model was trained on (e.g. `Contract: "Month-to-Month" | "One Year" | "Two Year"`). Any unlisted value is rejected at the schema level
   - This same constraint is enforced in the frontend: numeric inputs have `min`/`max` attributes with placeholders showing the allowed range, and categorical inputs are dropdowns restricted to valid options only — so invalid data is blocked at the UI level before it ever reaches the API
4. Validated features are remapped from underscore-keyed schema fields to space-separated column names matching the model's training data
5. The LightGBM pipeline preprocesses and scores the input, returning a churn probability
6. Probability is compared against the tuned threshold (0.5784) to produce a prediction label and risk tier
7. Result is rendered as a risk badge, prediction label, and probability bar

---

## Project Structure

```text
churn-predictor/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app, CORS, lifespan
│   │   ├── core/
│   │   │   └── config.py        # Pydantic BaseSettings — all env vars
│   │   ├── routes/
│   │   │   └── predict.py       # POST /predict, GET /health
│   │   ├── services/
│   │   │   └── predictor.py     # inference logic, COLUMN_MAP, risk tiers
│   │   ├── schemas/
│   │   │   └── churn.py         # request/response Pydantic models
│   │   └── models/
│   │       └── loader.py        # joblib model loader (lru_cache)
│   ├── churn_model.pkl          # serialized LightGBM pipeline artifact
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CustomerForm/
│   │   │   ├── ResultCard/
│   │   │   └── SectionHeader/
│   │   ├── api/
│   │   │   └── predict.js
│   │   ├── App.jsx
│   │   └── App.css
│   └── package.json
└── README.md
```

---

## Model

The prediction model is a tuned LightGBM pipeline trained on the [Maven Analytics Telecom Churn dataset](https://www.kaggle.com/datasets/shilongzhuang/telecom-customer-churn-by-maven-analytics).

- Full sklearn `Pipeline` — preprocessor + model serialized as a single joblib artifact
- `OneHotEncoder(drop='first')` for 18 categorical features
- Numerical features passed through without scaling
- Tuned via `GridSearchCV` with `StratifiedKFold(n_splits=5)`, scoring on `average_precision`
- Decision threshold tuned to **0.5784** using the Precision-Recall curve

**Test performance:**
- ROC-AUC: 0.9201
- PR-AUC: 0.8463
- Churn Precision: 0.76 (at tuned threshold)
- Churn Recall: 0.73 (at tuned threshold)

For full model development details — EDA, preprocessing decisions, model comparison, SHAP analysis — see the [research notebook](https://github.com/jaypatel-dev-creator/telecom_customer_churn_prediction_dt).

---

## API

**POST** `/predict`

Request body:
```json
{
    "Gender": "Male",
    "Age": 35,
    "Married": "Yes",
    "Tenure_in_Months": 5,
    "Contract": "Month-to-Month",
    "Monthly_Charge": 95.0,
    "..."
}
```

Response:
```json
{
    "churn_probability": 0.8012,
    "prediction": "Churned",
    "risk_level": "High Risk"
}
```

**GET** `/health`
```json
{ "status": "ok" }
```

---

## Tech Stack

**Backend**
- FastAPI 0.135.3
- LightGBM 4.6.0
- scikit-learn 1.6.1
- pandas 3.0.2
- joblib 1.5.3
- Pydantic 2.13.0 + pydantic-settings 2.15.0
- Docker

**Frontend**
- React 19
- Vite
- CSS

**Deployment**
- Backend — Render (Docker)
- Frontend — Vercel

---

## Local Development

**Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # defaults work out of the box for local dev
uvicorn app.main:app --reload --port 8000
```

Swagger docs: `http://localhost:8000/docs`

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

```bash
cp .env.example .env           # defaults work out of the box for local dev
```

---

## Known Limitations

**Render cold starts**
The backend is deployed on Render's free tier. If the service has been inactive for 15+ minutes, the first request will take 30–60 seconds while the container spins back up. Subsequent requests are fast. This is a free-tier limitation and would not occur on a paid instance.

**Model retraining**
The current model is a static artifact trained on a fixed dataset snapshot. Customer behaviour changes over time — model performance may degrade without periodic retraining on fresh data. If the model is retrained with different feature ranges or categories, `schemas/churn.py` must be updated alongside the artifact.

---

## Related

- [Research Notebook & Model Development](https://github.com/jaypatel-dev-creator/telecom_customer_churn_prediction_dt) — full EDA, preprocessing, model training, SHAP analysis