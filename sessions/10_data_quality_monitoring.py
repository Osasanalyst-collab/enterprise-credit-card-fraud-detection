import json, pandas as pd
from fraud_detection.monitoring.data_quality import quality_metrics
df=pd.read_csv("data/processed/featured_transactions.csv")
metrics=quality_metrics(df)
open("artifacts/monitoring_snapshot.json","w").write(json.dumps(metrics,indent=2))
print(metrics)
