import logging
import boto3
from botocore.exceptions import ClientError
import os
import json

AWS_REGION = ''  
# AWS_PROFILE = 'localstack'
ENDPOINT_URL = 'http://localhost:4566'
ACCESS_KEY = ""
SECRET_KEY = ""
S3_ENDPOINT_URL = os.getenv('ENDPOINT_URL',"http://localhost:4566")
# S3_CLIENT = boto3.client('s3', endpoint_url=S3_ENDPOINT_URL)

# boto3.setup_default_session(profile_name=AWS_PROFILE)

s3_client = boto3.client("s3", region_name=AWS_REGION,
                         endpoint_url=S3_ENDPOINT_URL,
                         use_ssl=False,
                        aws_access_key_id=ACCESS_KEY,
                        aws_secret_access_key=SECRET_KEY)

localstack_resource = boto3.resource("s3", region_name=AWS_REGION,
                         endpoint_url=ENDPOINT_URL)

def create_bucket(bucket_name):
    """
    Creates a S3 bucket.
    """
    try:
        response = s3_client.create_bucket(
            Bucket=bucket_name)
    except ClientError:
        raise
    else:
        return response

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
        return response


def main():
    """
    Main invocation function.
    """
    file_name = '2021_05_predictions.parquet'
    object_name = '2021_05_predictions.parquet'
    bucket = 'nyc-duration'
    s3 = upload_file(file_name, bucket, object_name)


if __name__ == '__main__':
    main()