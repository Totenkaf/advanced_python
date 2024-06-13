"""Copyright 2022 by Artem Ustsov"""

from dataclasses import dataclass, field


@dataclass()
class MlFlowParams:
    use_mlflow: bool = False
    mlflow_uri: str = field(default="http://5.188.141.0:8000")
    mlflow_experiment: str = field(default="demo")
