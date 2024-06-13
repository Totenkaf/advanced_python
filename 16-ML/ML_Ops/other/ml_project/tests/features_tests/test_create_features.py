import os
import sys
import unittest

import numpy as np

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH, 'src'
)
sys.path.append(SOURCE_PATH)

from entities import FeatureParams, FeatureProcessingParams
from features import create_transformer, process_features
from tests.data_tests import TestDataModule


class TestFeaturesModule(TestDataModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.categorical = ['sex', 'cp', 'fbs', 'restecg', 'slope', 'exang', 'ca', 'thal']
        self.numerical = ['age', 'trestbps', 'chol', 'thalach', 'slope']

        fp = FeatureParams(categorical=self.categorical,
                           numerical=self.numerical,
                           target_column=self.target_column)
        fpp = FeatureProcessingParams()
        self.tf = create_transformer(fp, fpp)

        self.tf.fit(self.X_train)
        self.X_train = process_features(self.tf, self.X_train)
        self.X_test = process_features(self.tf, self.X_test)

    def test_create_transformer(self):
        self.assertEqual(len(self.tf.transformers), 2)

    def test_process_features(self):
        self.assertEqual(self.X_train.shape, (160, 28))
        self.assertEqual(self.X_test.shape, (40, 28))

        self.assertIsInstance(self.X_train, np.ndarray)
        self.assertIsInstance(self.X_test, np.ndarray)

    def test_read_data(self):
        pass

    def test_extract_target_variable(self):
        pass

    def test_split_train_test_data(self):
        pass


if __name__ == '__main__':
    unittest.main()
