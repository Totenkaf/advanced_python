import matplotlib.pyplot as plt
import pandas as pd
from DataSynthesizer.DataDescriber import DataDescriber
from DataSynthesizer.DataGenerator import DataGenerator
from DataSynthesizer.lib.utils import display_bayesian_network, read_json_file
from DataSynthesizer.ModelInspector import ModelInspector

# input dataset
input_data = 'data/raw/heart_cleveland_upload.csv'
# location of two output files
mode = 'correlated_attribute_mode'
description_file = 'tests/synthetic_data/description.json'
synthetic_data = 'tests/synthetic_data/synthetic_data.csv'

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

# Read both datasets using Pandas.
input_df = pd.read_csv(input_data, skipinitialspace=True)
synthetic_df = pd.read_csv(synthetic_data)
# Read attribute description from the dataset description file.
attribute_description = read_json_file(description_file)['attribute_description']

inspector = ModelInspector(input_df, synthetic_df, attribute_description)

for attribute in synthetic_df.columns:
    inspector.compare_histograms(attribute)
    plt.suptitle(f'{attribute.upper()}')
    plt.savefig(f'tests/synthetic_data/statistics/{attribute}_histogram.png')

inspector.mutual_information_heatmap()
plt.savefig('tests/synthetic_data/statistics/heatmap.png')
