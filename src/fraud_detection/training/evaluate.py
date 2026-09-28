from dataclasses import asdict, dataclass
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_fscore_support, roc_auc_score, confusion_matrix

@dataclass
class Metrics:
    threshold: float
    precision: float
    recall: float
    f1: float
    pr_auc: float
    roc_auc: float
    tn: int
    fp: int
    fn: int
    tp: int

def evaluate_probabilities(y_true, probabilities, threshold: float) -> dict:
    pred = (np.asarray(probabilities) >= threshold).astype(int)
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, pred, average="binary", zero_division=0)
    tn, fp, fn, tp = confusion_matrix(y_true, pred, labels=[0, 1]).ravel()
    result = Metrics(threshold, float(precision), float(recall), float(f1), float(average_precision_score(y_true, probabilities)), float(roc_auc_score(y_true, probabilities)), int(tn), int(fp), int(fn), int(tp))
    return asdict(result)
