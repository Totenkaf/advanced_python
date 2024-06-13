import os

import click
import numpy as np
import pandas as pd
from DataSynthesizer.DataDescriber import DataDescriber
from DataSynthesizer.DataGenerator import DataGenerator
from DataSynthesizer.lib.utils import display_bayesian_network


@click.command('generate')
@click.option('--output-dir', type=click.Path(),
              help='Path to store train data')
def generate_data(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    synthetic_data = os.path.join(output_dir, 'synthetic_data.csv')
    generate_synthetic_data(synthetic_data)

    data = pd.read_csv(synthetic_data)
    target_column = data.columns[-1]
    X = data.drop(target_column, axis=1)
    y = data[target_column]
    X['cp'].replace(2, np.NaN)  # to create some missing values to process later

    X.to_csv(os.path.join(output_dir, 'data.csv'), index=False)
    y.to_csv(os.path.join(output_dir, 'target.csv'), index=False)
    os.remove(synthetic_data)


def generate_synthetic_data(synthetic_data: str):
    # input dataset
    input_data = 'synthetic_data.csv'
    # location of two output files
    description_file = 'description.json'

    # An attribute is categorical if its domain size is less than this threshold.
    # Here modify the threshold to adapt to the domain size of 'education' (which is 14 in input dataset).
    threshold_value = 5

    # specify categorical attributes
    categorical_attributes = {'sex': True, 'cp': True, 'fbs': True, 'restecg': True, 'exang': True, 'ca': True, 'thal': True}


    # A parameter in Differential Privacy. It roughly means that removing a row in the input dataset will not
    # change the probability of getting the same output more than a multiplicative difference of exp(epsilon).
    # Increase epsilon value to reduce the injected noises. Set epsilon=0 to turn off differential privacy.
    epsilon = 1

    # The maximum number of parents in Bayesian network, i.e., the maximum number of incoming edges.
    degree_of_bayesian_network = 2

    # Number of tuples generated in synthetic dataset.
    num_tuples_to_generate = 200

    describer = DataDescriber(category_threshold=threshold_value)
    describer.describe_dataset_in_correlated_attribute_mode(dataset_file=input_data,
                                                            epsilon=epsilon,
                                                            k=degree_of_bayesian_network,
                                                            attribute_to_is_categorical=categorical_attributes)
    describer.save_dataset_description_to_file(description_file)
    display_bayesian_network(describer.bayesian_network)
    generator = DataGenerator()
    generator.generate_dataset_in_correlated_attribute_mode(num_tuples_to_generate, description_file)
    generator.save_synthetic_data(synthetic_data)
    os.remove(description_file)


if __name__ == '__main__':
    generate_data()
