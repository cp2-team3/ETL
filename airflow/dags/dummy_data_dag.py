from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from dummy_article import board_api, signin_api
import random

def create_data():
    for i in range(5):
        user = "test"+str(random.randint(1,10000))
        title = "Dummy Article"
        content = "This is for making bulk log data"
        board_api(method='POST', title=title, content=content, id=user)

dag = DAG(
        dag_id = 'dummy_data_dag',
        start_date = datetime(2023,3,1),
        schedule_interval = '1 * * * *'
    )

create_data_task = PythonOperator(
        task_id = 'create_data_task',
        python_callable = create_data,
        dag = dag
    )

create_data_task