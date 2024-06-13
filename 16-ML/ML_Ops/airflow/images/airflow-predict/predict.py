"""Copyright 2022 by Artem Ustsov"""

import os
import pickle

import click
import pandas as pd


@click.command("predict")
@click.option("--input-dir", type=click.Path(), help="Input data path")
@click.option("--output-dir", type=click.Path(), help="Metrics storage path")
def predict(input_dir: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, "LogisticRegressionCV.pkl"), "wb") as f:
        model = pickle.load(f)
        x_data = pd.read_csv(os.path.join(input_dir, "train_data.csv"))
        y_pred = model.predict(x_data)
        pd.DataFrame(y_pred).to_csv(
            os.path.join(output_dir, "predictions.csv"),
            index=False,
        )


if __name__ == "__main__":
    predict()
