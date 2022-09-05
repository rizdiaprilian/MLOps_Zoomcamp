from pathlib import Path
from datetime import datetime
from pandas.testing import assert_frame_equal
from pandas import Timestamp
import pandas as pd
import os, pickle
import numpy as np
from deepdiff import DeepDiff
import boto3
from botocore.exceptions import ClientError


AWS_REGION = os.getenv('AWS_REGION', "")
ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID', "")
SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', "")
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

def dt(year, month, day):
    return datetime(year, month, day)

def input_data():
    data = [
            (dt(2001, 6, 1), 'Newcastle upon Tyne', 'E060003', 189310, 2.3, 1.3, 146575),
            (dt(2003, 7, 15), 'Liverpool', 'F423103', 243400, 2.3, 2.3, 242358),
            (dt(2005, 9, 21), 'Kent', 'B80514', 142500, 2.3, 2.3, 134131), 
    ]

    columns = ['Date', 'Region_Name', 'Area_Code', 'Average_Price', 'Monthly_Change',
       'Annual_Change', 'Average_Price_SA']
    df = pd.DataFrame(data, columns=columns)
    df["Date"] = pd.to_datetime(df.Date)
    output_file = 'Oxford_predictions.parquet'
    df.to_parquet(
            output_file,
            engine='pyarrow',
            compression=None,
            index=False
        )

    object_name = f'Oxford_predictions.parquet'
    bucket = 'UK-house-price-localstack'
    s3 = upload_file(output_file, bucket, object_name)
    return df

def load_model():
    MODEL_FILE = os.getenv('MODEL_FILE', f'model_prophet_Oxford.bin')
    with open(MODEL_FILE, 'rb') as f_in:
        model = pickle.load(f_in)
    return model


def predict_features():
    df = input_data()
    data_prep = df[['Date','Average_Price']].rename(columns={'Date': 'ds', 'Average_Price': 'y'})
    expected_result = {
        'ds': {0: Timestamp('2001-06-01 00:00:00'), 1: Timestamp('2003-07-15 00:00:00'),
                    2: Timestamp('2005-09-21 00:00:00')},
        'y': {0: 189310, 1: 243400, 2: 142500},
        }

    df_expected = pd.DataFrame(expected_result)
    assert_frame_equal(data_prep, df_expected)
    model = load_model()
    y_predict = model.predict(data_prep)
    
    df_predict = y_predict[['ds','yhat','yhat_lower','yhat_upper']]
    merge_result = pd.merge(data_prep, df_predict, how="left", on="ds")
    merge_result['yhat'] = np.round(merge_result['yhat'], decimals = 2)
    merge_result['yhat_lower'] = np.round(merge_result['yhat_lower'], decimals =-4)
    merge_result['yhat_upper'] = np.round(merge_result['yhat_upper'], decimals =-4)

    result_dict = merge_result.to_dict()
    expected_prediction = {
        'ds': {0: Timestamp('2001-06-01 00:00:00'), 1: Timestamp('2003-07-15 00:00:00'),
                    2: Timestamp('2005-09-21 00:00:00')},
        'y': {0: 189310, 1: 243400, 2: 142500},
        'yhat': {0: 153840.89, 1: 161832.55, 2: 227003.84},
        'yhat_lower': {0: 140000.0, 1: 150000.0, 2: 210000.0},
        'yhat_upper': {0: 170000.0, 1: 180000.0, 2: 240000.0},
    }
    assert expected_prediction == result_dict
    diff = DeepDiff(result_dict, expected_prediction, significant_digits=2)
    print(f'diff={diff}')

    assert 'type_changes' not in diff
    assert 'values_changed' not in diff


if __name__ == '__main__':
    predict_features()
