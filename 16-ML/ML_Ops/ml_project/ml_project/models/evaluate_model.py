"""Copyright 2022 by Artem Ustsov"""
import pandas as pd
from sklearn.metrics import f1_score
from typing import Dict
import numpy as np


def evaluate_model(
    predicts: np.array, target: pd.DataFrame, use_log_trick: bool = False
) -> Dict[str, float]:
    if use_log_trick:
        target = np.exp(target)
    return {
        "f1_score": f1_score(target, predicts),
    }
