import os
import requests
import argparse
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://v3.openstates.org"

def fetch_bills(state: str, keyword: str, page: int = 1) -> dict:
    api_key = os.getenv("OPENSTATES_API_KEY")
    if not api_key:
        raise ValueError("OPENSTATES_API_KEY not set in environment.")
    headers = {"X-API-KEY": api_key}
    params = {
        "jurisdiction": state.lower(),
        "q": keyword,
        "page": page,
        "per_page": 20,
        "include": ["sponsorships", "votes"]
    }
    response = requests.get(f"{BASE_URL}/bills", headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def ingest(state: str, keyword: str) -> list:
    all_bills = []
    page = 1
    while True:
        logger.info(f"Fetching page {page} for state={state}, keyword={keyword}")
        data = fetch_bills(state, keyword, page)
        results = data.get("results", [])
        if not results:
            break
        all_bills.extend(results)
        if not data.get("pagination", {}).get("next_page"):
            break
        page += 1
    logger.info(f"Total bills fetched: {len(all_bills)}")
    return all_bills

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True)
    parser.add_argument("--keyword", default="climate")
    args = parser.parse_args()
    bills = ingest(args.state, args.keyword)
    print(f"Fetched {len(bills)} bills for {args.state} / {args.keyword}")