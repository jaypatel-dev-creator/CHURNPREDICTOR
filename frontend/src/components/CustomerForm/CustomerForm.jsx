// src/components/CustomerForm/CustomerForm.jsx

import { useState } from "react"
import SectionHeader from "../SectionHeader/SectionHeader"
import { predictChurn } from "../../api/predict"
import "./CustomerForm.css"

const INITIAL_STATE = {
    Gender: "Male",
    Age: "",
    Married: "Yes",
    Number_of_Dependents: 0,
    Number_of_Referrals: 0,
    Tenure_in_Months: "",
    Offer: "No Offer",
    Phone_Service: "Yes",
    Avg_Monthly_Long_Distance_Charges: 0,      // changed from "" to 0
    Multiple_Lines: "No",
    Internet_Service: "Yes",
    Internet_Type: "Fiber Optic",
    Avg_Monthly_GB_Download: 0,                // changed from "" to 0
    Online_Security: "No",
    Online_Backup: "No",
    Device_Protection_Plan: "No",
    Premium_Tech_Support: "No",
    Streaming_TV: "No",
    Streaming_Movies: "No",
    Streaming_Music: "No",
    Unlimited_Data: "No",
    Contract: "Month-to-Month",
    Paperless_Billing: "Yes",
    Payment_Method: "Credit Card",
    Monthly_Charge: "",
    Total_Charges: "",
    Total_Refunds: 0.0,
    Total_Extra_Data_Charges: 0,
    Total_Long_Distance_Charges: "",
    Total_Revenue: ""
}

const CustomerForm = ({ onResult }) => {
    const [formData, setFormData] = useState(INITIAL_STATE)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const handleChange = (e) => {
        const { name, value } = e.target
        setFormData(prev => ({
            ...prev,
            [name]: value
        }))
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)
        setError(null)

        try {
            const payload = {
                ...formData,
                Age: Number(formData.Age),
                Number_of_Dependents: Number(formData.Number_of_Dependents),
                Number_of_Referrals: Number(formData.Number_of_Referrals),
                Tenure_in_Months: Number(formData.Tenure_in_Months),
                Avg_Monthly_Long_Distance_Charges: Number(formData.Avg_Monthly_Long_Distance_Charges),
                Avg_Monthly_GB_Download: Number(formData.Avg_Monthly_GB_Download),
                Monthly_Charge: Number(formData.Monthly_Charge),
                Total_Charges: Number(formData.Total_Charges),
                Total_Refunds: Number(formData.Total_Refunds),
                Total_Extra_Data_Charges: Number(formData.Total_Extra_Data_Charges),
                Total_Long_Distance_Charges: Number(formData.Total_Long_Distance_Charges),
                Total_Revenue: Number(formData.Total_Revenue)
            }

            const result = await predictChurn(payload)
            onResult(result)

        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <form className="customer-form" onSubmit={handleSubmit}>

            {/* Section 1 - Personal Info */}
            <SectionHeader title="Personal Information" />
            <div className="form-grid">
                <div className="form-group">
                    <label>Gender</label>
                    <select name="Gender" value={formData.Gender} onChange={handleChange}>
                        <option>Male</option>
                        <option>Female</option>
                    </select>
                </div>

                <div className="form-group">
                    <label>Age</label>
                    <input
                        type="number" name="Age"
                        value={formData.Age} onChange={handleChange}
                        min={19} max={80} required
                        placeholder="19 - 80"
                    />
                </div>

                <div className="form-group">
                    <label>Married</label>
                    <select name="Married" value={formData.Married} onChange={handleChange}>
                        <option>Yes</option>
                        <option>No</option>
                    </select>
                </div>

                <div className="form-group">
                    <label>Number of Dependents</label>
                    <input
                        type="number" name="Number_of_Dependents"
                        value={formData.Number_of_Dependents} onChange={handleChange}
                        min={0} max={9} 
                        placeholder="0 - 9"
                    />
                </div>
            </div>

            {/* Section 2 - Account Info */}
            <SectionHeader title="Account Information" />
            <div className="form-grid">
                <div className="form-group">
                    <label>Tenure in Months</label>
                    <input
                        type="number" name="Tenure_in_Months"
                        value={formData.Tenure_in_Months} onChange={handleChange}
                        min={1} max={72} required
                        placeholder="1 - 72"
                    />
                </div>

                <div className="form-group">
                    <label>Number of Referrals</label>
                    <input
                        type="number" name="Number_of_Referrals"
                        value={formData.Number_of_Referrals} onChange={handleChange}
                        min={0} max={11}
                    />
                </div>

                <div className="form-group">
                    <label>Offer</label>
                    <select name="Offer" value={formData.Offer} onChange={handleChange}>
                        <option>No Offer</option>
                        <option>Offer A</option>
                        <option>Offer B</option>
                        <option>Offer C</option>
                        <option>Offer D</option>
                        <option>Offer E</option>
                    </select>
                </div>

                <div className="form-group">
                    <label>Contract</label>
                    <select name="Contract" value={formData.Contract} onChange={handleChange}>
                        <option>Month-to-Month</option>
                        <option>One Year</option>
                        <option>Two Year</option>
                    </select>
                </div>

                <div className="form-group">
                    <label>Paperless Billing</label>
                    <select name="Paperless_Billing" value={formData.Paperless_Billing} onChange={handleChange}>
                        <option>Yes</option>
                        <option>No</option>
                    </select>
                </div>

                <div className="form-group">
                    <label>Payment Method</label>
                    <select name="Payment_Method" value={formData.Payment_Method} onChange={handleChange}>
                        <option>Credit Card</option>
                        <option>Bank Withdrawal</option>
                        <option>Mailed Check</option>
                    </select>
                </div>
            </div>

            {/* Section 3 - Phone Services */}
            <SectionHeader title="Phone Services" />
            <div className="form-grid">
                <div className="form-group">
                    <label>Phone Service</label>
                    <select name="Phone_Service" value={formData.Phone_Service} onChange={handleChange}>
                        <option>Yes</option>
                        <option>No</option>
                    </select>
                </div>

                <div className="form-group">
                    <label>Multiple Lines</label>
                    <select name="Multiple_Lines" value={formData.Multiple_Lines} onChange={handleChange}>
                        <option>Yes</option>
                        <option>No</option>
                        <option>No Phone Service</option>
                    </select>
                </div>

                {/* fixed — now properly wrapped in form-group with label */}
                <div className="form-group">
                    <label>Avg Monthly Long Distance Charges ($)</label>
                    <input
                        type="number" name="Avg_Monthly_Long_Distance_Charges"
                        value={formData.Avg_Monthly_Long_Distance_Charges}
                        onChange={handleChange}
                        min={0} max={49.99} step={0.01}
                    />
                </div>
            </div>

            {/* Section 4 - Internet Services */}
            <SectionHeader title="Internet Services" />
            <div className="form-grid">
                <div className="form-group">
                    <label>Internet Service</label>
                    <select name="Internet_Service" value={formData.Internet_Service} onChange={handleChange}>
                        <option>Yes</option>
                        <option>No</option>
                    </select>
                </div>

                <div className="form-group">
                    <label>Internet Type</label>
                    <select name="Internet_Type" value={formData.Internet_Type} onChange={handleChange}>
                        <option>Fiber Optic</option>
                        <option>Cable</option>
                        <option>DSL</option>
                        <option>No Internet Service</option>
                    </select>
                </div>

                <div className="form-group">
                    <label>Avg Monthly GB Download</label>
                    <input
                        type="number" name="Avg_Monthly_GB_Download"
                        value={formData.Avg_Monthly_GB_Download}
                        onChange={handleChange}
                        min={0} max={85} step={0.1}
                    />
                </div>

                <div className="form-group">
                    <label>Online Security</label>
                    <select name="Online_Security" value={formData.Online_Security} onChange={handleChange}>
                        <option>Yes</option>
                        <option>No</option>
                        <option>No Internet Service</option>
                    </select>
                </div>

                <div className="form-group">
                    <label>Online Backup</label>
                    <select name="Online_Backup" value={formData.Online_Backup} onChange={handleChange}>
                        <option>Yes</option>
                        <option>No</option>
                        <option>No Internet Service</option>
                    </select>
                </div>

                <div className="form-group">
                    <label>Device Protection Plan</label>
                    <select name="Device_Protection_Plan" value={formData.Device_Protection_Plan} onChange={handleChange}>
                        <option>Yes</option>
                        <option>No</option>
                        <option>No Internet Service</option>
                    </select>
                </div>

                <div className="form-group">
                    <label>Premium Tech Support</label>
                    <select name="Premium_Tech_Support" value={formData.Premium_Tech_Support} onChange={handleChange}>
                        <option>Yes</option>
                        <option>No</option>
                        <option>No Internet Service</option>
                    </select>
                </div>

                <div className="form-group">
                    <label>Streaming TV</label>
                    <select name="Streaming_TV" value={formData.Streaming_TV} onChange={handleChange}>
                        <option>Yes</option>
                        <option>No</option>
                        <option>No Internet Service</option>
                    </select>
                </div>

                <div className="form-group">
                    <label>Streaming Movies</label>
                    <select name="Streaming_Movies" value={formData.Streaming_Movies} onChange={handleChange}>
                        <option>Yes</option>
                        <option>No</option>
                        <option>No Internet Service</option>
                    </select>
                </div>

                <div className="form-group">
                    <label>Streaming Music</label>
                    <select name="Streaming_Music" value={formData.Streaming_Music} onChange={handleChange}>
                        <option>Yes</option>
                        <option>No</option>
                        <option>No Internet Service</option>
                    </select>
                </div>

                <div className="form-group">
                    <label>Unlimited Data</label>
                    <select name="Unlimited_Data" value={formData.Unlimited_Data} onChange={handleChange}>
                        <option>Yes</option>
                        <option>No</option>
                        <option>No Internet Service</option>
                    </select>
                </div>
            </div>

            {/* Section 5 - Billing */}
            <SectionHeader title="Billing Information" />
            <div className="form-grid">
                <div className="form-group">
                    <label>Monthly Charge ($)</label>
                    <input
                        type="number" name="Monthly_Charge"
                        value={formData.Monthly_Charge} onChange={handleChange}
                        min={-10} step={0.01} required        // added min={-10}
                        placeholder="e.g. 65.50"
                    />
                </div>

                <div className="form-group">
                    <label>Total Charges ($)</label>
                    <input
                        type="number" name="Total_Charges"
                        value={formData.Total_Charges} onChange={handleChange}
                        min={0} step={0.01} required
                        placeholder="e.g. 1200.00"
                    />
                </div>

                <div className="form-group">
                    <label>Total Refunds ($)</label>
                    <input
                        type="number" name="Total_Refunds"
                        value={formData.Total_Refunds} onChange={handleChange}
                        min={0} max={49.79} step={0.01}
                    />
                </div>

                <div className="form-group">
                    <label>Total Extra Data Charges ($)</label>
                    <input
                        type="number" name="Total_Extra_Data_Charges"
                        value={formData.Total_Extra_Data_Charges} onChange={handleChange}
                        min={0} max={150}
                    />
                </div>

                <div className="form-group">
                    <label>Total Long Distance Charges ($)</label>
                    <input
                        type="number" name="Total_Long_Distance_Charges"
                        value={formData.Total_Long_Distance_Charges} onChange={handleChange}
                        min={0} step={0.01} required
                        placeholder="e.g. 500.00"
                    />
                </div>

                <div className="form-group">
                    <label>Total Revenue ($)</label>
                    <input
                        type="number" name="Total_Revenue"
                        value={formData.Total_Revenue} onChange={handleChange}
                        min={0} step={0.01} required
                        placeholder="e.g. 1700.00"
                    />
                </div>
            </div>

            {error && <p className="error-message">{error}</p>}

            <button type="submit" className="submit-button" disabled={loading}>
                {loading ? "Predicting..." : "Predict Churn"}
            </button>

        </form>
    )
}

export default CustomerForm