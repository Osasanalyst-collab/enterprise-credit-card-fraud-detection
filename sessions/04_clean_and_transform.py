from fraud_detection.ingestion.batch_ingestion import read_csv
from fraud_detection.transformation.clean_transactions import clean_transactions
df=clean_transactions(read_csv("data/samples/sample_transactions.csv"))
df.to_csv("data/interim/clean_transactions.csv",index=False)
print(df.shape)
