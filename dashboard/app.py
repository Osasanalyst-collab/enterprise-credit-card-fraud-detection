from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# 1. PROJECT PATH CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from fraud_detection.inference.predictor import FraudPredictor


# ============================================================
# 2. STREAMLIT PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Fraud Operations Center",
    page_icon="🛡️",
    layout="wide",
)


# ============================================================
# 3. PROJECT ARTIFACT PATHS
# ============================================================

MODEL_DIR = ROOT / "artifacts" / "models"
SAMPLE_PATH = ROOT / "data" / "samples" / "sample_transactions.csv"
DQ_PATH = ROOT / "artifacts" / "data_quality.json"


# ============================================================
# 4. RESOURCE LOADING
# ============================================================

@st.cache_resource
def load_predictor() -> FraudPredictor:
    """
    Load the registered production fraud model.

    The resource is cached so Streamlit does not reload the model
    every time the user interacts with the application.
    """
    return FraudPredictor(MODEL_DIR)


@st.cache_data
def load_sample() -> pd.DataFrame:
    """
    Load the demonstration transaction dataset.
    """
    if SAMPLE_PATH.exists():
        return pd.read_csv(SAMPLE_PATH)

    return pd.DataFrame()


@st.cache_data
def load_quality() -> dict:
    """
    Load the latest data-quality monitoring artifact.
    """
    if DQ_PATH.exists():
        return json.loads(DQ_PATH.read_text(encoding="utf-8"))

    return {}


# ============================================================
# 5. UTILITY FUNCTIONS
# ============================================================

def money(value: float) -> str:
    """Format monetary values."""
    return f"£{float(value):,.2f}"


def score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Score transactions using the registered fraud model.

    Target labels such as isFraud are not used as prediction
    features. Feature selection is handled by the production
    inference pipeline.
    """
    return load_predictor().predict_frame(df)


def risk_filter(frame: pd.DataFrame) -> pd.DataFrame:
    """
    Allow fraud investigators to filter transactions
    by model-generated risk level.
    """

    available_levels = [
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL",
    ]

    levels = st.multiselect(
        "Risk level",
        available_levels,
        default=["HIGH", "CRITICAL"],
    )

    if not levels:
        return frame

    return frame[
        frame["risk_level"].astype(str).isin(levels)
    ]


# ============================================================
# 6. LOAD PRODUCTION MODEL
# ============================================================

try:
    predictor = load_predictor()
    meta = predictor.metadata

except Exception as exc:
    st.error(
        "The registered fraud-detection model could not be loaded."
    )

    st.exception(exc)

    st.info(
        "Check that the trained model and metadata exist inside "
        "'artifacts/models/'."
    )

    st.stop()


# ============================================================
# 7. SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("🛡️ FraudOps")

st.sidebar.caption(
    "Enterprise Fraud Detection Platform"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Dashboard",
        "Single Transaction",
        "Batch Prediction",
        "Fraud Analytics",
        "Model Monitoring",
    ],
)

st.sidebar.divider()

st.sidebar.caption(
    f"Model: {meta.get('version', 'unknown')}"
)

st.sidebar.caption(
    f"Threshold: "
    f"{float(meta.get('threshold', 0)):.2f}"
)


# ============================================================
# 8. EXECUTIVE DASHBOARD
# ============================================================

if page == "Executive Dashboard":

    st.title("🛡️ Enterprise Fraud Operations Center")

    st.caption(
        "Interactive transaction-risk monitoring using the "
        "registered production fraud-detection model."
    )

    raw = load_sample()

    if raw.empty:

        st.warning(
            "No sample dataset was found. "
            "Upload transactions through Batch Prediction."
        )

    else:

        with st.spinner(
            "Scoring sample transactions..."
        ):
            scored = score(raw)

        fraud = scored["prediction"] == 1

        total_transactions = len(scored)
        flagged_transactions = int(fraud.sum())

        flag_rate = (
            fraud.mean()
            if total_transactions > 0
            else 0
        )

        flagged_value = scored.loc[
            fraud,
            "amount",
        ].sum()

        # ----------------------------------------------------
        # KPI CARDS
        # ----------------------------------------------------

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Transactions",
            f"{total_transactions:,}",
        )

        c2.metric(
            "Flagged Transactions",
            f"{flagged_transactions:,}",
        )

        c3.metric(
            "Flag Rate",
            f"{flag_rate:.2%}",
        )

        c4.metric(
            "Flagged Value",
            money(flagged_value),
        )

        st.divider()

        # ----------------------------------------------------
        # RISK DISTRIBUTION
        # ----------------------------------------------------

        st.subheader("Risk Distribution")

        risk_distribution = (
            scored["risk_level"]
            .astype(str)
            .value_counts()
        )

        st.bar_chart(
            risk_distribution
        )

        # ----------------------------------------------------
        # TRANSACTION VALUE
        # ----------------------------------------------------

        st.subheader(
            "Transaction Value by Type"
        )

        value_by_type = (
            scored
            .groupby("type")["amount"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(
            value_by_type
        )

        # ----------------------------------------------------
        # HIGH-RISK TRANSACTIONS
        # ----------------------------------------------------

        st.subheader(
            "Highest-Risk Transactions"
        )

        display_columns = [
            "step",
            "type",
            "amount",
            "nameOrig",
            "nameDest",
            "fraud_probability",
            "risk_level",
            "decision",
        ]

        display_columns = [
            column
            for column in display_columns
            if column in scored.columns
        ]

        high_risk = (
            scored
            .sort_values(
                "fraud_probability",
                ascending=False,
            )
            [display_columns]
            .head(25)
        )

        st.dataframe(
            high_risk,
            width="stretch",
            hide_index=True,
        )


# ============================================================
# 9. SINGLE TRANSACTION PREDICTION
# ============================================================

elif page == "Single Transaction":

    st.title(
        "🔍 Single Transaction Risk Assessment"
    )

    st.caption(
        "Enter transaction attributes to generate "
        "a real-time fraud-risk assessment."
    )

    with st.form(
        "single_transaction_form"
    ):

        left, right = st.columns(2)

        step = left.number_input(
            "Transaction step (hour)",
            min_value=0,
            value=1,
            step=1,
        )

        tx_type = right.selectbox(
            "Transaction type",
            [
                "PAYMENT",
                "TRANSFER",
                "CASH_OUT",
                "DEBIT",
                "CASH_IN",
            ],
        )

        amount = left.number_input(
            "Transaction amount",
            min_value=0.0,
            value=1000.0,
            step=100.0,
        )

        old_origin = right.number_input(
            "Origin balance before transaction",
            min_value=0.0,
            value=5000.0,
        )

        new_origin = left.number_input(
            "Origin balance after transaction",
            min_value=0.0,
            value=4000.0,
        )

        old_destination = right.number_input(
            "Destination balance before transaction",
            min_value=0.0,
            value=1000.0,
        )

        new_destination = left.number_input(
            "Destination balance after transaction",
            min_value=0.0,
            value=2000.0,
        )

        origin_account = right.text_input(
            "Origin account",
            "CUST-DEMO-001",
        )

        destination_account = left.text_input(
            "Destination account",
            "DEST-DEMO-001",
        )

        submitted = st.form_submit_button(
            "Assess Fraud Risk",
            type="primary",
        )

    if submitted:

        transaction = pd.DataFrame(
            [
                {
                    "step": int(step),
                    "type": tx_type,
                    "amount": float(amount),
                    "nameOrig": origin_account,
                    "oldbalanceOrg": float(
                        old_origin
                    ),
                    "newbalanceOrig": float(
                        new_origin
                    ),
                    "nameDest": destination_account,
                    "oldbalanceDest": float(
                        old_destination
                    ),
                    "newbalanceDest": float(
                        new_destination
                    ),
                    "isFraud": 0,
                    "isFlaggedFraud": 0,
                }
            ]
        )

        try:

            with st.spinner(
                "Assessing transaction risk..."
            ):

                result = (
                    score(transaction)
                    .iloc[0]
                )

            probability = float(
                result["fraud_probability"]
            )

            prediction = int(
                result["prediction"]
            )

            # ------------------------------------------------
            # RESULTS
            # ------------------------------------------------

            c1, c2, c3, c4 = (
                st.columns(4)
            )

            c1.metric(
                "Fraud Probability",
                f"{probability:.2%}",
            )

            c2.metric(
                "Risk Level",
                str(
                    result["risk_level"]
                ),
            )

            c3.metric(
                "Decision",
                str(
                    result["decision"]
                ),
            )

            c4.metric(
                "Model",
                str(
                    result["model_version"]
                ),
            )

            st.subheader(
                "Risk Score"
            )

            st.progress(
                min(
                    max(
                        probability,
                        0.0,
                    ),
                    1.0,
                )
            )

            if prediction == 1:

                st.error(
                    "⚠️ Transaction exceeds the "
                    "production fraud threshold "
                    "and requires the indicated "
                    "control action."
                )

            else:

                st.success(
                    "✅ Transaction is below the "
                    "production fraud threshold."
                )

        except Exception as exc:

            st.error(
                "The transaction could not be scored."
            )

            st.exception(exc)


# ============================================================
# 10. BATCH PREDICTION
# ============================================================

elif page == "Batch Prediction":

    st.title(
        "📁 Batch Fraud Detection"
    )

    st.caption(
        "Upload PaySim-compatible transaction data "
        "and score multiple transactions using the "
        "registered production model."
    )

    uploaded_file = st.file_uploader(
        "Upload transaction CSV",
        type=["csv"],
    )

    if uploaded_file is not None:

        try:

            raw = pd.read_csv(
                uploaded_file
            )

            required_columns = {
                "step",
                "type",
                "amount",
                "oldbalanceOrg",
                "newbalanceOrig",
                "oldbalanceDest",
                "newbalanceDest",
            }

            missing_columns = sorted(
                required_columns
                - set(raw.columns)
            )

            if missing_columns:

                st.error(
                    "Missing required columns: "
                    + ", ".join(
                        missing_columns
                    )
                )

            else:

                st.success(
                    f"Loaded "
                    f"{len(raw):,} transactions."
                )

                st.dataframe(
                    raw.head(20),
                    width="stretch",
                    hide_index=True,
                )

                if st.button(
                    "Run Fraud Detection",
                    type="primary",
                ):

                    with st.spinner(
                        "Scoring transactions..."
                    ):

                        st.session_state[
                            "batch_scored"
                        ] = score(raw)

        except Exception as exc:

            st.error(
                "The uploaded CSV could not be processed."
            )

            st.exception(exc)

    # --------------------------------------------------------
    # BATCH RESULTS
    # --------------------------------------------------------

    if "batch_scored" in st.session_state:

        scored = st.session_state[
            "batch_scored"
        ]

        filtered = risk_filter(
            scored
        )

        flagged_count = int(
            (
                scored["prediction"] == 1
            ).sum()
        )

        critical_count = int(
            (
                scored[
                    "risk_level"
                ].astype(str)
                == "CRITICAL"
            ).sum()
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Transactions Scored",
            f"{len(scored):,}",
        )

        c2.metric(
            "Flagged",
            f"{flagged_count:,}",
        )

        c3.metric(
            "Critical Risk",
            f"{critical_count:,}",
        )

        st.subheader(
            "Scored Transactions"
        )

        batch_results = (
            filtered
            .sort_values(
                "fraud_probability",
                ascending=False,
            )
        )

        st.dataframe(
            batch_results,
            width="stretch",
            hide_index=True,
        )

        csv_data = (
            batch_results
            .to_csv(
                index=False
            )
            .encode("utf-8")
        )

        st.download_button(
            label="Download Scored CSV",
            data=csv_data,
            file_name=(
                "fraud_predictions.csv"
            ),
            mime="text/csv",
        )


# ============================================================
# 11. FRAUD ANALYTICS
# ============================================================

elif page == "Fraud Analytics":

    st.title(
        "📊 Fraud Analytics"
    )

    st.caption(
        "Explore transaction behaviour and "
        "model-generated fraud risk."
    )

    raw = load_sample()

    if raw.empty:

        st.info(
            "Sample transaction data "
            "is unavailable."
        )

    else:

        with st.spinner(
            "Preparing fraud analytics..."
        ):

            scored = score(raw)

        # ----------------------------------------------------
        # FRAUD PROBABILITY BY TYPE
        # ----------------------------------------------------

        st.subheader(
            "Average Fraud Probability "
            "by Transaction Type"
        )

        probability_by_type = (
            scored
            .groupby("type")[
                "fraud_probability"
            ]
            .mean()
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(
            probability_by_type
        )

        # ----------------------------------------------------
        # FLAGGED VALUE BY TYPE
        # ----------------------------------------------------

        st.subheader(
            "Flagged Transaction Value "
            "by Type"
        )

        flagged = scored[
            scored["prediction"] == 1
        ]

        if flagged.empty:

            st.info(
                "No transactions were flagged "
                "by the current model threshold."
            )

        else:

            flagged_value_by_type = (
                flagged
                .groupby("type")[
                    "amount"
                ]
                .sum()
                .sort_values(
                    ascending=False
                )
            )

            st.bar_chart(
                flagged_value_by_type
            )

        # ----------------------------------------------------
        # HOURLY RISK
        # ----------------------------------------------------

        st.subheader(
            "Hourly Risk Pattern"
        )

        hourly_data = scored.assign(
            hour=(
                scored["step"]
                .astype(int)
                % 24
            )
        )

        hourly_risk = (
            hourly_data
            .groupby("hour")[
                "fraud_probability"
            ]
            .mean()
        )

        st.line_chart(
            hourly_risk
        )

        # ----------------------------------------------------
        # INVESTIGATION TABLE
        # ----------------------------------------------------

        st.subheader(
            "Fraud Investigation Queue"
        )

        investigation = (
            risk_filter(scored)
            .sort_values(
                "fraud_probability",
                ascending=False,
            )
        )

        st.dataframe(
            investigation,
            width="stretch",
            hide_index=True,
        )


# ============================================================
# 12. MODEL & DATA MONITORING
# ============================================================

else:

    st.title(
        "📈 Model & Data Monitoring"
    )

    st.caption(
        "Monitor the registered fraud model "
        "and latest data-quality results."
    )

    metrics = meta.get(
        "metrics",
        {},
    )

    # --------------------------------------------------------
    # MODEL KPIs
    # --------------------------------------------------------

    c1, c2, c3, c4 = (
        st.columns(4)
    )

    c1.metric(
        "Model Version",
        meta.get(
            "version",
            "N/A",
        ),
    )

    c2.metric(
        "Decision Threshold",
        f"{float(meta.get('threshold', 0)):.2f}",
    )

    c3.metric(
        "PR-AUC",
        f"{float(metrics.get('pr_auc', 0)):.3f}",
    )

    c4.metric(
        "ROC-AUC",
        f"{float(metrics.get('roc_auc', 0)):.3f}",
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Precision",
        f"{float(metrics.get('precision', 0)):.3f}",
    )

    c2.metric(
        "Recall",
        f"{float(metrics.get('recall', 0)):.3f}",
    )

    c3.metric(
        "F1 Score",
        f"{float(metrics.get('f1', 0)):.3f}",
    )

    st.divider()

    # --------------------------------------------------------
    # MODEL METADATA
    # --------------------------------------------------------

    st.subheader(
        "Registered Model Metadata"
    )

    st.json(meta)

    # --------------------------------------------------------
    # DATA QUALITY
    # --------------------------------------------------------

    st.subheader(
        "Latest Data-Quality Report"
    )

    quality = load_quality()

    if quality:

        st.json(quality)

    else:

        st.info(
            "No data-quality artifact "
            "was found."
        )

    # --------------------------------------------------------
    # DISCLAIMER
    # --------------------------------------------------------

    st.info(
        "Training metrics shown here are "
        "demonstration metrics from the included "
        "synthetic/sample workflow. Production "
        "monitoring should use delayed ground-truth "
        "fraud labels."
    )