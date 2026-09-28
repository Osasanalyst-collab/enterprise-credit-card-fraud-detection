from pathlib import Path
import json, joblib
import pandas as pd
from fraud_detection.features.build_features import build_features
from fraud_detection.utils.exceptions import ModelArtifactError

class FraudPredictor:
    def __init__(self, model_dir: str | Path):
        model_dir = Path(model_dir)
        latest = model_dir / "latest.json"
        if not latest.exists():
            raise ModelArtifactError("No registered model. Run training first.")
        self.metadata = json.loads(latest.read_text(encoding="utf-8"))
        self.model = joblib.load(self.metadata["artifact"])
        self.threshold = float(self.metadata["threshold"])

    def predict_frame(self, raw: pd.DataFrame) -> pd.DataFrame:
        featured = build_features(raw)
        probability = self.model.predict_proba(featured)[:, 1]
        result = raw.copy()
        result["fraud_probability"] = probability
        result["prediction"] = (probability >= self.threshold).astype(int)
        result["risk_level"] = pd.cut(probability, [-0.01, 0.30, 0.75, 0.90, 1.0], labels=["LOW", "MEDIUM", "HIGH", "CRITICAL"])
        result["decision"] = result["risk_level"].map({"LOW":"APPROVE", "MEDIUM":"STEP_UP", "HIGH":"REVIEW", "CRITICAL":"BLOCK"})
        result["model_version"] = self.metadata["version"]
        return result
