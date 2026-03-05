import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", 5432),
        dbname=os.getenv("POSTGRES_DB", "legislative_db"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

def initialize_schema():
    conn = get_connection()
    cur = conn.cursor()
    with open("sql/schema.sql", "r") as f:
        cur.execute(f.read())
    conn.commit()
    cur.close()
    conn.close()
    print("Schema initialized successfully.")

if __name__ == "__main__":
    initialize_schema()