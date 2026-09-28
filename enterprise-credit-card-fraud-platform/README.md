# Enterprise Credit Card Fraud Detection Platform

Production-oriented fraud detection repository adapted from the supplied PaySim-style notebook (6.9M+ rows compatible). It implements a memory-conscious batch pipeline, data validation, feature engineering, model training, threshold optimisation, model registry metadata, FastAPI inference, monitoring, PostgreSQL persistence, Docker, Airflow, dbt, CI/CD and staged enterprise deployment templates.

## What is executable now
- Local batch ingestion from CSV (chunked)
- Schema and data-quality validation
- Corrected balance features and time/behavioural features
- Leakage-aware model dataset creation
- Logistic Regression baseline and HistGradientBoosting candidate
- Imbalance handling with class/sample weights
- PR-AUC-focused evaluation and business-cost threshold selection
- Versioned model artifact and model card JSON
- Batch scoring and FastAPI real-time scoring
- SQLite by default; PostgreSQL through `DATABASE_URL`
- Unit tests, Docker Compose, GitHub Actions, Airflow DAG starter, dbt models

Kafka, Kubernetes, Terraform and managed cloud services are included as production-ready templates and require environment-specific credentials/infrastructure.

## Quick start
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/macOS
python scripts/generate_sample_data.py
python -m fraud_detection.cli run-all --input data/samples/sample_transactions.csv
uvicorn api.main:app --reload
```

## Session workflow
Run the scripts in `sessions/` in numerical order. Each session is independently documented and builds toward the final production workflow.

## Dataset columns expected
`step,type,amount,nameOrig,oldbalanceOrg,newbalanceOrig,nameDest,oldbalanceDest,newbalanceDest,isFraud,isFlaggedFraud`

## Important correction from the original notebook
Destination balance movement is calculated as:
```python
balance_diff_dest = newbalanceDest - oldbalanceDest
```

## Repository map
- `src/fraud_detection/`: production Python package
- `sessions/`: session-by-session executable workflow
- `api/`: FastAPI model service
- `orchestration/airflow/`: Airflow DAGs
- `dbt/`: warehouse transformation project
- `database/`: SQL schemas and analytics queries
- `infrastructure/`: Docker, Kubernetes and Terraform templates
- `tests/`: automated tests
- `docs/`: architecture, data contract, deployment and monitoring guides
