"""Copyright 2022 by Artem Ustsov"""

from typing import Any, NoReturn, Tuple

import pandas as pd
import boto3
from sklearn.model_selection import train_test_split

from ml_project.entities.split_params import SplittingParams
import logging


def download_data_from_s3(
    s3_bucket: str,
    s3_path: str,
    s3_endpoint_url: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    output_path: str,
) -> NoReturn:
    logger = logging.getLogger(__name__)
    logger.info(f"download from {s3_path}")
    session = boto3.session.Session()
    s3_client = session.client(
        service_name="s3",
        region_name="ru-msk",
        endpoint_url=s3_endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    with open(output_path, "wb") as f:
        s3_client.download_fileobj(s3_bucket, s3_path, f)


def read_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)
    return data


def write_data(path: str, data: Any) -> NoReturn:
    if isinstance(data, pd.DataFrame):
        data.to_csv(path, index=False)
    pd.DataFrame(data).to_csv(path, index=False)


def split_train_val_data(
    data: pd.DataFrame, params: SplittingParams
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    train_data, val_data = train_test_split(
        data, test_size=params.val_size, random_state=params.random_state
    )
    return train_data, val_data
