import pandas as pd
import logging
from src.db import get_connection

logger = logging.getLogger(__name__)

def load_bills(df: pd.DataFrame):
    conn = get_connection()
    cur = conn.cursor()
    inserted = 0
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO bills (id, state, session, title, description, status, introduced_date, updated_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                status = EXCLUDED.status,
                updated_date = EXCLUDED.updated_date
        """, (row["id"], row["state"], row["session"], row["title"],
              row["description"], row["status"], row["introduced_date"], row["updated_date"]))
        inserted += 1
    conn.commit()
    cur.close()
    conn.close()
    logger.info(f"Loaded {inserted} bills into PostgreSQL.")

def load_sponsors(df: pd.DataFrame):
    conn = get_connection()
    cur = conn.cursor()
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO sponsors (bill_id, name, party, role)
            VALUES (%s, %s, %s, %s)
        """, (row["bill_id"], row["name"], row["party"], row["role"]))
    conn.commit()
    cur.close()
    conn.close()
    logger.info(f"Loaded {len(df)} sponsors into PostgreSQL.")
