# Customer Churn Predictor — Frontend

![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-8.0-646CFF?logo=vite&logoColor=white)
![Axios](https://img.shields.io/badge/Axios-1.16-5A29E4?logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-Deployed-000000?logo=vercel&logoColor=white)

React + Vite SPA. Collects 30 customer features across five sections, sends them to the FastAPI backend, and renders the churn probability, prediction label, and risk tier.

**Live:** [churnpredictor-zeta.vercel.app](https://churnpredictor-zeta.vercel.app/)

---

## Project Structure

```text
frontend/
├── src/
│   ├── App.jsx                        # root component — state orchestration
│   ├── App.css                        # global layout styles
│   ├── main.jsx                       # React DOM entry point
│   ├── api/
│   │   └── predict.js                 # axios wrapper for POST /predict
│   └── components/
│       ├── CustomerForm/
│       │   ├── CustomerForm.jsx       # form state, type coercion, submit logic
│       │   └── CustomerForm.css
│       ├── ResultCard/
│       │   ├── ResultCard.jsx         # renders prediction result
│       │   └── ResultCard.css
│       └── SectionHeader/
│           └── SectionHeader.jsx      # reusable section title component
├── index.html
├── vite.config.js
└── package.json
```

---

## Data Flow

```
User fills form (CustomerForm)
        │
        ▼
handleSubmit fires
  - e.preventDefault()
  - coerces all numeric string inputs to Number()
  - builds typed payload
        │
        ▼
predictChurn(payload)  [api/predict.js]
  - axios.POST to VITE_API_URL/predict
  - throws with error.response.data.detail on non-2xx
        │
        ▼
FastAPI /predict
  - Pydantic validates types, ranges, and allowed categorical values
  - 422 returned immediately on invalid input
  - valid input passed to predictor service
        │
        ▼
Response: { churn_probability, prediction, risk_level }
        │
        ▼
App.jsx state: setResult(response)
        │
        ▼
CustomerForm unmounts → ResultCard mounts
  - renders risk badge (colour-coded by risk tier)
  - renders prediction label (Churned / Stayed)
  - renders probability bar
  - "Predict Another Customer" → onReset() → result = null → form reappears
```

---

## Components

**`App.jsx`**
Root component. Owns `result` state — `null` shows the form, a populated object shows the result card. Passes `onResult` down to `CustomerForm` and `onReset` down to `ResultCard`. No routing library — single view toggled by state.

**`CustomerForm.jsx`**
The main form. Manages `formData` (30 fields), `loading`, and `error` state. On submit, coerces all numeric string inputs to `Number()` before sending — HTML inputs always return strings, the backend expects typed numbers. Required fields: `Age`, `Tenure_in_Months`, `Monthly_Charge`, `Total_Charges`, `Total_Long_Distance_Charges`, `Total_Revenue`. Displays inline error message on API failure.

**`api/predict.js`**
Thin axios wrapper. Reads `VITE_API_URL` from environment. Returns the response data on success. On failure, extracts `error.response.data.detail` from the FastAPI error response and throws it as a plain `Error` — the form catches and displays this string directly.

**`ResultCard.jsx`**
Stateless display component. Receives `{ churn_probability, prediction, risk_level }` and `onReset`. Risk badge colour is computed inline: red for High Risk, orange for Medium Risk, green for Low Risk. Probability bar width is `churn_probability * 100`%.

**`SectionHeader.jsx`**
Single-prop reusable component. Renders a styled `<h2>` to divide the form into sections.

---

## Form Sections & Fields

| Section | Fields |
|---|---|
| Personal Information | Gender, Age, Married, Number of Dependents |
| Account Information | Tenure in Months, Number of Referrals, Offer, Contract, Paperless Billing, Payment Method |
| Phone Services | Phone Service, Multiple Lines, Avg Monthly Long Distance Charges |
| Internet Services | Internet Service, Internet Type, Avg Monthly GB Download, Online Security, Online Backup, Device Protection Plan, Premium Tech Support, Streaming TV, Streaming Movies, Streaming Music, Unlimited Data |
| Billing Information | Monthly Charge, Total Charges, Total Refunds, Total Extra Data Charges, Total Long Distance Charges, Total Revenue |

---

## Tech Stack

| Package | Version | Purpose |
|---|---|---|
| React | 19.2.4 | UI framework |
| Vite | 8.0.4 | Build tool + dev server |
| axios | 1.16.0 | HTTP client |

---

## Local Setup

```bash
cd frontend
npm install
```

Create `.env` in `frontend/`:
```
VITE_API_URL=http://localhost:8000
```

```bash
npm run dev
```

App runs at `http://localhost:5173`. Backend must be running at `http://localhost:8000`.

---

## Environment Variables

| Variable | Description |
|---|---|
| `VITE_API_URL` | Base URL of the FastAPI backend. No trailing slash. |

In production this is set to the Render backend URL in the Vercel project settings — not committed to source.