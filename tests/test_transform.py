import pytest
from src.transform import transform_bills, transform_sponsors

SAMPLE_BILLS = [
    {
        "id": "TX-HB1234",
        "jurisdiction": {"name": "TX"},
        "session": "2025",
        "title": "Clean Energy Grid Act",
        "abstracts": [{"abstract": "Establishes clean energy standards."}],
        "latest_action_description": "In Committee",
        "first_action_date": "2025-01-15",
        "updated_at": "2025-02-01T00:00:00Z",
        "sponsorships": [{"name": "Jane Smith", "party": "Democratic", "primary": True}],
        "votes": []
    }
]

def test_transform_bills_columns():
    df = transform_bills(SAMPLE_BILLS)
    assert "id" in df.columns
    assert "title" in df.columns
    assert "status" in df.columns
    assert len(df) == 1

def test_transform_bills_no_duplicates():
    df = transform_bills(SAMPLE_BILLS * 3)
    assert len(df) == 1

def test_transform_sponsors():
    df = transform_sponsors(SAMPLE_BILLS)
    assert len(df) == 1
    assert df.iloc[0]["name"] == "Jane Smith"
    assert df.iloc[0]["role"] == "primary"