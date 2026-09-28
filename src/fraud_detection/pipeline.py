from pathlib import Path
import json
from fraud_detection.config.settings import get_settings
from fraud_detection.features.build_features import build_features
from fraud_detection.ingestion.batch_ingestion import read_csv
from fraud_detection.ingestion.schema_validation import validate_schema
from fraud_detection.monitoring.data_quality import quality_metrics
from fraud_detection.training.train import train_and_register
from fraud_detection.transformation.clean_transactions import clean_transactions

def run_training_pipeline(input_path: str | Path, model_name="logistic", sample_rows: int | None = None):
    settings = get_settings()
    raw = read_csv(input_path, nrows=sample_rows)
    contract = validate_schema(raw)
    clean = clean_transactions(raw)
    featured = build_features(clean)
    metrics = quality_metrics(featured)
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/data_quality.json").write_text(json.dumps({"contract": contract, "quality": metrics}, indent=2), encoding="utf-8")
    featured.to_parquet("data/processed/featured_transactions.parquet", index=False) if _parquet_available() else featured.to_csv("data/processed/featured_transactions.csv", index=False)
    model = train_and_register(featured, settings.model_dir, model_name=model_name, version=settings.model_version)
    return {"contract": contract, "quality": metrics, "model": model}

def _parquet_available():
    try:
        import pyarrow  # noqa: F401
        return True
    except ImportError:
        return False
