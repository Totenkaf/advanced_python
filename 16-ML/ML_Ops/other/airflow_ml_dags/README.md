# Homework №3
### _To get started_
```
export LOCAL_DATA_DIR=$(pwd)/data
export LOCAL_MLRUNS_DIR=$(pwd)/mlruns
export FERNET_KEY=$(python3 -c "from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)")
docker-compose up --build
```

Airflow now available at http://localhost:8080, _login = admin, password = admin_.

### _To select production model for inference_
In MLFlow at http://localhost:5000/#/models choose model and change its stage to `Production` (before running predict dag in airflow).
![Screenshot from 2022-11-09 00-53-14](https://user-images.githubusercontent.com/66686119/200684195-5f1f4a5e-504a-43a3-8b18-d22ed823fdab.png)
![Screenshot from 2022-11-09 00-58-17](https://user-images.githubusercontent.com/66686119/200684750-36609b08-7ac0-47f6-83cb-cfa72a4282c7.png)


### _To run tests_
```
docker exec -it airflow_ml_dags_scheduler_1 bash
pip3 install pytest
python3 -m pytest --disable-warnings tests/test_dag_structure.py
python3 -m pytest --disable-warnings tests/test_dag_loading.py
```
