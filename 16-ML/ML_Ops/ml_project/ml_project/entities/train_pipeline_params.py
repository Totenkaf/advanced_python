"""Copyright 2022 by Artem Ustsov"""

from typing import Optional

from dataclasses import dataclass
from .output_params import OutputParams
from .download_params import DownloadParams
from .mlflow_params import MlFlowParams
from .split_params import SplittingParams
from .feature_params import FeatureParams
from .train_params import TrainingParams
from marshmallow_dataclass import class_schema
import yaml


@dataclass()
class TrainingPipelineParams:
    input_data_path: str
    splitting_params: SplittingParams
    feature_params: FeatureParams
    train_params: TrainingParams
    output_params: Optional[OutputParams]
    downloading_params: Optional[DownloadParams] = None
    mlflow_params: Optional[MlFlowParams] = None


TrainingPipelineParamsSchema = class_schema(TrainingPipelineParams)


def read_training_pipeline_params(path: str) -> TrainingPipelineParams:
    with open(path, "r") as input_stream:
        schema = TrainingPipelineParamsSchema()
        return schema.load(yaml.safe_load(input_stream))
