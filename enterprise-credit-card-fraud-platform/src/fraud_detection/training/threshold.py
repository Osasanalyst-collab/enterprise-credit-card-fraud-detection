import numpy as np

def optimise_threshold(y_true, probabilities, amounts, false_positive_cost=15.0, review_cost=5.0, false_negative_multiplier=1.0):
    y = np.asarray(y_true)
    p = np.asarray(probabilities)
    a = np.asarray(amounts)
    best = None
    for threshold in np.linspace(0.05, 0.95, 91):
        pred = (p >= threshold).astype(int)
        fp = (pred == 1) & (y == 0)
        fn = (pred == 0) & (y == 1)
        cost = float(fp.sum() * (false_positive_cost + review_cost) + (a[fn] * false_negative_multiplier).sum())
        row = {"threshold": float(round(threshold, 2)), "business_cost": cost, "false_positives": int(fp.sum()), "false_negatives": int(fn.sum())}
        if best is None or row["business_cost"] < best["business_cost"]:
            best = row
    return best
