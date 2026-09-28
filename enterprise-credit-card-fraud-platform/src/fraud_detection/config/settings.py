from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    log_level: str = "INFO"
    data_path: Path = Path("data/samples/sample_transactions.csv")
    database_url: str = "sqlite:///artifacts/fraud_platform.db"
    model_dir: Path = Path("artifacts/models")
    model_name: str = "credit-card-fraud-model"
    model_version: str = "1.0.0"
    model_threshold: float = 0.50
    api_key: str = "change-me"
    review_cost: float = 5.0
    false_positive_cost: float = 15.0
    false_negative_multiplier: float = 1.0
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.model_dir.mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    Path("artifacts").mkdir(exist_ok=True)
    return settings
