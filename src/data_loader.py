import json
import os
from typing import List, Dict

def load_legislators(filepath: str = "data/sample_legislators.json") -> List[Dict]:
    with open(filepath, "r") as f:
        return json.load(f)

def get_legislator(name: str, state: str = None, filepath: str = "data/sample_legislators.json") -> Dict:
    legislators = load_legislators(filepath)
    for leg in legislators:
        if leg["name"].lower() == name.lower():
            if state is None or leg["state"].upper() == state.upper():
                return leg
    raise ValueError(f"Legislator '{name}' not found.")

def format_votes_for_embedding(legislator: Dict) -> List[str]:
    docs = []
    for vote in legislator.get("votes", []):
        doc = (
            f"Legislator: {legislator['name']} ({legislator['party']} - {legislator['state']}) "
            f"voted {vote['vote'].upper()} on {vote['bill_title']} (Bill ID: {vote['bill_id']}) "
            f"on {vote['date']}."
        )
        docs.append(doc)
    return docs