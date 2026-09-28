# Streamlit Fraud Operations Center

Run from the repository root:

```powershell
pip install -r requirements.txt
streamlit run dashboard/app.py
```

The app reuses `FraudPredictor`, the registered model in `artifacts/models/`, and the shared production feature engineering code.

Pages:
- Executive Dashboard
- Single Transaction
- Batch Prediction
- Fraud Analytics
- Model Monitoring
