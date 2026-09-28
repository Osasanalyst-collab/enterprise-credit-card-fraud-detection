import pandas as pd

def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = out.columns.str.strip()
    out["type"] = out["type"].astype(str).str.strip().str.upper()
    numeric = ["step", "amount", "oldbalanceOrg", "newbalanceOrig", "oldbalanceDest", "newbalanceDest"]
    for col in numeric:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    for col in ["isFraud", "isFlaggedFraud"]:
        if col in out:
            out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0).astype("int8")
    out = out.drop_duplicates()
    out = out.dropna(subset=["type", "amount", *numeric[2:]])
    out = out[out["amount"] >= 0]
    return out.reset_index(drop=True)
