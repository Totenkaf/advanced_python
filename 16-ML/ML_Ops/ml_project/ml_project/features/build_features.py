"""Copyright 2022 by Artem Ustsov"""

import logging
from typing import List, NoReturn
import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from sklearn.impute import SimpleImputer
from sklearn.pipeline import FeatureUnion, Pipeline

from ml_project.entities.feature_params import FeatureParams


class FeatureSelector(BaseEstimator, TransformerMixin):
    def __init__(self, feature_names: List[str]) -> NoReturn:
        self._feature_names = feature_names

    def fit(self, x_data: pd.DataFrame, y: pd.Series = None) -> object:
        return self

    def transform(
        self, x_data: pd.DataFrame, y: pd.Series = None
    ) -> pd.DataFrame:
        return x_data[self._feature_names]


class DataframeTransformer(BaseEstimator, TransformerMixin):
    def fit(self, x_data: pd.DataFrame, y: pd.Series = None) -> object:
        return self

    def transform(
        self, x_data: pd.DataFrame, y: pd.Series = None
    ) -> pd.DataFrame:
        x_data.columns = [
            "age",
            "sex",
            "chest_pain_type",
            "resting_blood_pressure",
            "cholesterol",
            "fasting_blood_sugar",
            "rest_ecg",
            "max_heart_rate_achieved",
            "exercise_induced_angina",
            "st_depression",
            "st_slope",
            "num_major_vessels",
            "thalassemia",
            "condition",
        ]

        return x_data


class TargetTransformer(BaseEstimator, TransformerMixin):
    def fit(self, x_data: pd.DataFrame, y: pd.Series = None) -> object:
        return self

    @staticmethod
    def process_condition(obj) -> NoReturn:
        if obj == 0:
            return "no disease"
        if obj == 1:
            return "disease"

    def transform(
        self, x_data: pd.DataFrame, y: pd.Series = None
    ) -> pd.DataFrame:
        x_data.loc[:, x_data.columns[0]] = x_data[x_data.columns[0]].apply(
            self.process_condition
        )
        return x_data


class CategoricalTransformer(BaseEstimator, TransformerMixin):
    @staticmethod
    def process_sex(obj):
        if obj == 0:
            return "female"
        if obj == 1:
            return "male"

    @staticmethod
    def process_chest_pain_type(obj) -> NoReturn:
        if obj == 0:
            return "typical_angina"
        if obj == 1:
            return "atypical_angina"
        if obj == 2:
            return "non_anginal_pain"
        if obj == 3:
            return "asymptomatic"

    @staticmethod
    def process_rest_ecg(obj) -> NoReturn:
        if obj == 0:
            return "normal"
        if obj == 1:
            return "ST-T_wave_abnormality"
        if obj == 2:
            return "left_ventricular_hypertrophy"

    @staticmethod
    def process_fasting_blood_sugar(obj) -> NoReturn:
        if obj == 0:
            return "less_than_120mg/ml"
        if obj == 1:
            return "greater_than_120mg/ml"

    @staticmethod
    def process_exercise_induced_angina(obj) -> NoReturn:
        if obj == 0:
            return "no"
        if obj == 1:
            return "yes"

    @staticmethod
    def process_st_slope(obj) -> NoReturn:
        if obj == 0:
            return "upsloping"
        if obj == 1:
            return "flat"
        if obj == 2:
            return "downsloping"

    @staticmethod
    def process_thalassemia(obj) -> NoReturn:
        if obj == 0:
            return "fixed_defect"
        if obj == 1:
            return "normal"
        if obj == 2:
            return "reversable_defect"

    def fit(self, x_data: pd.DataFrame, y: pd.Series = None) -> object:
        return self

    def transform(
        self, x_data: pd.DataFrame, y: pd.Series = None
    ) -> pd.DataFrame:
        for cat_feature in x_data.columns:
            exec(
                f"x_data.loc[:, '{cat_feature}'] = x_data['{cat_feature}'].apply(self.process_{cat_feature})"
            )
        return x_data


class NumericalTransformer(BaseEstimator, TransformerMixin):
    def fit(self, x_data: pd.DataFrame, y: pd.Series = None) -> object:
        return self

    def transform(
        self, x_data: pd.DataFrame, y: pd.Series = None
    ) -> pd.DataFrame:
        x_data = x_data.replace([np.inf, -np.inf], np.nan)
        return x_data


def build_rename_raw_data_columns_pipeline() -> Pipeline:
    rename_raw_data_pipeline = Pipeline(
        steps=[
            ("data_renames", DataframeTransformer()),
        ]
    )
    return rename_raw_data_pipeline


def build_features_values_rename_pipeline(params: FeatureParams) -> Pipeline:
    categorical_pipeline = Pipeline(
        steps=[
            ("cat_selector", FeatureSelector(params.categorical_features)),
            ("cat_transformer", CategoricalTransformer()),
        ]
    )

    numerical_pipeline = Pipeline(
        steps=[
            ("num_selector", FeatureSelector(params.numerical_features)),
            ("num_transformer", NumericalTransformer()),
        ]
    )

    target_pipeline = Pipeline(
        steps=[
            ("target_selector", FeatureSelector([params.target_col])),
            ("target_transformer", TargetTransformer()),
        ]
    )

    full_pipeline = Pipeline(
        [
            (
                "full_pipline",
                FeatureUnion(
                    [
                        ("categorical_pipeline", categorical_pipeline),
                        ("numerical_pipeline", numerical_pipeline),
                        ("target_pipeline", target_pipeline),
                    ]
                ),
            )
        ]
    )

    return full_pipeline


def build_raw_data_pipeline(params: FeatureParams) -> Pipeline:
    raw_headers_pipeline = Pipeline(
        steps=[
            (
                "raw_data_columns_rename",
                build_rename_raw_data_columns_pipeline(),
            ),
            ("feature_rename", build_features_values_rename_pipeline(params)),
        ]
    )
    return raw_headers_pipeline


def process_raw_data(
    raw_data_df: pd.DataFrame, params: FeatureParams
) -> pd.DataFrame:
    raw_data_pipeline = build_raw_data_pipeline(params)
    return pd.DataFrame(
        raw_data_pipeline.fit_transform(raw_data_df),
        columns=params.categorical_features
        + params.numerical_features
        + [params.target_col],
    )


def build_categorical_pipeline() -> Pipeline:
    categorical_pipeline = Pipeline(
        steps=[
            (
                "impute",
                SimpleImputer(
                    missing_values=np.nan, strategy="most_frequent"
                ),
            ),
            ("one_hot_encoder", OneHotEncoder(sparse=False)),
        ]
    )
    return categorical_pipeline


def build_numerical_pipeline() -> Pipeline:
    numerical_pipeline = Pipeline(
        steps=[
            ("impute", SimpleImputer(missing_values=np.nan, strategy="mean")),
            ("std_scaler", StandardScaler()),
        ]
    )
    return numerical_pipeline


def make_features(
    transformer: ColumnTransformer, df: pd.DataFrame
) -> pd.DataFrame:
    logger = logging.getLogger(__name__)
    logger.info("Making features")
    return transformer.transform(df)


def build_transformer(params: FeatureParams) -> ColumnTransformer:
    transformer = ColumnTransformer(
        [
            (
                "categorical_pipeline",
                build_categorical_pipeline(),
                params.categorical_features,
            ),
            (
                "numerical_pipeline",
                build_numerical_pipeline(),
                params.numerical_features,
            ),
        ]
    )
    return transformer


def extract_target(df: pd.DataFrame, params: FeatureParams) -> pd.Series:
    target = df[params.target_col]
    return target
