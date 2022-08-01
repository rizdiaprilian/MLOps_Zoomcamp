#!/usr/bin/env python
# coding: utf-8

import os, sys
import pickle
import pandas as pd


def read_data(filename, categorical: list, options_url: dict):
    df = pd.read_parquet(filename, storage_options=options_url)
    df["duration"] = df.dropOff_datetime - df.pickup_datetime
    df["duration"] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    df[categorical] = df[categorical].fillna(-1).astype("int").astype("str")

    return df

def save_data(df: pd.DataFrame, output_file, options_url: dict):
    df.to_parquet(
            output_file,
            engine='pyarrow',
            compression=None,
            index=False,
            storage_options=options_url
        )
    print(f"Saving data successfully completed....")

def main(year: int, month: int):

    # input_file = f"https://raw.githubusercontent.com/alexeygrigorev/datasets/master/nyc-tlc/fhv/fhv_tripdata_{year:04d}-{month:02d}.parquet"
    input_file = f's3://nyc-duration/{year:04d}_{month:02d}_predictions.parquet'
    # output_file = f"taxi_type=fhv_year={year:04d}_month={month:02d}.parquet"
    output_file = f's3://nyc-duration/{year:04d}_{month:02d}_predictions_updated.parquet'
    S3_ENDPOINT_URL = os.getenv('ENDPOINT_URL',"http://localhost:4566")
    options = {
        'client_kwargs': {
            'endpoint_url': S3_ENDPOINT_URL
            }
        }
    with open("model.bin", "rb") as f_in:
        dv, lr = pickle.load(f_in)

    categorical = ["PUlocationID", "DOlocationID"]

    df = read_data(input_file, categorical, options)
    df["ride_id"] = f"{year:04d}/{month:02d}_" + df.index.astype("str")

    dicts = df[categorical].to_dict(orient="records")
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)

    print("predicted mean duration:", y_pred.mean())
    print("predicted sum duration:", y_pred.sum())

    df_result = pd.DataFrame()
    df_result["ride_id"] = df["ride_id"]
    df_result["predicted_duration"] = y_pred

    # df_result.to_parquet(output_file, engine="pyarrow", index=False)
    save_data(df_result, output_file, options)

class ModelService:
    def __init__(self, model, model_version=None, callbacks=None):
        self.model = model
        self.model_version = model_version
        self.callbacks = callbacks or []

    def prepare_features(self, df):

        df['duration'] = df.dropOff_datetime - df.pickup_datetime
        df['duration'] = df.duration.dt.total_seconds() / 60

        df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
        categorical = ['PUlocationID', 'DOlocationID']
        df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
        return df

    def predict(self, features):
        pred = self.model.predict(features)
        return float(pred[0])

if __name__ == "__main__":
    year = int(sys.argv[1])  # 2021
    month = int(sys.argv[2])  # 01 to 12
    main(year, month)
