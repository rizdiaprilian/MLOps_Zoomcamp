#!/usr/bin/env python
# coding: utf-8

import os, sys
import pickle
import pandas as pd

import boto3
from botocore.exceptions import ClientError

s3_endpoint = os.getenv('S3_ENDPOINT_URL', "http://localhost:4566")
s3_client = boto3.client('s3', endpoint_url=s3_endpoint)

def upload_file(file_name, bucket, object_name=None):
    """
    Upload a file to a S3 bucket.
    """
    try:
        if object_name is None:
            object_name = os.path.basename(file_name)
        response = s3_client.upload_file(
            file_name, bucket, object_name)
    except ClientError:
        raise
    else:
        print(f"upload success.......")
        return response

def get_input_path(year, month):
    default_input_pattern = 'https://raw.githubusercontent.com/alexeygrigorev/datasets/master/nyc-tlc/fhv/fhv_tripdata_{year:04d}-{month:02d}.parquet'
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)
    return input_pattern.format(year=year, month=month)


def get_output_path(year, month):
    # default_output_pattern = 's3://nyc-duration/{year:04d}_{month:02d}_predictions.parquet'
    default_output_pattern = 's3://nyc-duration/{year:04d}_{month:02d}_predictions.parquet'
    # default_output_pattern = 's3://mlopszoomcamp-bucket/taxi_type=fhv/year={year:04d}/month={month:02d}/predictions.parquet'
    output_pattern = os.getenv('OUTPUT_FILE_PATTERN', default_output_pattern)
    return output_pattern.format(year=year, month=month)


def read_data(filename, categorical: list):
    df = pd.read_parquet(filename)
    df["duration"] = df.dropOff_datetime - df.pickup_datetime
    df["duration"] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    df[categorical] = df[categorical].fillna(-1).astype("int").astype("str")

    return df


def main(year: int, month: int):
    input_file = get_input_path(year, month)
    output_file = get_output_path(year, month)
    print(output_file)
    with open("model.bin", "rb") as f_in:
        dv, lr = pickle.load(f_in)

    categorical = ["PUlocationID", "DOlocationID"]

    df = read_data(input_file, categorical)
    df["ride_id"] = f"{year:04d}/{month:02d}_" + df.index.astype("str")

    dicts = df[categorical].to_dict(orient="records")
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)

    print("predicted mean duration:", y_pred.mean())

    df_result = pd.DataFrame()
    df_result["ride_id"] = df["ride_id"]
    df_result["predicted_duration"] = y_pred

    # df_result.to_parquet(output_file, engine="pyarrow", index=False)
    S3_ENDPOINT_URL = os.getenv('ENDPOINT_URL',"http://localhost:4566")
    options = {
        'client_kwargs': {
            'endpoint_url': S3_ENDPOINT_URL
            }
        }
    df_result.to_parquet(output_file, engine="pyarrow", storage_options=options)
    # object_name = f'{year:04d}_{month:02d}_predictions.parquet'
    # bucket = 'nyc-duration'
    # s3 = upload_file(output_file, bucket, object_name)


if __name__ == "__main__":
    year = int(sys.argv[1])  # 2021
    month = int(sys.argv[2])  # 01 to 12
    main(year, month)
