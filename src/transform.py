import pandas as pd
from datetime import datetime

def transform_bills(raw_bills: list) -> pd.DataFrame:
    records = []
    for bill in raw_bills:
        records.append({
            "id": bill.get("id"),
            "state": bill.get("jurisdiction", {}).get("name", ""),
            "session": bill.get("session"),
            "title": bill.get("title", "").strip(),
            "description": bill.get("abstracts", [{}])[0].get("abstract", "") if bill.get("abstracts") else "",
            "status": bill.get("latest_action_description", ""),
            "introduced_date": bill.get("first_action_date"),
            "updated_date": bill.get("updated_at"),
        })
    df = pd.DataFrame(records)
    df["introduced_date"] = pd.to_datetime(df["introduced_date"], errors="coerce").dt.date
    df["updated_date"] = pd.to_datetime(df["updated_date"], errors="coerce")
    df.drop_duplicates(subset=["id"], inplace=True)
    return df

def transform_sponsors(raw_bills: list) -> pd.DataFrame:
    records = []
    for bill in raw_bills:
        for sponsor in bill.get("sponsorships", []):
            records.append({
                "bill_id": bill.get("id"),
                "name": sponsor.get("name", ""),
                "party": sponsor.get("party", ""),
                "role": "primary" if sponsor.get("primary") else "cosponsor"
            })
    return pd.DataFrame(records)

def transform_votes(raw_bills: list) -> pd.DataFrame:
    records = []
    for bill in raw_bills:
        for vote in bill.get("votes", []):
            records.append({
                "id": vote.get("id"),
                "bill_id": bill.get("id"),
                "vote_date": vote.get("date"),
                "yes_count": vote.get("counts", [{}])[0].get("value", 0),
                "no_count": vote.get("counts", [{}])[1].get("value", 0) if len(vote.get("counts", [])) > 1 else 0,
                "passed": vote.get("result") == "pass"
            })
    df = pd.DataFrame(records)
    if not df.empty:
        df["vote_date"] = pd.to_datetime(df["vote_date"], errors="coerce").dt.date
    return df