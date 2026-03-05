import pytest
from src.data_loader import load_legislators, get_legislator, format_votes_for_embedding

def test_load_legislators():
    legislators = load_legislators()
    assert len(legislators) > 0
    assert "name" in legislators[0]
    assert "votes" in legislators[0]

def test_get_legislator_found():
    leg = get_legislator("Jane Smith", "TX")
    assert leg["name"] == "Jane Smith"
    assert leg["state"] == "TX"

def test_get_legislator_not_found():
    with pytest.raises(ValueError):
        get_legislator("Nobody Here", "TX")

def test_format_votes_for_embedding():
    leg = get_legislator("Jane Smith", "TX")
    docs = format_votes_for_embedding(leg)
    assert len(docs) == len(leg["votes"])
    assert "Jane Smith" in docs[0]
    assert "voted" in docs[0].lower()
```

---

That is the complete Project 5. Same process as before — create the folder structure on your computer, copy each file in, then push to GitHub. The `.gitignore` from before covers this repo too so create a new one with the same content including `chroma_db/` to avoid pushing the vector database:
```
.env
__pycache__/
*.pyc
.DS_Store
chroma_db/