from src.embeddings import get_or_create_collection
from typing import List

def retrieve_votes(legislator_name: str, n_results: int = 10) -> List[str]:
    collection = get_or_create_collection()
    results = collection.query(
        query_texts=[f"votes by {legislator_name} on climate energy environment bills"],
        n_results=n_results
    )
    docs = results.get("documents", [[]])[0]
    return docs