from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from entities import SplittingParams


def read_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)
    return data


def extract_target_variable(data: pd.DataFrame,
                            target_column_name: str
                            ) -> Tuple[pd.DataFrame, np.ndarray]:
    X = data.drop(target_column_name, axis=1)
    y = data[target_column_name].to_numpy()
    return X, y


def split_train_test_data(X: np.ndarray, y: np.ndarray, params: SplittingParams
                          ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=params.test_size, random_state=params.random_state
    )
    return X_train, X_test, y_train, y_test
