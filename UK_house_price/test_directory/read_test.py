from pathlib import Path
import pandas as pd
import pickle
import os, sys
import boto3
from datetime import datetime


def input_data(region: str):
    S3_ENDPOINT_URL = os.getenv('ENDPOINT_URL',"http://localhost:4566")
    
    options = {
        'client_kwargs': {
            'endpoint_url': S3_ENDPOINT_URL
            }
        }
    file_loaded = f's3://UK-house-price-localstack/{region}_predictions.parquet'
    df = pd.read_parquet(file_loaded, storage_options=options)

    return df


if __name__ == "__main__":
    region = int(sys.argv[1])  # Oxford
    df = input_data(region)

    print(df.head())