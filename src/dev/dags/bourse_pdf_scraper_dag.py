from airflow import DAG
from airflow.operators.python import PythonOperator  # type: ignore
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/opt/airflow/src')
from src.run_pipeline import main as run_pipeline_main



default_args = {  
    'owner': 'airflow',
    'start_date': datetime(2025, 8, 11),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'bourse_pdf_scraper',
    default_args=default_args,
    schedule_interval='@weekly',
    catchup=False,
) as dag:

    task_pipeline = PythonOperator(
        task_id='run_full_pipeline',
        python_callable=run_pipeline_main,
    )
