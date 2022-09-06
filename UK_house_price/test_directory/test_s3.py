import os
from pprint import pprint
import boto3

print(os.environ.get('AWS_DEFAULT_REGION'))
print(os.environ.get('AWS_REGION'))
print(os.environ.get('AWS_ACCESS_KEY_ID'))
print(os.environ.get('AWS_SECRET_ACCESS_KEY'))
s3_endpoint = os.getenv('S3_ENDPOINT_URL', "http://localhost:4566")
s3_client = boto3.client('s3', endpoint_url=s3_endpoint)

bucket = "UK-house-price-localstack"

response = s3_client.list_buckets()

pprint(response)