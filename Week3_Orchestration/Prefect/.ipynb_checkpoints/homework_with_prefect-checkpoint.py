import pandas as pd

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import os
from pathlib import Path

import mlflow
import prefect
from prefect import task, flow, get_run_logger
from prefect.task_runners import SequentialTaskRunner

@task(name="get-path-task")
def get_paths(date):
    PATH_CUR = os.getcwd()
    p = Path(PATH_CUR)
    train_path = os.path.join(p.parents[1], 'data/fhv_tripdata_2021-06.parquet')
    val_path = os.path.join(p.parents[1], 'data/fhv_tripdata_2021-07.parquet')
    return train_path, val_path

@task(name="read-parquet-task")
def read_data(path):
    logger = get_run_logger()
    logger.info("INFO reading parquet files.")
    df = pd.read_parquet(path)
    return df

@task(name="task-prepare-features")
def prepare_features(df, categorical, train=True):
    logger = get_run_logger()
    logger.info("INFO preparing categorical features & calculating average duration.")
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    mean_duration = df.duration.mean()
    if train:
        logger.info(f"INFO The mean duration of training is {mean_duration}")
    else:
        logger.info(f"INFO The mean duration of validation is {mean_duration}")
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df

@task(name="train-model-task")
def train_model(df, categorical):
    logger = get_run_logger()
    logger.info("INFO training model.")
    train_dicts = df[categorical].to_dict(orient='records')
    dv = DictVectorizer()
    logger.warning("WARNING DictVectorizer")
    X_train = dv.fit_transform(train_dicts) 
    y_train = df.duration.values

    logger.info(f"INFO The shape of X_train is {X_train.shape}")
    logger.info(f"INFO The DictVectorizer has {len(dv.feature_names_)} features")

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_train)
    mse = mean_squared_error(y_train, y_pred, squared=False)
    logger.info(f"INFO The MSE of training is: {mse}")
    return lr, dv

@task(name="run-model-task")
def run_model(df, categorical, dv, lr):
    logger = get_run_logger()
    logger.info("INFO running model.")
    val_dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(val_dicts) 
    y_pred = lr.predict(X_val)
    y_val = df.duration.values

    mse = mean_squared_error(y_val, y_pred, squared=False)
    logger.info(f"The MSE of validation is: {mse}")
    return

@flow(name="log-example-flow")
def main(date=None):
    # mlflow.set_tracking_uri("sqlite:///mlflow_prefect.db")
    # mlflow.set_experiment("prefect-experiment")
    train_path, val_path = get_paths(date).result()
    categorical = ['PUlocationID', 'DOlocationID']

    df_train = read_data(train_path)
    df_train_processed = prepare_features(df_train, categorical)

    df_val = read_data(val_path)
    df_val_processed = prepare_features(df_val, categorical, False)

    # train the model
    lr, dv = train_model(df_train_processed, categorical).result()
    run_model(df_val_processed, categorical, dv, lr)

if __name__ == '__main__':
    main("2021-08-15")
