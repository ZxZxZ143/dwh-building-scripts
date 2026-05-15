from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="load_bronze_sources",
    description="Load PostgreSQL, CSV and JSON sources into DWH bronze layer",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["dwh", "bronze", "etl"],
) as dag:

    load_abs_tables = BashOperator(
        task_id="load_abs_tables",
        bash_command="PYTHONPATH=/opt/airflow python /opt/airflow/scripts/abs/load_abs_to_dwh.py",
    )

    load_loan_system_tables = BashOperator(
        task_id="load_loan_system_tables",
        bash_command="PYTHONPATH=/opt/airflow python /opt/airflow/scripts/loan/load_loan_system_to_dwh.py",
    )

    load_card_processing_tables = BashOperator(
        task_id="load_card_processing_tables",
        bash_command="PYTHONPATH=/opt/airflow python /opt/airflow/scripts/card/load_card_system_to_dwh.py",
    )

    load_aml_alerts_csv = BashOperator(
        task_id="load_aml_alerts_csv",
        bash_command="PYTHONPATH=/opt/airflow python /opt/airflow/scripts/aml_alerts/load_aml_alerts_to_dwh.py",
    )

    load_dbo_json = BashOperator(
        task_id="load_dbo_json",
        bash_command="PYTHONPATH=/opt/airflow python /opt/airflow/scripts/dbo/load_dbo_to_dwh.py",
    )

    [
        load_abs_tables,
        load_loan_system_tables,
        load_card_processing_tables,
        load_aml_alerts_csv,
        load_dbo_json,
    ]