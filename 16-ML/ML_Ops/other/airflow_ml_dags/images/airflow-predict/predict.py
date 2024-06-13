import os

import click
import pandas as pd
import mlflow.pyfunc


@click.command('predict')
@click.option('--input-dir', type=click.Path(),
              help='Path to input data')
@click.option('--output-dir', type=click.Path(),
              help='Path to store metrics')
def predict(input_dir: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    X = pd.read_csv(os.path.join(input_dir, 'train_data.csv'))  # processed data

    mlflow.set_tracking_uri("http://localhost:5000")
    # fetch latest production model
    model = mlflow.pyfunc.load_model(
        model_uri='models:/rf_model/Production'
    )
    y_pred = model.predict(X)
    pd.DataFrame(y_pred).to_csv(os.path.join(output_dir, 'predictions.csv'), index=False)


if __name__ == '__main__':
    predict()
