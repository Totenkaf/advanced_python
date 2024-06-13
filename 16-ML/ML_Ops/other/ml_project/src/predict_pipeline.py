import logging
import pickle

import click
import pandas as pd

from data import read_data
from features import process_features
from logger import LoggerFormating
from models import predict_model

logger = logging.getLogger('Prediction Pipeline')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(LoggerFormating())
logger.addHandler(handler)
logger.propagate = False


@click.command()
@click.option('--path_to_model', type=click.Path(exists=True),
              default='models/model_knn.pkl',
              help='Path to model to make prediciion with')
@click.option('--path_to_transformer', type=click.Path(exists=True),
              default='models/transformers/transformer_knn.pkl',
              help='Path to transformation to be applied to the data')
@click.option('--path_to_csv', type=click.Path(exists=True),
              default='data/test/heart_cleveland_upload_test_unlabeled.csv',
              help='Path to unlabeled data')
@click.option('--path_to_prediction', type=click.Path(exists=False),
              default='models/predictions/pred_knn.csv',
              help='Path to save prediction')
def run_predict_pipeline(path_to_model: str, path_to_transformer: str,
                         path_to_csv: str, path_to_prediction: str):
    logger.info('Starting predict pipeline with params ...')
    data = read_data(path_to_csv)
    logger.info(f'Successfully read DataFrame, shape is {data.shape}')

    logger.info('Transforming features... ')
    with open(path_to_transformer, 'rb') as f:
        transformer = pickle.load(f)
    logger.info('Successfully read transformer')
    X = process_features(transformer, data)
    logger.info('Transformed features')

    logger.info('Making prediction... ')
    with open(path_to_model, 'rb') as f:
        model = pickle.load(f)
    logger.info('Successfully read model')
    y = predict_model(model, X)
    logger.info(f'Made prediction using {type(model).__name__}')

    pd.DataFrame(y).to_csv(path_to_prediction, index=False)
    logger.info(f'Saved model to {path_to_prediction}')
    logger.info('End prediction')


if __name__ == '__main__':
    run_predict_pipeline()
