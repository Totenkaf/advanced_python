"""Copyright 2022 by Artem Ustsov"""

import os
import pickle

import click
import pandas as pd
import sklearn.model_selection as selection
from sklearn.linear_model import LogisticRegressionCV


@click.command("train")
@click.option(
    "--input-dir", type=click.Path(), help="Splitted data storage path",
)
@click.option(
    "--output-dir", type=click.Path(), help="Model storage path",
)
def train(input_dir: str, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)

    x_data = pd.read_csv(os.path.join(input_dir, "x_train.csv"))
    y = pd.read_csv(os.path.join(input_dir, "y_train.csv"))

    model = LogisticRegressionCV(
        penalty="l2",
        cv=selection.StratifiedKFold(20),
        max_iter=10000,
        tol=0.001,
    )
    model.fit(x_data, y)

    with open(os.path.join(output_dir, "LogisticRegressionCV.pkl"), "wb") as f:
        pickle.dump(model, f)


if __name__ == "__main__":
    train()
