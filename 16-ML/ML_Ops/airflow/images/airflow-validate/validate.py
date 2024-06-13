"""Copyright 2022 by Artem Ustsov"""

import json
import os
import pickle

import click
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score


@click.command("validate")
@click.option("--input-dir", type=click.Path(), help="Path to splitted data")
@click.option("--model-dir", type=click.Path(), help="Path to model")
@click.option("--output-dir", type=click.Path(), help="Path to store metrics")
def validate(
        input_dir: str,
        model_dir: str,
        output_dir: str,
):
    model_name = os.listdir(model_dir)[0]
    os.makedirs(output_dir, exist_ok=True)
    x_data = pd.read_csv(os.path.join(input_dir, "x_val.csv"))
    y_true = pd.read_csv(os.path.join(input_dir, "y_val.csv"))

    with open(os.path.join(model_dir, model_name), "rb") as model_file:
        model = pickle.load(model_file)
    y_pred = model.predict(x_data)

    metrics = dict()
    metrics["accuracy"] = accuracy_score(y_true, y_pred)
    metrics["f1_score"] = f1_score(y_true, y_pred)

    with open(os.path.join(output_dir, "metric.json"), "w") as metric_file:
        json.dump(metrics, metric_file)


if __name__ == "__main__":
    validate()
