a57ac3e (Initial commit: legislative data pipeline)
# Legislative Data Pipeline

A production-style ETL pipeline that ingests state legislative bill data from the Open States API, transforms and stores it in PostgreSQL, and generates summary reports to support civic data analysis and climate policy tracking.

## Tech Stack
- Python, Pandas, Requests
- PostgreSQL
- Apache Airflow
- pytest
- python-dotenv

## Project Structure
legislative-pipeline/
├── src/
│   ├── ingest.py
│   ├── transform.py
│   ├── load.py
│   ├── validate.py
│   ├── report.py
│   └── db.py
├── dags/
│   └── legislative_dag.py
├── sql/
│   └── schema.sql
├── tests/
│   ├── test_ingest.py
│   ├── test_transform.py
│   └── test_validate.py
├── .env.example
├── requirements.txt
└── README.md

## Setup
1. pip install -r requirements.txt
2. cp .env.example .env and fill in credentials
3. python -m src.db
4. python -m src.ingest --state TX --keyword "climate"
5. python -m src.report --state TX --output reports/tx_climate.csv

## Airflow DAG
ingest_bills >> validate_raw >> transform_bills >> load_to_postgres >> generate_report

## Roadmap
- Add LegiScan API as secondary source
- Add district-level demographic enrichment
- Streamlit dashboard
- GCP Cloud Run deployment
```

---

**requirements.txt**
```
requests==2.31.0
pandas==2.1.0
psycopg2-binary==2.9.7
python-dotenv==1.0.0
apache-airflow==2.7.0
pytest==7.4.0

sqlalchemy==2.0.20

# legislative-pipeline
1b8c6a3121ed9e6564fec77978ebd03eeea9a4f8

sqlalchemy==2.0.20
a57ac3e (Initial commit: legislative data pipeline)
