import os
import sys
import unittest

import numpy as np
import pandas as pd

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH, 'src'
)
sys.path.append(SOURCE_PATH)

from data import extract_target_variable, read_data, split_train_test_data
from entities import SplittingParams

unittest.TestLoader.sortTestMethodsUsing = None


class TestDataModule(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_file = 'tests/synthetic_data/synthetic_data.csv'
        self.target_column = 'condition'
        self.input_size = (200, 14)

        self.data = read_data(self.input_file)
        self.X, self.y = extract_target_variable(self.data, self.target_column)
        self.X_train, self.X_test, self.y_train, self.y_test = \
            split_train_test_data(self.X, self.y, SplittingParams())

    def test_read_data(self):
        self.assertEqual(self.data.shape, (200, 14))
        self.assertIn(self.target_column, self.data.columns)

    def test_extract_target_variable(self):
        self.assertIsInstance(self.X, pd.DataFrame)
        self.assertIsInstance(self.y, np.ndarray)
        self.assertEqual(self.X.shape, (200, 13))
        self.assertEqual(self.y.shape, (200, ))

    def test_split_train_test_data(self):
        self.X, self.y = extract_target_variable(self.data, self.target_column)

        self.assertIsInstance(self.X_train, pd.DataFrame)
        self.assertIsInstance(self.y_train, np.ndarray)
        self.assertIsInstance(self.X_test, pd.DataFrame)
        self.assertIsInstance(self.y_test, np.ndarray)

        self.assertEqual(self.X_train.shape, (160, 13))
        self.assertEqual(self.y_train.shape, (160, ))
        self.assertEqual(self.X_test.shape, (40, 13))
        self.assertEqual(self.y_test.shape, (40, ))


if __name__ == '__main__':
    unittest.main()
