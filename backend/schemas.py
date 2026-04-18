from pydantic import BaseModel

class CustomerFeatures(BaseModel):
    Gender: str
    Age: int
    Married: str
    Number_of_Dependents: int
    Number_of_Referrals: int
    Tenure_in_Months: int
    Offer: str
    Phone_Service: str
    Avg_Monthly_Long_Distance_Charges: float
    Multiple_Lines: str
    Internet_Service: str
    Internet_Type: str
    Avg_Monthly_GB_Download: float
    Online_Security: str
    Online_Backup: str
    Device_Protection_Plan: str
    Premium_Tech_Support: str
    Streaming_TV: str
    Streaming_Movies: str
    Streaming_Music: str
    Unlimited_Data: str
    Contract: str
    Paperless_Billing: str
    Payment_Method: str
    Monthly_Charge: float
    Total_Charges: float
    Total_Refunds: float
    Total_Extra_Data_Charges: int
    Total_Long_Distance_Charges: float
    Total_Revenue: float

class PredictionResponse(BaseModel):
    churn_probability: float
    prediction: str
    risk_level: str