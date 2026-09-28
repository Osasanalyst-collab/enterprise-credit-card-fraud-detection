import numpy as np
import pandas as pd

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    # PaySim step is one hour. Preserve it to create time features.
    out["hour"] = (out["step"].astype("int64") % 24).astype("int16")
    out["day"] = (out["step"].astype("int64") // 24).astype("int16")
    out["balance_diff_orig"] = out["oldbalanceOrg"] - out["newbalanceOrig"]
    # Corrected from the source notebook.
    out["balance_diff_dest"] = out["newbalanceDest"] - out["oldbalanceDest"]
    out["orig_error"] = out["balance_diff_orig"] - out["amount"]
    out["dest_error"] = out["balance_diff_dest"] - out["amount"]
    out["amount_log"] = np.log1p(out["amount"].clip(lower=0))
    out["empties_origin"] = ((out["oldbalanceOrg"] > 0) & (out["newbalanceOrig"] == 0)).astype("int8")
    out["zero_dest_before"] = (out["oldbalanceDest"] == 0).astype("int8")
    out["is_transfer_or_cashout"] = out["type"].isin(["TRANSFER", "CASH_OUT"]).astype("int8")
    return out
