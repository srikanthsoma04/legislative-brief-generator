import pandas as pd
import argparse
import logging
from src.db import get_connection

logger = logging.getLogger(__name__)

def generate_report(state: str, output: str = None):
    conn = get_connection()
    query = """
        SELECT b.id, b.title, b.status, b.introduced_date,
               s.name AS sponsor_name, s.party
        FROM bills b
        LEFT JOIN sponsors s ON b.id = s.bill_id AND s.role = 'primary'
        WHERE b.state ILIKE %s
        ORDER BY b.introduced_date DESC
    """
    df = pd.read_sql(query, conn, params=(f"%{state}%",))
    conn.close()
    print(f"\nState: {state.upper()}  |  Total bills: {len(df)}")
    print("-" * 50)
    print(df["status"].value_counts().to_string())
    print("\nTop sponsors:")
    print(df["sponsor_name"].value_counts().head(5).to_string())
    if output:
        df.to_csv(output, index=False)
        logger.info(f"Report saved to {output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    generate_report(args.state, args.output)