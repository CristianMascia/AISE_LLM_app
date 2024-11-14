from __future__ import annotations
import datetime
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from utils.summarize import LLMSummarizer
from utils.clustering import Clusterer
import logging

logging.basicConfig(level=logging.INFO)

date = datetime.datetime.now().strftime("%Y%m%d")
file_name = f"taxi-rides-{date}.json"

with DAG(
    dag_id="ETML",
    start_date=pendulum.datetime(2024, 10, 14),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    logging.info("DAG started ...")
    logging.info("Extracting and clustering data ...")

    extract_cluster_load_task = PythonOperator(
        task_id="extract_cluster_save",
        python_callable=Clusterer(file_name).cluster_and_label,
        op_kwargs={"features": ["ride_dist", "ride_time"]}
    )

    logging.info("Extracting and summarizing data ...")

    extract_summarize_load_task = PythonOperator(
        task_id="extract_summarize",
        python_callable=LLMSummarizer(file_name).summarize
    )
    extract_cluster_load_task >> extract_summarize_load_task
