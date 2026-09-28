from fraud_detection.config.settings import get_settings
from fraud_detection.inference.predictor import FraudPredictor
from fraud_detection.ingestion.batch_ingestion import read_csv
raw=read_csv("data/samples/sample_transactions.csv",nrows=1000)
out=FraudPredictor(get_settings().model_dir).predict_frame(raw)
out.to_csv("artifacts/batch_predictions.csv",index=False)
print(out[["fraud_probability","risk_level","decision"]].head())
