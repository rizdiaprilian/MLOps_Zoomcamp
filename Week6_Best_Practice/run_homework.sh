# docker-compose up -d

# aws --endpoint-url=http://localhost:4566 s3 mb s3://nyc-duration

# awsls s3api create-bucket --bucket hands-on-cloud-localstack-bucket

# aws --endpoint-url=http://localhost:4566 s3 ls
## or
# awslocal s3 ls

awslocal s3 ls s3://nyc-duration --recursive --human-readable

export INPUT_FILE_PATTERN="s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
export OUTPUT_FILE_PATTERN="s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"

python batch_second.py 2021 10