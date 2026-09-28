from fraud_detection.ingestion.batch_ingestion import read_csv
from fraud_detection.features.build_features import build_features
df=build_features(read_csv("data/interim/clean_transactions.csv"))
df.to_csv("data/processed/featured_transactions.csv",index=False)
print(df[["balance_diff_orig","balance_diff_dest","amount_log"]].head())
