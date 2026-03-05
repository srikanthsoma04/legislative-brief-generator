from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.ingest import ingest
from src.transform import transform_bills, transform_sponsors, transform_votes
from src.validate import validate_bills
from src.load import load_bills, load_sponsors

default_args = {
    "owner": "srikanth",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
}

with DAG(
    dag_id="legislative_pipeline",
    default_args=default_args,
    description="Daily ingestion of state legislative bill data from Open States API",
    schedule_interval="0 6 * * *",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["civic", "legislative", "climate"],
) as dag:

    def run_ingest(**context):
        bills = ingest(state="TX", keyword="climate")
        context["ti"].xcom_push(key="raw_bills", value=bills)

    def run_validate(**context):
        bills = context["ti"].xcom_pull(key="raw_bills")
        df = transform_bills(bills)
        assert validate_bills(df), "Data validation failed — pipeline halted."
        context["ti"].xcom_push(key="bills_df", value=df.to_dict())

    def run_load(**context):
        import pandas as pd
        bills = context["ti"].xcom_pull(key="raw_bills")
        bills_df = pd.DataFrame(context["ti"].xcom_pull(key="bills_df"))
        sponsors_df = transform_sponsors(bills)
        load_bills(bills_df)
        load_sponsors(sponsors_df)

    ingest_task = PythonOperator(task_id="ingest_bills", python_callable=run_ingest)
    validate_task = PythonOperator(task_id="validate_raw", python_callable=run_validate)
    load_task = PythonOperator(task_id="load_to_postgres", python_callable=run_load)

    ingest_task >> validate_task >> load_task