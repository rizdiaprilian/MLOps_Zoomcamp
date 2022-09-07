# pylint: disable=invalid-name,missing-function-docstring
# pylint: disable=missing-module-docstring,wrong-import-position

import logging
import os
import pickle
import sys
from time import sleep

import boto3
import numpy as np
import pandas as pd
from deepdiff import DeepDiff
from pandas import Timestamp

sys.path.append("../")

from create_bucket_localstack import read_localstack, upload_file
from tests.test_data import input_data

ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", "http://localhost:4566")
AWS_REGION = os.environ.get("AWS_REGION")

## Logger config
logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s: %(levelname)s: %(message)s"
)


s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    endpoint_url=S3_ENDPOINT_URL,
    use_ssl=False,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

s3_resource = boto3.resource("s3", region_name=AWS_REGION, endpoint_url=S3_ENDPOINT_URL)


def load_model(region: str):
    """Loading model from previously trained Prophet model"""
    MODEL_FILE = os.getenv("MODEL_FILE", f"model_prophet_{region}.bin")
    with open(MODEL_FILE, "rb") as f_in:
        model = pickle.load(f_in)
    return model


def prediction(region: str):
    """Generalizing testing data with trained Prophet model"""
    df = input_data()
    data_prep = df[["Date", "Average_Price"]].rename(
        columns={"Date": "ds", "Average_Price": "y"}
    )
    model = load_model(region)
    y_predict = model.predict(data_prep)
    df_predict = y_predict[["ds", "yhat", "yhat_lower", "yhat_upper"]]
    merge_result = pd.merge(data_prep, df_predict, how="left", on="ds")
    merge_result["yhat"] = np.round(merge_result["yhat"], decimals=2)
    merge_result["yhat_lower"] = np.round(merge_result["yhat_lower"], decimals=-4)
    merge_result["yhat_upper"] = np.round(merge_result["yhat_upper"], decimals=-4)

    ## This assertion only works for prediction made on model made for "Oxford"
    ## Comment these blocks to exclude assertion codes below
    result_dict = merge_result.to_dict()
    expected_prediction = {
        "ds": {
            0: Timestamp("2001-06-01 00:00:00"),
            1: Timestamp("2003-07-15 00:00:00"),
            2: Timestamp("2005-09-21 00:00:00"),
        },
        "y": {0: 189310, 1: 243400, 2: 142500},
        "yhat": {0: 153840.89, 1: 161832.55, 2: 227003.84},
        "yhat_lower": {0: 140000.0, 1: 150000.0, 2: 210000.0},
        "yhat_upper": {0: 170000.0, 1: 180000.0, 2: 240000.0},
    }

    assert expected_prediction == result_dict
    diff = DeepDiff(result_dict, expected_prediction, significant_digits=2)
    print(f"diff={diff}")

    assert "type_changes" not in diff
    assert "values_changed" not in diff
    ### Assertion ends ###

    return merge_result


def main():
    """Main program to make prediction and store parquet file in S3 localstack"""
    region = sys.argv[1]  # "Oxford"
    merge_result = prediction(region)
    output_file = f"{region}_predictions.parquet"
    merge_result.to_parquet(
        output_file, engine="pyarrow", compression=None, index=False
    )

    object_name = f"{region}_predictions.parquet"
    bucket = "uk-house-price-localstack"
    upload_file(output_file, bucket, object_name)
    sleep(5)
    df = read_localstack(f"s3://uk-house-price-localstack/{region}_predictions.parquet")
    print(df.head())


if __name__ == "__main__":
    main()
