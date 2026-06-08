from airflow import DAG
from airflow.operators.bash import BashOperator
from utils.callbacks import on_failure_callback, on_success_callback

from datetime import datetime

default_args = {
    "owner": "gabs",
    "retries": 3,
    "on_failure_callback": on_failure_callback,
}

TASK_CONFIGS = [
    ("bronze_layer",  "cd /app && python3 -m processing.bronze_layer"),
    ("silver_layer",  "cd /app && python3 -m processing.silver_layer"),
    ("gold_layer",    "cd /app && python3 -m processing.gold_layer"),
    ("load_postgres", "cd /app && python3 -m storage.postgres_loader"),
    ("dbt_run",       "cd /app/bcb_dbt && dbt run --profiles-dir /app/bcb_dbt"),
    ("dbt_test",      "cd /app/bcb_dbt && dbt test --profiles-dir /app/bcb_dbt"),
]

with DAG(
    dag_id="bcb_lakehouse_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    tasks = []

    for task_id, command in TASK_CONFIGS:
        task = BashOperator(
            task_id=task_id,
            bash_command=command,
            do_xcom_push=False,
            on_success_callback=on_success_callback,
        )
        tasks.append(task)

    for i in range(len(tasks) - 1):
        tasks[i] >> tasks[i + 1]