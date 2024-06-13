"""Copyright 2022 by Artem Ustsov"""

import os

import click
import pandas as pd
from sklearn.model_selection import train_test_split


@click.command("split")
@click.option(
    "--input-dir", type=click.Path(), help="Processed data storage path",
)
@click.option(
    "--output-dir", type=click.Path(), help="Splitted data storage path",
)
def split_data(input_dir: str, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    x_data = pd.read_csv(os.path.join(input_dir, "train_data.csv"))
    y = pd.read_csv(os.path.join(input_dir, "target.csv"))

    x_train, x_val, y_train, y_val = train_test_split(x_data, y, test_size=0.3)

    x_train.to_csv(os.path.join(output_dir, "x_train.csv"), index=False)
    x_val.to_csv(os.path.join(output_dir, "x_val.csv"), index=False)
    y_train.to_csv(os.path.join(output_dir, "y_train.csv"), index=False)
    y_val.to_csv(os.path.join(output_dir, "y_val.csv"), index=False)


if __name__ == "__main__":
    split_data()
