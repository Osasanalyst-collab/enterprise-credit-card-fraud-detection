from pydantic import BaseModel, Field

class Transaction(BaseModel):
    step: int = Field(ge=0)
    type: str
    amount: float = Field(ge=0)
    nameOrig: str = "REDACTED_ORIGIN"
    oldbalanceOrg: float = Field(ge=0)
    newbalanceOrig: float = Field(ge=0)
    nameDest: str = "REDACTED_DESTINATION"
    oldbalanceDest: float = Field(ge=0)
    newbalanceDest: float = Field(ge=0)
    isFraud: int = 0
    isFlaggedFraud: int = 0

class PredictionResponse(BaseModel):
    fraud_probability: float
    prediction: int
    risk_level: str
    decision: str
    model_version: str
