import pandas as pd

def quality_metrics(df: pd.DataFrame) -> dict[str, float | int]:
    rows = len(df)
    return {
        "rows": rows,
        "duplicate_rate": float(df.duplicated().mean()) if rows else 0.0,
        "missing_cell_rate": float(df.isna().mean().mean()) if rows else 0.0,
        "fraud_rate": float(df["isFraud"].mean()) if rows and "isFraud" in df else 0.0,
        "average_amount": float(df["amount"].mean()) if rows else 0.0,
    }
