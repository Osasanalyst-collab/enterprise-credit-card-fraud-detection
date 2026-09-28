RAW_COLUMNS = [
    "step", "type", "amount", "nameOrig", "oldbalanceOrg", "newbalanceOrig",
    "nameDest", "oldbalanceDest", "newbalanceDest", "isFraud", "isFlaggedFraud"
]
TRANSACTION_TYPES = {"PAYMENT", "TRANSFER", "CASH_OUT", "DEBIT", "CASH_IN", "DEPOSIT"}
TARGET = "isFraud"
MODEL_FEATURES = [
    "type", "amount", "oldbalanceOrg", "newbalanceOrig", "oldbalanceDest",
    "newbalanceDest", "hour", "day", "balance_diff_orig", "balance_diff_dest",
    "orig_error", "dest_error", "amount_log", "empties_origin", "zero_dest_before",
    "is_transfer_or_cashout"
]
