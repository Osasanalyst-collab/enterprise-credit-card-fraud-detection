from pathlib import Path
import numpy as np, pandas as pd
rng = np.random.default_rng(42); n=20_000
transaction_type = rng.choice(["PAYMENT","TRANSFER","CASH_OUT","DEBIT","CASH_IN"], n, p=[.35,.2,.25,.05,.15])
amount = rng.lognormal(8, 1.2, n).round(2)
old_o = rng.lognormal(9, 1.1, n).round(2); new_o = np.maximum(0, old_o-amount).round(2)
old_d = rng.lognormal(8, 1.2, n).round(2); new_d = (old_d+amount).round(2)
fraud_score = ((transaction_type=="TRANSFER")|(transaction_type=="CASH_OUT")) & (amount>np.quantile(amount,.985))
is_fraud = fraud_score.astype(int)
# inject realistic fraudulent balance pattern
new_o[is_fraud==1]=0
frame=pd.DataFrame({"step":rng.integers(1,744,n),"type":transaction_type,"amount":amount,"nameOrig":[f"C{i:09d}" for i in range(n)],"oldbalanceOrg":old_o,"newbalanceOrig":new_o,"nameDest":[f"M{i:09d}" for i in range(n)],"oldbalanceDest":old_d,"newbalanceDest":new_d,"isFraud":is_fraud,"isFlaggedFraud":((is_fraud==1)&(amount>200000)).astype(int)})
path=Path('data/samples/sample_transactions.csv'); path.parent.mkdir(parents=True, exist_ok=True); frame.to_csv(path,index=False); print(f"Generated {len(frame):,} rows at {path}")
