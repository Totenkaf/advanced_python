"""Copyright 2022 by Artem Ustsov"""

import os
import shutil

import click
import pandas as pd
from sklearn.impute import SimpleImputer


@click.command("preprocess")
@click.option(
    "--input-dir", type=click.Path(), help="Train data storage path",
)
@click.option(
    "--output-dir", type=click.Path(), help="Processed data storage path",
)
def preprocess_data(input_dir: str, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    data = pd.read_csv(os.path.join(input_dir, "data.csv"))

    inputer = SimpleImputer(strategy="most_frequent")
    x_data = inputer.fit_transform(data)
    processed_data = pd.DataFrame(x_data, columns=data.columns)
    processed_data.to_csv(
        os.path.join(output_dir, "train_data.csv"),
        index=False,
    )

    shutil.copyfile(
        os.path.join(input_dir, "target.csv"),
        os.path.join(output_dir, "target.csv"),
    )


if __name__ == "__main__":
    preprocess_data()
