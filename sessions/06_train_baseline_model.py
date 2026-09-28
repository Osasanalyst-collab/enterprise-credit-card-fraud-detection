import json
import pandas as pd
from fraud_detection.training.train import train_and_register
df=pd.read_csv("data/processed/featured_transactions.csv")
print(json.dumps(train_and_register(df,"artifacts/models","logistic","1.0.0"),indent=2))
