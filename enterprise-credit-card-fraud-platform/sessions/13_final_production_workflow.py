import json
from fraud_detection.pipeline import run_training_pipeline
result=run_training_pipeline("data/samples/sample_transactions.csv",model_name="logistic")
print(json.dumps(result,indent=2,default=str))
