# VK Technopark-BMSTU | SEM II, ML OPS | HW_3

================================================================ 

Усцов Артем Алексеевич.  
Группа ML-21.  
Преподаватели: Михаил Марюфич


## Quick Start
~~~
export LOCAL_DATA_DIR=$(pwd)/data
export FERNET_KEY=$(python3 fernet_gen.py)
docker-compose up --build
~~~

Airflow is now available on: http://127.0.0.1:8080   
- login = admin  
- password = admin  

### Run Tests
~~~
docker exec -it airflow-scheduler-1 bash
python3 -m pytest --disable-warnings tests/test_dag_structure.py
python3 -m pytest --disable-warnings tests/test_dag_loading.py
~~~
