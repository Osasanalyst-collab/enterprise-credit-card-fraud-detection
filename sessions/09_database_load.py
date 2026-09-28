import pandas as pd
from fraud_detection.config.settings import get_settings
from fraud_detection.database.connection import write_frame
df=pd.read_csv("artifacts/batch_predictions.csv")
print("Rows loaded:",write_frame(df,"fraud_predictions",get_settings().database_url,if_exists="replace"))
