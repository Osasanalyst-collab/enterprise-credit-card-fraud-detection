from datetime import datetime, timezone
from pathlib import Path
import json, joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_sample_weight
from fraud_detection.config.constants import MODEL_FEATURES, TARGET
from fraud_detection.training.evaluate import evaluate_probabilities
from fraud_detection.training.model_factory import build_model
from fraud_detection.training.threshold import optimise_threshold

def train_and_register(df: pd.DataFrame, model_dir: str | Path, model_name="logistic", version="1.0.0", random_state=42) -> dict:
    X = df[MODEL_FEATURES]
    y = df[TARGET].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=random_state)
    model = build_model(model_name)
    fit_kwargs = {}
    if model_name == "hist_gradient_boosting":
        fit_kwargs["classifier__sample_weight"] = compute_sample_weight("balanced", y_train)
    model.fit(X_train, y_train, **fit_kwargs)
    probabilities = model.predict_proba(X_test)[:, 1]
    threshold_result = optimise_threshold(y_test, probabilities, X_test["amount"].to_numpy())
    metrics = evaluate_probabilities(y_test, probabilities, threshold_result["threshold"])
    model_dir = Path(model_dir); model_dir.mkdir(parents=True, exist_ok=True)
    artifact = model_dir / f"fraud_model_{version}.joblib"
    metadata = model_dir / f"fraud_model_{version}.json"
    joblib.dump(model, artifact)
    payload = {
        "model_name": model_name, "version": version, "created_at": datetime.now(timezone.utc).isoformat(),
        "artifact": str(artifact), "threshold": threshold_result["threshold"],
        "business_threshold": threshold_result, "metrics": metrics, "features": MODEL_FEATURES,
        "training_rows": int(len(X_train)), "test_rows": int(len(X_test)),
    }
    metadata.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (model_dir / "latest.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload
