import logging
import boto3
from botocore.exceptions import ClientError
import os
import json
import pickle

ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL',"http://localhost:4566")
AWS_REGION = os.environ.get('AWS_REGION')

## Logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')


s3_client = boto3.client("s3", region_name=AWS_REGION,
                         endpoint_url=S3_ENDPOINT_URL,
                         use_ssl=False,
                        aws_access_key_id=ACCESS_KEY,
                        aws_secret_access_key=SECRET_KEY)

s3_resource = boto3.resource("s3", region_name=AWS_REGION,
                         endpoint_url=S3_ENDPOINT_URL)


def create_bucket(bucket_name):
    """
    Creates a S3 bucket.
    """
    try:
        response = s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': AWS_REGION})
    except ClientError:
        logger.exception('Could not create S3 bucket locally.')
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
        logger.info('Upload file to s3 bucket localstack finishes...')
        return response

def download_file(file_name, bucket, object_name):
    """
    Download a file from a S3 bucket.
    """
    try:
        response = s3_resource.Bucket(bucket).download_file(object_name, file_name)
    except ClientError:
        logger.exception('Could not download file to S3 bucket.')
        raise
    else:
        return response

def main():
    """
    Main invocation function.
    """
    bucket_name = 'uk-house-price-localstack'
    logger.info('Creating S3 bucket locally using LocalStack...')
    s3 = create_bucket(bucket_name)
    logger.info('S3 bucket created.')
    logger.info(json.dumps(s3, indent=4) + '\n')
    # file_name = 'model_prophet_Oxford.bin'
    # object_name = 'model_prophet_Oxford.bin'
    # s3 = upload_file(file_name, bucket_name, object_name)
    # s3 = download_file(file_name, bucket_name, object_name)


if __name__ == '__main__':
    main()