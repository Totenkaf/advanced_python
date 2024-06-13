import os
import pickle
import sys
import unittest

import numpy as np
from sklearn.exceptions import NotFittedError
from sklearn.neighbors import KNeighborsClassifier
from sklearn.utils.validation import check_is_fitted

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH, 'src'
)
sys.path.append(SOURCE_PATH)

from entities import TrainingParams
from models import evaluate_model, predict_model, save_model, train_model
from tests.features_tests import TestFeaturesModule


class TestFitPredictModule(TestFeaturesModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        tp = TrainingParams()
        self.model, self.best_params, self.best_score = \
            train_model(self.X_train, self.y_train, tp)

        self.y_pred = predict_model(self.model, self.X_test)

    def test_train_model(self):
        try:
            check_is_fitted(self.model)
        except NotFittedError:
            self.fail('Model did not fit')
        self.assertIsInstance(self.best_params, dict)
        self.assertGreaterEqual(self.best_score['val_recall'], 0)

    def test_save_model(self):
        pth = 'model.pkl'
        save_model(self.model, pth)
        self.assertTrue(os.path.exists(pth))
        with open(pth, 'rb') as f:
            model = pickle.load(f)
        self.assertIsInstance(model, KNeighborsClassifier)
        os.remove(pth)

    def test_predict_model(self):
        self.assertIsInstance(self.y_pred, np.ndarray)
        self.assertEqual(self.y_pred.shape, (40,))
        self.assertEqual(list(np.unique(self.y_pred)), [0, 1])

    def test_evaluate_model(self):
        metrics = evaluate_model(self.y_pred, self.y_test)
        self.assertIsInstance(metrics, dict)
        self.assertGreaterEqual(metrics['recall'], 0)

    def test_create_transformer(self):
        pass

    def test_process_features(self):
        pass


if __name__ == '__main__':
    unittest.main()
