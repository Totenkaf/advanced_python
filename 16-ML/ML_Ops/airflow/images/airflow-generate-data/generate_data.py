"""Copyright 2022 by Artem Ustsov"""

import os

import click
import numpy as np
import pandas as pd

from DataSynthesizer.DataDescriber import DataDescriber
from DataSynthesizer.DataGenerator import DataGenerator
from DataSynthesizer.lib.utils import display_bayesian_network


@click.command("data_generate")
@click.option(
    "--output-dir", type=click.Path(), help="Train data path storage",
)
def generate_data(output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    synthetic_data = os.path.join(output_dir, "synthetic_data.csv")
    generate_synthetic_data(synthetic_data)

    data = pd.read_csv(synthetic_data)
    target_column = data.columns[-1]
    x_data = data.drop(target_column, axis=1)
    y = data[target_column]

    x_data["chest_pain_type"].replace(
        1, np.NaN
    )

    x_data.to_csv(os.path.join(output_dir, "data.csv"), index=False)
    y.to_csv(os.path.join(output_dir, "target.csv"), index=False)
    os.remove(synthetic_data)


def generate_synthetic_data(synthetic_data: str) -> None:
    input_data = "synthetic_data.csv"
    description_file = "description.json"

    categorical_attributes = {
        "sex": True,
        "chest_pain_type": True,
        "fasting_blood_sugar": True,
        "rest_ecg": True,
        "exercise_induced_angina": True,
        "st_slope": True,
        "thalassemia": True,
    }

    describer = DataDescriber(category_threshold=5)
    describer.describe_dataset_in_correlated_attribute_mode(
        dataset_file=input_data,
        epsilon=1,
        k=2,
        attribute_to_is_categorical=categorical_attributes,
    )
    describer.save_dataset_description_to_file(description_file)
    display_bayesian_network(describer.bayesian_network)
    generator = DataGenerator()

    # Number of tuples generated in synthetic dataset.
    num_tuples_to_generate = 200
    generator.generate_dataset_in_correlated_attribute_mode(
        num_tuples_to_generate, description_file
    )
    generator.save_synthetic_data(synthetic_data)

    os.remove(description_file)


if __name__ == "__main__":
    generate_data()
