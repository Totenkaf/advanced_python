"""Copyright 2022 by Artem Ustsov"""

import pandas as pd
from pandas_profiling import ProfileReport
import os
import sys
import click
import logging
from ml_project.entities.train_pipeline_params import (
    read_training_pipeline_params,
)


def make_eda_report(config_path: str):
    training_pipeline_params = read_training_pipeline_params(config_path)
    df = pd.read_csv(training_pipeline_params.input_data_path)
    profile = ProfileReport(df, title="EDA Report")
    profile.to_file(
        os.path.join(training_pipeline_params.output_params.eda, "EDA.html")
    )


@click.command(name="make_eda")
@click.argument("config_path")
def make_eda_command(config_path: str):
    make_eda_report(config_path)
    return


if __name__ == "__main__":
    if not os.path.isdir("logs"):
        os.mkdir("logs")

    FORMAT_LOG = "%(asctime)s: %(message)s"
    file_log = logging.FileHandler("logs/make_eda.log")
    console_out = logging.StreamHandler(sys.stdout)

    logging.basicConfig(
        handlers=(file_log, console_out),
        format=FORMAT_LOG,
        level=logging.INFO,
        datefmt="%H:%M:%S",
    )
    logger = logging.getLogger(__name__)

    logger.info("=====PROGRAM START======")
    make_eda_command()
    logger.info("=====PROGRAM STOP======")
