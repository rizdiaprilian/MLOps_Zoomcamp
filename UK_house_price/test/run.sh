#!/usr/bin/env perl

cd "$(dirname "$0")"

LOCAL_TAG=`date +"%Y-%m-%d-%H-%M-%S"`
export LOCAL_IMAGE_NAME="UK-house-model:${LOCAL_TAG}"

## Docker test
docker build -t ${LOCAL_IMAGE_NAME} ..

docker run -it -rm \
    -p 8080: 8080 \
    -e PREDICTION_NAME="UK_house_price" \
    -e RUN_ID="uibg329rg9bwwegwrg" \
    -e MODEL_LOCATION="/app/model" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="eu-west-1" \
    -v $(pwd)/model:/app/model \
    ${LOCAL_IMAGE_NAME}

pipenv run python test_model.py