from airflow import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime


with DAG(
    dag_id="bcb_lakehouse_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    bronze_task = BashOperator(
        task_id="bronze_layer",
        bash_command="cd /app && python3 -m processing.bronze_layer"
    )

    silver_task = BashOperator(
        task_id="silver_layer",
        bash_command="cd /app && python3 -m processing.silver_layer"
    )

    gold_task = BashOperator(
        task_id="gold_layer",
        bash_command="cd /app && python3 -m processing.gold_layer"
    )

    bronze_task >> silver_task >> gold_task