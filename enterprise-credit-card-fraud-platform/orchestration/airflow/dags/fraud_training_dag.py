from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
with DAG("fraud_training_pipeline", start_date=datetime(2026,1,1), schedule="0 2 * * *", catchup=False, tags=["fraud","ml"]) as dag:
    validate = BashOperator(task_id="validate", bash_command="python sessions/03_ingest_and_validate.py")
    transform = BashOperator(task_id="transform", bash_command="python sessions/04_clean_and_transform.py && python sessions/05_feature_engineering.py")
    train = BashOperator(task_id="train", bash_command="python sessions/06_train_baseline_model.py")
    monitor = BashOperator(task_id="monitor", bash_command="python sessions/10_data_quality_monitoring.py")
    validate >> transform >> train >> monitor
