from pathlib import Path
import pandas as pd
import pickle
import os, sys
import boto3
from datetime import datetime


# AWS_REGION = 'eu-west-2'
# ENDPOINT_URL = 'http://localhost:4566'
# ACCESS_KEY = "AKIARBMT65NSOGGBYJF2"
# SECRET_KEY = "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"
# S3_ENDPOINT_URL = os.getenv('ENDPOINT_URL',"http://localhost:4566")



def input_data(year:int, month: int):
    S3_ENDPOINT_URL = os.getenv('ENDPOINT_URL',"http://localhost:4566")
    
    options = {
        'client_kwargs': {
            'endpoint_url': S3_ENDPOINT_URL
            }
        }
    file_loaded = f's3://nyc-duration/{year:04d}_{month:02d}_predictions.parquet'
    df = pd.read_parquet(file_loaded, storage_options=options)

    return df


if __name__ == "__main__":
    year = int(sys.argv[1])  # 2021
    month = int(sys.argv[2])  # 10
    df = input_data(year, month)

    print(df.head())