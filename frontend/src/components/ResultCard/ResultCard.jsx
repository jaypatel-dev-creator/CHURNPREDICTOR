import "./ResultCard.css"

const ResultCard = ({ result, onReset }) => {
    const getRiskColor = (riskLevel) => {
        if (riskLevel === "High Risk") return "#e74c3c"
        if (riskLevel === "Medium Risk") return "#f39c12"
        return "#27ae60"
    }

    const getProbabilityBar = (probability) => {
        return Math.round(probability * 100)
    }

    return (
        <div className="result-card">
            <h2 className="result-title">Prediction Result</h2>

            <div
                className="risk-badge"
                style={{ backgroundColor: getRiskColor(result.risk_level) }}
            >
                {result.risk_level}
            </div>

            <div className="prediction-label">
                {result.prediction === "Churned" ? "⚠️ Likely to Churn" : "✅ Likely to Stay"}
            </div>

            <div className="probability-section">
                <p className="probability-label">Churn Probability</p>
                <div className="probability-bar-container">
                    <div
                        className="probability-bar"
                        style={{
                            width: `${getProbabilityBar(result.churn_probability)}%`,
                            backgroundColor: getRiskColor(result.risk_level)
                        }}
                    />
                </div>
                <p className="probability-value">
                    {getProbabilityBar(result.churn_probability)}%
                </p>
            </div>

            <button className="reset-button" onClick={onReset}>
                Predict Another Customer
            </button>
        </div>
    )
}

export default ResultCard