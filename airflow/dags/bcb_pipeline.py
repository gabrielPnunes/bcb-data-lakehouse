from airflow import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime

default_args = {
    "owner": "gabs",
    "retries": 3,
}

with DAG(
    dag_id="bcb_lakehouse_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    bronze_task = BashOperator(
        task_id="bronze_layer",
        bash_command="cd /app && python3 -m processing.bronze_layer",
        do_xcom_push=False,
    )

    silver_task = BashOperator(
        task_id="silver_layer",
        bash_command="cd /app && python3 -m processing.silver_layer",
        do_xcom_push=False,
    )

    gold_task = BashOperator(
        task_id="gold_layer",
        bash_command="cd /app && python3 -m processing.gold_layer",
        do_xcom_push=False,
    )

    load_postgres_task = BashOperator(
        task_id="load_postgres",
        bash_command="cd /app && python3 -m storage.postgres_loader",
        do_xcom_push=False,
    )

    dbt_run_task = BashOperator(
        task_id="dbt_run",
        bash_command="cd /app/bcb_dbt && dbt run",
        do_xcom_push=False,
    )

    dbt_test_task = BashOperator(
        task_id="dbt_test",
        bash_command="cd /app/bcb_dbt && dbt test",
        do_xcom_push=False,
    )

    bronze_task >> silver_task >> gold_task >> load_postgres_task >> dbt_run_task >> dbt_test_task