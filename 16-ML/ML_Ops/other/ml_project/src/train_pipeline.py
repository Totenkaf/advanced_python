import json
import logging

import hydra
import mlflow
import numpy as np
import pandas as pd
from hydra.core.config_store import ConfigStore
from hydra.utils import instantiate

from data import extract_target_variable, read_data, split_train_test_data
from entities import TrainConfig
from features import create_transformer, process_features
from logger import LoggerFormating
from models import evaluate_model, predict_model, save_model, train_model

logger = logging.getLogger('Training Pipeline')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(LoggerFormating())
logger.addHandler(handler)
logger.propagate = False

cs = ConfigStore.instance()
cs.store(name='train', node=TrainConfig)


@hydra.main(version_base=None, config_path='../configs', config_name='config')
def run_train_pipeline(params: TrainConfig):
    params = instantiate(params, _convert_='partial')
    logger.info(f'Starting train pipeline with params {params}')
    data = read_data(params.path_to_input_data)
    logger.info(f'Successfully read DataFrame, shape is {data.shape}')

    X, y = extract_target_variable(data, params.feature_params.target_column)

    X_train, X_test, y_train, y_test = split_train_test_data(X, y, params.splitting_params)
    logger.info(f'Test samples: {X_train.shape[0]}, Test samples: {X_test.shape[0]}')
    X_test.to_csv(params.path_to_test_data)  # to use in prediction pipeline
    logger.info(f'Saved unlabeled test data to {params.path_to_test_data}')

    logger.info('Transforming features... ')
    transformer = create_transformer(params.feature_params, params.model.feature_processing_params)
    transformer.fit(X_train)
    X_train = process_features(transformer, X_train)
    df_train_processed = np.concatenate([X_train, y_train[..., np.newaxis]], axis=-1)
    pd.DataFrame(df_train_processed).to_csv(params.model.path_to_processed_data, index=False)
    logger.info(f'Saved features to {params.model.path_to_processed_data}')
    save_model(transformer, params.model.path_to_transformer)
    logger.info(f'Saved transform to {params.model.path_to_transformer}')

    mlflow.set_tracking_uri("http://localhost:5000")
    with mlflow.start_run(run_name=params.mlflow_run_name):
        logger.info(f'Start training {params.model.train_params.model_type}...')
        if params.model.train_params.grid_search:
            model, best_params, val_metrics = train_model(X_train, y_train, params.model.train_params)
            logger.info(f'Best HyperParams for {params.model.train_params.model_type} are {best_params}')
            for hp in best_params:
                mlflow.log_param(hp, best_params[hp])
            logger.info(f'Validation matrics: {val_metrics}')
            for metric in val_metrics:
                mlflow.log_metric(metric, val_metrics[metric])
        else:
            model = train_model(X_train, y_train, params.model.train_params)
        logger.info(f'End training {params.model.train_params.model_type}')

        logger.info('Calculating metrics...')
        y_pred = predict_model(model, process_features(transformer, X_test))
        metrics = evaluate_model(y_pred, y_test)
        for metric in metrics:
            mlflow.log_metric(metric, metrics[metric])
        logger.info(f'Metrics on test data {metrics}')
        with open(params.model.path_to_model_metric, 'w') as metric_file:
            if params.model.train_params.grid_search:
                json.dump({**val_metrics, **metrics}, metric_file)
            else:
                json.dump(metrics, metric_file)

        logger.info(f'Saving model to {params.model.path_to_output_model} ...')
        save_model(model, params.model.path_to_output_model)
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="classification_model",
            registered_model_name=params.model.train_params.model_type)
        logger.info('Saved model')

        logger.info('End training')


if __name__ == '__main__':
    run_train_pipeline()
