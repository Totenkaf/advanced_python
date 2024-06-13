import os
import pickle

import click
import mlflow
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


@click.command('train')
@click.option('--input-dir', type=click.Path(),
              help='Path to splitted data')
@click.option('--output-dir', type=click.Path(),
              help='Path to store model')
def train(input_dir: str, output_dir: str):
    mlflow.set_tracking_uri("http://localhost:5000")
    with mlflow.start_run(run_name='train'):
        run = mlflow.active_run()

        os.makedirs(output_dir, exist_ok=True)
        X = pd.read_csv(os.path.join(input_dir, 'x_train.csv'))
        y = pd.read_csv(os.path.join(input_dir, 'y_train.csv'))

        model = RandomForestClassifier(max_depth=5)
        model.fit(X, y)

        model_params = model.get_params()
        for param in model_params:
            mlflow.log_param(param, model_params[param])

        with open(os.path.join(output_dir, f'rf_model_{run.info.run_id}.pkl'), 'wb') as f:
            pickle.dump(model, f)

        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="classification_model",
            registered_model_name='rf_model')


if __name__ == '__main__':
    train()
