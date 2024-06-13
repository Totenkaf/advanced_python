"""Copyright 2022 by Artem Ustsov"""

import logging
import os
import sys
import click

from ml_project.data import read_data, write_data, split_train_val_data
from ml_project.entities.train_pipeline_params import (
    read_training_pipeline_params,
)
from ml_project.features import make_features
from ml_project.features.build_features import (
    extract_target,
    build_transformer,
    process_raw_data,
)
from ml_project.models.process_model import serialize_model
from ml_project.models.fit_model import train_model


import mlflow

from ml_project.models.fit_model import create_inference_pipeline


def fit_pipeline(config_path: str):
    training_pipeline_params = read_training_pipeline_params(config_path)

    logger.info(
        f"is mlflow available="
        f"{training_pipeline_params.mlflow_params.use_mlflow}"
    )
    if training_pipeline_params.mlflow_params.use_mlflow:
        logger.info("set environment variables")
        os.environ[
            "MLFLOW_S3_ENDPOINT_URL"
        ] = training_pipeline_params.downloading_params.s3_endpoint_url
        os.environ[
            "MLFLOW_TRACKING_URI"
        ] = training_pipeline_params.mlflow_params.mlflow_uri

        logger.info("check the mlflow experiment")
        if not mlflow.get_experiment_by_name(
            training_pipeline_params.mlflow_params.mlflow_experiment
        ):
            logger.info(
                f"create new experiment with name "
                f"{training_pipeline_params.mlflow_params.mlflow_experiment}"
            )
            mlflow.create_experiment(
                training_pipeline_params.mlflow_params.mlflow_experiment
            )
        logger.info(
            f"set experiment with name "
            f"{training_pipeline_params.mlflow_params.mlflow_experiment}"
        )
        mlflow.set_experiment(
            training_pipeline_params.mlflow_params.mlflow_experiment
        )

        logger.info("ml_flow registry enable")
        with mlflow.start_run(
            run_name=training_pipeline_params.mlflow_params.mlflow_experiment
        ):
            mlflow.log_artifact(config_path)
            model_path = run_fit_pipeline(training_pipeline_params)
            mlflow.log_artifact(model_path)
    else:
        return run_fit_pipeline(training_pipeline_params)


def run_fit_pipeline(training_pipeline_params):
    logger.info(f"start train pipeline with params:")
    for field, value in training_pipeline_params.__dict__.items():
        logger.info(f"{field}={value}")

    data = read_data(training_pipeline_params.input_data_path)
    logger.info(f"data.shape is {data.shape}")

    readable_data = process_raw_data(
        data, training_pipeline_params.feature_params
    )
    readable_data.to_csv(
        training_pipeline_params.output_params.clean_input, index_label=False
    )

    train_df, val_df = split_train_val_data(
        data, training_pipeline_params.splitting_params
    )

    train_target = extract_target(
        train_df, training_pipeline_params.feature_params
    )
    write_data(
        training_pipeline_params.output_params.target_train,
        train_target,
    )

    val_target = extract_target(
        val_df, training_pipeline_params.feature_params
    )
    write_data(
        training_pipeline_params.output_params.target_test,
        val_target,
    )

    train_df = train_df.drop(
        training_pipeline_params.feature_params.target_col, axis=1
    )
    logger.info(
        f"write train_df into "
        f"{training_pipeline_params.output_params.train}"
    )
    write_data(
        training_pipeline_params.output_params.train,
        train_df,
    )

    val_df = val_df.drop(
        training_pipeline_params.feature_params.target_col, axis=1
    )
    logger.info(
        f"Write val_df into " f"{training_pipeline_params.output_params.test}"
    )
    write_data(
        training_pipeline_params.output_params.test,
        val_df,
    )

    logger.info(f"train_df.shape is {train_df.shape}")
    logger.info(f"val_df.shape is {val_df.shape}")

    transformer = build_transformer(training_pipeline_params.feature_params)
    transformer.fit(train_df)

    train_features = make_features(transformer, train_df)
    logger.info(
        f"write train_features into "
        f"{training_pipeline_params.output_params.train_processed}"
    )
    write_data(
        training_pipeline_params.output_params.train_processed,
        train_features,
    )
    logger.info("write train data")

    logger.info(f"train_features.shape is {train_features.shape}")
    model = train_model(
        train_features,
        train_target,
        training_pipeline_params.train_params,
    )

    inference_pipeline = create_inference_pipeline(model, transformer)

    logger.info("Serialize model")
    path_to_model = serialize_model(
        inference_pipeline, training_pipeline_params.output_params.model
    )
    logger.info(
        f"Link to mlflow server: "
        f"{training_pipeline_params.__dict__['mlflow_params'].mlflow_uri}"
    )
    return path_to_model


@click.command(name="fit_pipeline")
@click.argument("config_path")
def fit_pipeline_command(config_path: str):
    fit_pipeline(config_path)
    return


if __name__ == "__main__":
    if not os.path.isdir("logs"):
        os.mkdir("logs")

    FORMAT_LOG = "%(asctime)s: %(message)s"
    file_log = logging.FileHandler("logs/fit_pipeline.log")
    console_out = logging.StreamHandler(sys.stdout)

    logging.basicConfig(
        handlers=(file_log, console_out),
        format=FORMAT_LOG,
        level=logging.INFO,
        datefmt="%H:%M:%S",
    )
    logger = logging.getLogger(__name__)

    logger.info("=====PROGRAM START======")
    fit_pipeline_command()
    logger.info("=====PROGRAM STOP======")
