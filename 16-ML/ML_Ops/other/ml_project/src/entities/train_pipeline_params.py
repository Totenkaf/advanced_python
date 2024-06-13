from dataclasses import dataclass

from .feature_params import FeatureParams, FeatureProcessingParams
from .split_params import SplittingParams
from .train_params import TrainingParams


@dataclass
class ModelConfig:
    path_to_output_model: str
    path_to_model_metric: str

    path_to_processed_data: str
    path_to_transformer: str
    feature_processing_params: FeatureProcessingParams

    train_params: TrainingParams


@dataclass
class TrainConfig:
    model: ModelConfig

    path_to_input_data: str
    path_to_test_data: str

    splitting_params: SplittingParams
    feature_params: FeatureParams

    mlflow_run_name: str
