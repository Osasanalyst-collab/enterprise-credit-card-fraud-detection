import json
from fraud_detection.ingestion.batch_ingestion import read_csv
from fraud_detection.ingestion.schema_validation import validate_schema
df=read_csv("data/samples/sample_transactions.csv")
print(json.dumps(validate_schema(df),indent=2))
