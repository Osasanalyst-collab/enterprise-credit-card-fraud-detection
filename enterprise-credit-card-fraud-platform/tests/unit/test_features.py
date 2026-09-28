import pandas as pd
from fraud_detection.features.build_features import build_features

def test_destination_balance_difference_is_correct():
    df=pd.DataFrame([{"step":1,"type":"TRANSFER","amount":50,"oldbalanceOrg":100,"newbalanceOrig":50,"oldbalanceDest":20,"newbalanceDest":70}])
    out=build_features(df)
    assert out.loc[0,"balance_diff_dest"]==50
    assert out.loc[0,"dest_error"]==0
