"""Copyright 2022 by Artem Ustsov"""

import json
import logging
import os
import pandas as pd

import requests


if __name__ == "__main__":
    if not os.path.isdir("logs"):
        os.mkdir("logs")

    FORMAT_LOG = "%(asctime)s: %(message)s"
    file_log = logging.FileHandler("logs/fetcher.log")
    console_out = logging.StreamHandler()

    logging.basicConfig(
        handlers=(file_log, console_out),
        format=FORMAT_LOG,
        level=logging.INFO,
        datefmt="%H:%M:%S",
    )
    logger = logging.getLogger('Requests')

    data = pd.read_csv('requests/test_diseases.csv').drop('condition', axis=1)
    data_requests = data.to_dict(orient='records')

    for request in data_requests:
        response = requests.post(
            'http://127.0.0.1:8000/predict',
            json.dumps(request)
        )
        logger.info('Response:')
        logger.info(f'Status Code: {response.status_code}')
        logger.info(f'Message: {response.json()}')
