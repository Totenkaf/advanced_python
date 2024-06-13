import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from entities.feature_params import FeatureParams, FeatureProcessingParams


def create_categorical_pipeline(to_process=True) -> Pipeline:
    if to_process:
        return Pipeline([('impute', SimpleImputer(strategy='most_frequent')),
                         ('ohe', OneHotEncoder())])
    else:
        return Pipeline([('impute', SimpleImputer(strategy='most_frequent'))])


def create_numerical_pipeline(to_process=True) -> Pipeline:
    if to_process:
        return Pipeline([('impute', SimpleImputer(strategy='mean')),
                         ('scaler', StandardScaler())])
    else:
        return Pipeline([('impute', SimpleImputer(strategy='mean'))])


def process_features(transformer: ColumnTransformer, data: pd.DataFrame) -> np.ndarray:
    return transformer.transform(data)


def create_transformer(params: FeatureParams,
                       process_params: FeatureProcessingParams) -> ColumnTransformer:
    transformer = ColumnTransformer(
        [
            (
                'categorical_pipeline',
                create_categorical_pipeline(process_params.process_categorical),
                params.categorical,
            ),
            (
                'numerical_pipeline',
                create_numerical_pipeline(process_params.process_numerical),
                params.numerical,
            ),
        ]
    )
    return transformer
