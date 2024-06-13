import logging
import os
import pickle
import shutil
import sys
import unittest

from hydra import compose, initialize
from hydra.errors import InstantiationException
from hydra.utils import instantiate
from sklearn.compose import ColumnTransformer
from sklearn.neighbors import KNeighborsClassifier

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH, 'src'
)
sys.path.append(SOURCE_PATH)

from src import run_predict_pipeline, run_train_pipeline

logging.disable(logging.CRITICAL)


class TestTrainPredictPipeline(unittest.TestCase):
    def test_1_run_train_pipeline(self):
        os.makedirs('tests/models', exist_ok=True)

        with initialize(version_base=None, config_path='test_configs'):
            params = compose(config_name="test_config")
        run_train_pipeline(params)

        self.assertTrue(os.path.exists(params.path_to_test_data))
        self.assertTrue(os.path.exists(params.model.path_to_output_model))
        self.assertTrue(os.path.exists(params.model.path_to_model_metric))
        self.assertTrue(os.path.exists(params.model.path_to_processed_data))
        self.assertTrue(os.path.exists(params.model.path_to_transformer))

        with open(params.model.path_to_output_model, 'rb') as file:
            model = pickle.load(file)
        self.assertIsInstance(model, KNeighborsClassifier)

        with open(params.model.path_to_transformer, 'rb') as f:
            model = pickle.load(f)
        self.assertIsInstance(model, ColumnTransformer)

    def test_2_broken_config(self):
        with initialize(version_base=None, config_path='test_configs'):
            params = compose(config_name="broken_config")
        with self.assertRaises(InstantiationException):
            run_train_pipeline(params)

    def test_3_run_prediction_pipeline(self):
        with initialize(version_base=None, config_path='test_configs'):
            params = compose(config_name="test_config")
        params = instantiate(params, _convert_='partial')
        run_predict_pipeline.callback(path_to_model=params.model.path_to_output_model,
                                      path_to_transformer=params.model.path_to_transformer,
                                      path_to_csv=params.path_to_test_data,
                                      path_to_prediction='tests/models/prediction.csv')
        self.assertTrue(os.path.exists('tests/models/prediction.csv'))
        shutil.rmtree('tests/models')


if __name__ == '__main__':
    unittest.main()
