import pickle
from typing import Dict, Tuple, Union

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier

from entities import TrainingParams

SklearnClassificationModel = Union[KNeighborsClassifier, LogisticRegression]


def train_model(X_train: np.ndarray, y_train: np.ndarray,
                train_params: TrainingParams
                ) -> Tuple[SklearnClassificationModel, ...]:
    if train_params.model_type == 'KNeighborsClassifier':
        model = KNeighborsClassifier()
        param_grid = {'n_neighbors': np.arange(1, 25),
                      'weights': ['uniform', 'distance'],
                      'metric': ['minkowski', 'manhattan']}
    elif train_params.model_type == 'LogisticRegression':
        model = LogisticRegression(random_state=train_params.random_state, solver='liblinear')
        param_grid = {'C': np.logspace(-3, 3, 10),
                      'penalty': ['l1', 'l2']}
    else:
        raise NotImplementedError()

    if train_params.grid_search:
        model_gscv = GridSearchCV(model, param_grid, scoring='recall', cv=5)
        model_gscv.fit(X_train, y_train)

        model = model_gscv.best_estimator_
        return model_gscv.best_estimator_, model_gscv.best_params_,  \
            {'val_recall': model_gscv.best_score_}
    else:
        model.fit(X_train, y_train)
        return model


def predict_model(model: SklearnClassificationModel, X: np.ndarray
                  ) -> np.ndarray:
    return model.predict(X)


def evaluate_model(y_pred: np.ndarray, y_target: np.ndarray
                   ) -> Dict[str, float]:
    return {'recall': recall_score(y_pred, y_target)}


def save_model(model: object, path_to_model: str):
    with open(path_to_model, 'wb') as f:
        pickle.dump(model, f)
