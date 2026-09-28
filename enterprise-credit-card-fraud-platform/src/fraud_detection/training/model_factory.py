from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from fraud_detection.config.constants import MODEL_FEATURES

CATEGORICAL = ["type"]
NUMERIC = [c for c in MODEL_FEATURES if c not in CATEGORICAL]

def build_preprocessor() -> ColumnTransformer:
    numeric = Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())])
    categorical = Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))])
    return ColumnTransformer([("num", numeric, NUMERIC), ("cat", categorical, CATEGORICAL)])

def build_model(name: str = "logistic") -> Pipeline:
    if name == "logistic":
        estimator = LogisticRegression(class_weight="balanced", max_iter=1200, solver="lbfgs")
    elif name == "hist_gradient_boosting":
        estimator = HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=31, random_state=42)
    else:
        raise ValueError(f"Unknown model: {name}")
    return Pipeline([("preprocessor", build_preprocessor()), ("classifier", estimator)])
