"""Copyright 2022 by Artem Ustsov"""

import json
import os
import sys
import click

from ml_project.data import read_data
from ml_project.vizualisation.vizualize import (
    plot_roc_curve,
    plot_confusion_matrix,
)
from ml_project.entities.train_pipeline_params import (
    read_training_pipeline_params,
)
from ml_project.models.predict_model import predict_model
from ml_project.models.evaluate_model import evaluate_model
from ml_project.models.process_model import deserialize_model

import mlflow
import logging


def predict_pipeline(config_path):
    predicting_pipeline_params = read_training_pipeline_params(config_path)

    logger.info(
        f"is mlflow available="
        f"{predicting_pipeline_params.mlflow_params.use_mlflow}"
    )
    if predicting_pipeline_params.mlflow_params.use_mlflow:
        logger.info("set environment variables")
        os.environ[
            "MLFLOW_S3_ENDPOINT_URL"
        ] = predicting_pipeline_params.downloading_params.s3_endpoint_url
        os.environ[
            "MLFLOW_TRACKING_URI"
        ] = predicting_pipeline_params.mlflow_params.mlflow_uri

        logger.info("check the mlflow experiment")
        if not mlflow.get_experiment_by_name(
            predicting_pipeline_params.mlflow_params.mlflow_experiment
        ):
            logger.info(
                f"create new experiment with name "
                f"{predicting_pipeline_params.mlflow_params.mlflow_experiment}"
            )
            mlflow.create_experiment(
                predicting_pipeline_params.mlflow_params.mlflow_experiment
            )
        logger.info(
            f"set experiment with name "
            f"{predicting_pipeline_params.mlflow_params.mlflow_experiment}"
        )
        mlflow.set_experiment(
            predicting_pipeline_params.mlflow_params.mlflow_experiment
        )

        logger.info("ml_flow registry enable")
        with mlflow.start_run(
            run_name=predicting_pipeline_params.mlflow_params.mlflow_experiment
        ):
            mlflow.log_artifact(config_path)
            (
                metrics,
                roc_curve_path,
                confusion_matrix_path,
            ) = run_predict_pipeline(predicting_pipeline_params)
            mlflow.log_metrics(metrics)
            mlflow.log_artifact(roc_curve_path)
            mlflow.log_artifact(confusion_matrix_path)
            mlflow.log_artifact(
                predicting_pipeline_params.output_params.model
            )
    else:
        return run_predict_pipeline(predicting_pipeline_params)


def run_predict_pipeline(predicting_pipeline_params):
    inference_pipeline = deserialize_model(
        predicting_pipeline_params.output_params.model
    )

    val_df = read_data(predicting_pipeline_params.output_params.test)
    val_target = read_data(
        predicting_pipeline_params.output_params.target_test
    )

    logger.info("Make predictions")
    predicts = predict_model(
        inference_pipeline,
        val_df,
    )
    logger.info("Evaluate model")
    metrics = evaluate_model(
        predicts,
        val_target,
    )
    with open(
        predicting_pipeline_params.output_params.metric, "w"
    ) as metric_file:
        json.dump(metrics, metric_file)
    logger.info(f"Metrics is {metrics}")

    roc_curve_path = plot_roc_curve(
        val_target, predicts, predicting_pipeline_params.output_params.visuals
    )
    confusion_matrix_path = plot_confusion_matrix(
        val_target, predicts, predicting_pipeline_params.output_params.visuals
    )

    logger.info(
        f"Link to mlflow server: "
        f"{predicting_pipeline_params.__dict__['mlflow_params'].mlflow_uri}"
    )
    return metrics, roc_curve_path, confusion_matrix_path


@click.command(name="predict_pipeline")
@click.argument("config_path")
def predict_pipeline_command(config_path: str):
    predict_pipeline(config_path)
    return


if __name__ == "__main__":
    if not os.path.isdir("logs"):
        os.mkdir("logs")

    FORMAT_LOG = "%(asctime)s: %(message)s"
    file_log = logging.FileHandler("logs/predict_pipeline.log")
    console_out = logging.StreamHandler(sys.stdout)

    logging.basicConfig(
        handlers=(file_log, console_out),
        format=FORMAT_LOG,
        level=logging.INFO,
        datefmt="%H:%M:%S",
    )
    logger = logging.getLogger(__name__)

    logger.info("=====PROGRAM START======")
    predict_pipeline_command()
    logger.info("=====PROGRAM STOP======")
