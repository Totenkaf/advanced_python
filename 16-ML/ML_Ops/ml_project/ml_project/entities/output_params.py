"""Copyright 2022 by Artem Ustsov"""

from dataclasses import dataclass


@dataclass()
class OutputParams:
    clean_input: str
    train: str
    train_processed: str
    test: str
    target_train: str
    target_test: str
    eda: str
    visuals: str
    model: str
    metric: str
