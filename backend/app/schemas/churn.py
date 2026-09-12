from typing import Literal
from pydantic import BaseModel, Field


# request schema
class CustomerFeatures(BaseModel):

    # --- Personal ---
    Gender: Literal["Male", "Female"]
    Age: int = Field(..., ge=19, le=80)
    Married: Literal["Yes", "No"]
    Number_of_Dependents: int = Field(..., ge=0, le=9)

    # --- Account ---
    Number_of_Referrals: int = Field(..., ge=0, le=11)
    Tenure_in_Months: int = Field(..., ge=1, le=72)
    Offer: Literal["No Offer", "Offer A", "Offer B", "Offer C", "Offer D", "Offer E"]
    Contract: Literal["Month-to-Month", "One Year", "Two Year"]
    Paperless_Billing: Literal["Yes", "No"]
    Payment_Method: Literal["Credit Card", "Bank Withdrawal", "Mailed Check"]

    # --- Phone ---
    Phone_Service: Literal["Yes", "No"]
    Multiple_Lines: Literal["Yes", "No", "No Phone Service"]
    Avg_Monthly_Long_Distance_Charges: float = Field(..., ge=0.0, le=49.99)

    # --- Internet ---
    Internet_Service: Literal["Yes", "No"]
    Internet_Type: Literal["Fiber Optic", "Cable", "DSL", "No Internet Service"]
    Avg_Monthly_GB_Download: float = Field(..., ge=0.0, le=85.0)
    Online_Security: Literal["Yes", "No", "No Internet Service"]
    Online_Backup: Literal["Yes", "No", "No Internet Service"]
    Device_Protection_Plan: Literal["Yes", "No", "No Internet Service"]
    Premium_Tech_Support: Literal["Yes", "No", "No Internet Service"]
    Streaming_TV: Literal["Yes", "No", "No Internet Service"]
    Streaming_Movies: Literal["Yes", "No", "No Internet Service"]
    Streaming_Music: Literal["Yes", "No", "No Internet Service"]
    Unlimited_Data: Literal["Yes", "No", "No Internet Service"]

    # --- Billing ---
    Monthly_Charge: float = Field(..., ge=-10.0, le=118.75)
    Total_Charges: float = Field(..., ge=0.0, le=8684.80)
    Total_Refunds: float = Field(..., ge=0.0, le=49.79)
    Total_Extra_Data_Charges: int = Field(..., ge=0, le=150)
    Total_Long_Distance_Charges: float = Field(..., ge=0.0, le=3564.72)
    Total_Revenue: float = Field(..., ge=0.0)


# response schema
class PredictionResponse(BaseModel):
    churn_probability: float
    prediction: str
    risk_level: str