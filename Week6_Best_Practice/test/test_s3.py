import os
import json
from pprint import pprint

import boto3


s3_endpoint = os.getenv('S3_ENDPOINT_URL', "http://localhost:4566")
s3_client = boto3.client('s3', endpoint_url=s3_endpoint)

bucket = "nyc-duration"

response = s3_client.list_buckets()

pprint(response)