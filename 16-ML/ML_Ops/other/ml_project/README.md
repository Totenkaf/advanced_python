# Homework №1
### _To install requirements_
Activate your virtual environment, depending on which virtual environement you're using (e.g. venv, virtualenvwrapper, conda, etc.), then run from `ml_prject/`:
```
pip3 install -r requirements.txt
pip3 install mlflow --no-warn-conflicts
```

### _To get started_
Get the data:
```
dvc pull -r gdrive
```
Run MLFlow server
```
mlflow server --backend-store-uri sqlite:///:memory --default-artifact-root ./mlruns
```
### _To run EDA_
Find a report at `reports/eda_report.html` or from `ml_prject/` run to generate a new file:
```
python3 src/data/create_eda_report.py --path_to_csv <path_to_csv> --path_to_report <path_to_report>
```
Default run: 
```
python3 src/data/create_eda_report.py
```
is equivalent to:
```
python3 src/data/create_eda_report.py data/raw/heart_cleveland_upload.csv reports/eda_report.html
```
### _To run Training Pipeline_
From `ml_prject` run to get KNN classifier (default):
```
python3 src/train_pipeline.py hydra.job.chdir=False
```
Run to get LogisticRegression classifier:

```
python3 src/train_pipeline.py model=logreg hydra.job.chdir=False
```
### _To run Prediction Pipeline_
From `ml_prject` run:
```
python3 src/predict_pipeline.py --path_to_model <path_to_model> --path_to_transformer <path_to_transformer> --path_to_csv <path_to_csv> --path_to_prediction <path_to_prediction>
```
To get more info about the options use:
```
python3 src/predict_pipeline.py --help
```
To run default example:
```
python3 src/predict_pipeline.py
```

### _To run Tests_
Generate synthetic data:
```
python3 tests/generate_synthetic_data.py
```
You can find the data and it's statistics in `tests/synthetic_data`

Run tests (may take a while):
```
python3 -m unittest tests
```
