"""Copyright 2022 by Artem Ustsov"""

import pandas as pd
import numpy as np
from typing import Any


def predict_model(
    model: Any,
    features: pd.DataFrame,
) -> np.ndarray:
    predicts = model.predict(features)
    return predicts
