# Customer Churn Predictor

A full-stack machine learning application that predicts customer churn for a telecom provider. Built with a LightGBM inference backend served via FastAPI, containerised with Docker, and deployed with a React frontend.

---

## Live Demo

- **Frontend:** [Vercel URL]
- **Backend API:** [Render URL]
- **API Docs:** [Render URL]/docs

---

## Project Structure

```text
churn-predictor/
├── backend/
│   ├── main.py
│   ├── model.py
│   ├── schemas.py
│   ├── churn_model.pkl
│   ├── requirements.txt
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

## How It Works

1. User fills in customer details across five sections — personal info, account, phone services, internet services, and billing
2. React frontend sends a POST request to the FastAPI `/predict` endpoint
3. FastAPI validates the input using Pydantic, passes it to the LightGBM pipeline
4. The pipeline preprocesses the input and returns a churn probability
5. Probability is compared against the tuned threshold (0.5784) to produce a prediction and risk label
6. Result is displayed as a risk badge, prediction label, and probability bar

---

## Model

The prediction model is a tuned LightGBM pipeline trained on the [Maven Analytics Telecom Churn dataset](https://www.kaggle.com/datasets/shilongzhuang/telecom-customer-churn-by-maven-analytics).

- Full sklearn `Pipeline` — preprocessor + model in a single object
- `OneHotEncoder(drop='first')` for 18 categorical features
- Numerical features passed through without scaling
- Tuned via `GridSearchCV` with `StratifiedKFold(n_splits=5)`, scoring on `average_precision`
- Decision threshold tuned to **0.5784** using the Precision-Recall curve

**Test performance:**
- ROC-AUC: 0.9201
- PR-AUC: 0.8463
- Churn Precision: 0.76 (at tuned threshold)
- Churn Recall: 0.73 (at tuned threshold)

**Note on input ranges:**
The model was trained on a specific data distribution. Numeric inputs are validated against their training-set ranges — for example, Age (19–80), Tenure in Months (1–72), Monthly Charge (-10 to 118.75), and usage-related fields. Inputs outside these ranges will still return a prediction but reliability decreases as values move further from the training distribution. Frontend validation enforces these constraints where applicable to reduce out-of-distribution inputs.


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
- FastAPI
- LightGBM
- scikit-learn
- pandas
- joblib
- Pydantic
- Docker

**Frontend**
- React 18
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
docker build -t churn-predictor .
docker run -p 8000:8000 churn-predictor
```


**Frontend**
```bash
cd frontend
npm install
npm run dev
```

Add `.env` file in frontend root:
VITE_API_URL=http://localhost:8000

---

## Related

- [Research Notebook & Model Development](https://github.com/jaypatel-dev-creator/telecom_customer_churn_prediction_dt) — full EDA, preprocessing, model training, SHAP analysis