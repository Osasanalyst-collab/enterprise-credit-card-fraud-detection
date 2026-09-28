import pandas as pd
from fraud_detection.transformation.clean_transactions import clean_transactions

def test_cleaning_removes_duplicates_and_standardises_type():
    row={"step":1,"type":" transfer ","amount":10,"oldbalanceOrg":20,"newbalanceOrig":10,"oldbalanceDest":0,"newbalanceDest":10,"isFraud":0,"isFlaggedFraud":0}
    out=clean_transactions(pd.DataFrame([row,row]))
    assert len(out)==1 and out.loc[0,"type"]=="TRANSFER"
