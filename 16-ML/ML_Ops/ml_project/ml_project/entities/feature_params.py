"""Copyright 2022 by Artem Ustsov"""

from dataclasses import dataclass
from typing import Optional, List


@dataclass()
class FeatureParams:
    categorical_features: List[str]
    numerical_features: List[str]
    target_col: Optional[str]
