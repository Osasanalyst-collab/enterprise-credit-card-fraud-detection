import pandas as pd, pytest
from fraud_detection.ingestion.schema_validation import validate_schema
from fraud_detection.utils.exceptions import DataContractError

def test_missing_columns_raise_contract_error():
    with pytest.raises(DataContractError): validate_schema(pd.DataFrame({"amount":[1]}))
