"""Copyright 2022 by Artem Ustsov"""

import pandas as pd
from sklearn.linear_model import LogisticRegressionCV
from sklearn.pipeline import Pipeline
import sklearn.model_selection as selection
from sklearn.compose import ColumnTransformer

from ml_project.entities.train_params import TrainingParams

SklearnClassifierModel = LogisticRegressionCV


def train_model(
    features: pd.DataFrame, target: pd.Series, train_params: TrainingParams
) -> SklearnClassifierModel:
    if train_params.model_type == "LogisticRegressionCV":
        cv = None
        if train_params.cross_val_strategy == "StratifiedKFold":
            cv = selection.StratifiedKFold(train_params.n_split)
        model = LogisticRegressionCV(
            penalty=train_params.penalty,
            cv=cv,
            max_iter=train_params.max_iter,
            tol=train_params.tol,
        )
    else:
        raise NotImplementedError()
    model.fit(features, target)
    return model


def create_inference_pipeline(
    model: SklearnClassifierModel, transformer: ColumnTransformer
) -> Pipeline:
    return Pipeline([("feature_part", transformer), ("model_part", model)])
