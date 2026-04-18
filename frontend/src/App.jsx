// src/App.jsx

import { useState } from "react"
import CustomerForm from "./components/CustomerForm/CustomerForm"
import ResultCard from "./components/ResultCard/ResultCard"
import "./App.css"

const App = () => {
    const [result, setResult] = useState(null)

    const handleResult = (predictionResult) => {
        setResult(predictionResult)
    }

    const handleReset = () => {
        setResult(null)
    }

    return (
        <div className="app">
            <header className="app-header">
                <h1 className="app-title">Customer Churn Predictor</h1>
                <p className="app-subtitle">
                    Enter customer details to predict churn probability
                </p>
            </header>

            <main className="app-main">
                {result ? (
                    <ResultCard result={result} onReset={handleReset} />
                ) : (
                    <CustomerForm onResult={handleResult} />
                )}
            </main>

            <footer className="app-footer">
                <p>Powered by LightGBM — Maven Analytics Telecom Dataset</p>
            </footer>
        </div>
    )
}

export default App