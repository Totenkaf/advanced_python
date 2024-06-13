"""Copyright 2022 by Artem Ustsov"""

import os
import pickle

import pandas as pd
from fastapi import FastAPI
from fastapi_health import health

from schema import MedicalFeatures

app = FastAPI()
model = None


@app.on_event('startup')
def load_model():
    """Predefines. Upload the model from S3"""

    path_to_model = os.getenv('PATH_TO_MODEL')
    with open(path_to_model, 'rb') as f:
        global model
        model = pickle.load(f)


@app.get('/')
def home():
    """Home page"""
    return {"key": "Hello"}


@app.post('/predict')
async def predict(data: MedicalFeatures):
    """Get the data from request.
    Make prediction and send response to user
    """

    data_df = pd.DataFrame([data.dict()])
    y = model.predict(data_df)
    print(y)

    return {'condition': 'disease' if y[0] == 1 else 'no disease'}


def check_ready():
    """General model check"""
    return model is not None


async def success_handler(**kwargs):
    """Success health check"""
    return 'Model is ready'


async def failure_handler(**kwargs):
    """Failure health check"""
    return 'Model is not ready'

app.add_api_route('/health', health([check_ready],
                  success_handler=success_handler,
                  failure_handler=failure_handler))
