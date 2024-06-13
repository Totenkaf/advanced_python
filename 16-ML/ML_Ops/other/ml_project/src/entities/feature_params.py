from dataclasses import dataclass, field
from typing import List


@dataclass()
class FeatureParams:
    categorical: List[str]
    numerical: List[str]
    target_column: str


@dataclass
class FeatureProcessingParams:
    process_categorical: bool = field(default=True)
    process_numerical: bool = field(default=True)
