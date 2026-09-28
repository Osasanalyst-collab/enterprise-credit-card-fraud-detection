import pandas as pd
from fraud_detection.config.constants import RAW_COLUMNS, TRANSACTION_TYPES
from fraud_detection.utils.exceptions import DataContractError

def validate_schema(df: pd.DataFrame, require_target: bool = True) -> dict[str, object]:
    required = set(RAW_COLUMNS if require_target else [c for c in RAW_COLUMNS if c not in {"isFraud", "isFlaggedFraud"}])
    missing = sorted(required - set(df.columns))
    if missing:
        raise DataContractError(f"Missing required columns: {missing}")
    invalid_types = sorted(set(df["type"].dropna().astype(str).unique()) - TRANSACTION_TYPES)
    negative_amounts = int((pd.to_numeric(df["amount"], errors="coerce") < 0).sum())
    return {
        "rows": len(df), "columns": len(df.columns), "missing_columns": missing,
        "invalid_transaction_types": invalid_types, "negative_amounts": negative_amounts,
        "duplicate_rows": int(df.duplicated().sum()),
        "null_cells": int(df.isna().sum().sum()),
    }
