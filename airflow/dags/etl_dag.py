from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import gzip
import shutil
import boto3

def run_etl():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%dT%H:%M")
    file_name = f"/home/ubuntu/Backend/logs/{timestamp}.log.gz"
    with open('/home/ubuntu/Backend/logs/json_logger.log', 'rb+') as f_in:
        with gzip.open(file_name, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        f_in.truncate(0)

    s3 = boto3.resource('s3',aws_access_key_id='######',aws_secret_access_key='#######')
    path = f"{now.year}/{now.month}/{now.day}/{now.hour}"
    s3.Bucket('######').upload_file(file_name, path)

dag = DAG(
        dag_id = 'etl_dag',
        start_date = datetime(2023,3,1),
        schedule_interval = '1 * * * *'
    )

run_etl_task = PythonOperator(
    task_id = 'run_etl_task',
    python_callable = run_etl,
    dag = dag
)

run_etl_task