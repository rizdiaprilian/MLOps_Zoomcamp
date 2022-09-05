from pathlib import Path
import pandas as pd
import pickle
import os, sys
import boto3
from datetime import datetime
from botocore.exceptions import ClientError


AWS_REGION = ''
ENDPOINT_URL = 'http://localhost:4566'
ACCESS_KEY = ""
SECRET_KEY = ""
S3_ENDPOINT_URL = os.getenv('ENDPOINT_URL',"http://localhost:4566")


def upload_file(file_name, bucket, object_name=None):
    """
    Upload a file to a S3 bucket.
    """
    s3_client = boto3.client("s3", region_name=AWS_REGION,
                         endpoint_url=S3_ENDPOINT_URL,
                         use_ssl=False,
                        aws_access_key_id=ACCESS_KEY,
                        aws_secret_access_key=SECRET_KEY)
    try:
        if object_name is None:
            object_name = os.path.basename(file_name)
        response = s3_client.upload_file(
            file_name, bucket, object_name)
    except ClientError:
        raise
    else:
        return response

def dt(hour, minute, second=0):
    return datetime(2021, 1, 1, hour, minute, second)


def input_data():
    S3_ENDPOINT_URL = os.getenv('ENDPOINT_URL',"http://localhost:4566")
    s3_client = boto3.client("s3", region_name=AWS_REGION,
                         endpoint_url=S3_ENDPOINT_URL,
                         use_ssl=False,
                        aws_access_key_id=ACCESS_KEY,
                        aws_secret_access_key=SECRET_KEY)
    options = {
        'client_kwargs': {
            'endpoint_url': S3_ENDPOINT_URL
            }
        }
    # df = pd.read_parquet('s3://mlopszoomcamp-bucket/taxi_type=fhv/year=2021/month=08/predictions.parquet')
    # file_loaded = f's3://nyc-duration/{year:04d}_{month:02d}_predictions.parquet'
    # df = pd.read_parquet(file_loaded, storage_options=options)

    data = [
            (None, None, dt(1, 2), dt(1, 10)),
            (1, 1, dt(1, 2), dt(1, 10)),
            (1, 1, dt(1, 2, 0), dt(1, 2, 50)),
            (1, 1, dt(1, 2, 0), dt(2, 2, 1)),        
        ]

    columns = ['PUlocationID', 'DOlocationID', 'pickup_datetime', 'dropOff_datetime']
    df = pd.DataFrame(data, columns=columns)

    output_file = '2021_01_predictions.parquet'
    df.to_parquet(
            output_file,
            engine='pyarrow',
            compression=None,
            index=False
        )

    object_name = f'2021_01_predictions.parquet'
    bucket = 'nyc-duration'
    s3 = upload_file(output_file, bucket, object_name)
    # return df


if __name__ == "__main__":
    # year = int(sys.argv[1])  # 2021
    # month = int(sys.argv[2])  # 10
    # df = input_data(year, month)
    df = input_data()

    # print(df.head())