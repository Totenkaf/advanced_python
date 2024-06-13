"""Copyright 2022 by Artem Ustsov"""

import os
import sys
import click
import logging
from ml_project.entities.train_pipeline_params import (
    read_training_pipeline_params,
)
from ml_project.data.load_data import download_data_from_s3
from pathlib import Path


@click.command(name="download_data_from_s3")
@click.argument("config_path")
def download_data_from_s3_command(config_path: str):
    training_pipeline_params = read_training_pipeline_params(config_path)
    downloading_params = training_pipeline_params.downloading_params
    if downloading_params:
        os.makedirs(downloading_params.output_folder, exist_ok=True)
        logger.info(f"download data from {downloading_params.s3_bucket}")
        for path in downloading_params.paths:
            download_data_from_s3(
                s3_bucket=downloading_params.s3_bucket,
                s3_path=path,
                s3_endpoint_url=downloading_params.s3_endpoint_url,
                aws_access_key_id=downloading_params.aws_access_key_id,
                aws_secret_access_key=downloading_params.aws_secret_access_key,
                output_path=os.path.join(
                    downloading_params.output_folder, Path(path).name
                ),
            )


if __name__ == "__main__":
    if not os.path.isdir("logs"):
        os.mkdir("logs")

    FORMAT_LOG = "%(asctime)s: %(message)s"
    file_log = logging.FileHandler("logs/download_data_from_s3.log")
    console_out = logging.StreamHandler(sys.stdout)

    logging.basicConfig(
        handlers=(file_log, console_out),
        format=FORMAT_LOG,
        level=logging.INFO,
        datefmt="%H:%M:%S",
    )
    logger = logging.getLogger(__name__)

    logger.info("=====PROGRAM START======")
    download_data_from_s3_command()
    logger.info("=====PROGRAM STOP======")
