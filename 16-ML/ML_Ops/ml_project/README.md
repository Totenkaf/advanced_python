[![.github/workflows/ci.yml](https://github.com/made-mlops-2022/artem_ustsov/actions/workflows/ci.yml/badge.svg)](https://github.com/made-mlops-2022/artem_ustsov/actions/workflows/ci.yml)
# VK Technopark-BMSTU | SEM II, ML OPS | HW_1

================================================================ 

Усцов Артем Алексеевич.  
Группа ML-21.  
Преподаватели: Михаил Марюфич



## Quick start

### Installation
Install dependencies with:
~~~
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
~~~


### Data downloading
Download training data from s3 bucket with:
~~~
python3 ml_project/download_data_from_s3.py configs/config_1.yaml
~~~

### Make EDA
You can make exploratory analysis only after downloading
~~~
python3 ml_project/make_eda.py configs/config_1.yaml
~~~

### Make predictions
You may use several configs to train model with
different parameters and make predictions on it

- Model I. Train & Predict
~~~
python3 ml_project/fit_pipeline.py configs/config_1.yaml
python3 ml_project/predict_pipeline.py configs/config_1.yaml
~~~

- Model II. Train & Predict
~~~
python3 ml_project/fit_pipeline.py configs/config_2.yaml
python3 ml_project/predict_pipeline.py configs/config_2.yaml
~~~

All data sourcing in remote MLRegistry Server
MLFlow Service is available on: http://5.188.141.0:8000/

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- Homework description.
    ├── data
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── ml_example                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- code to download or generate data
    │   │
    │   ├── features       <- code to turn raw data into features for modeling
    │   │
    │   ├── models         <- code to train models and then use trained models to make
    │   │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io