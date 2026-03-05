import pandas as pd
from src.validate import validate_bills

def test_validate_bills_passes():
    df = pd.DataFrame([{"id": "TX-1", "title": "Clean Energy Act", "status": "In Committee"}])
    assert validate_bills(df) is True

def test_validate_bills_fails_empty():
    df = pd.DataFrame()
    assert validate_bills(df) is False

def test_validate_bills_fails_duplicate_ids():
    df = pd.DataFrame([
        {"id": "TX-1", "title": "Bill A", "status": "Passed"},
        {"id": "TX-1", "title": "Bill A Duplicate", "status": "Passed"}
    ])
    assert validate_bills(df) is False