#!/usr/bin/env perl

cd "$(dirname "$0")"

LOCAL_TAG=`date +"%Y-%m-%d-%H-%M-%S"`
export LOCAL_IMAGE_NAME="uk-house-model:${LOCAL_TAG}"

## Docker test
docker build --tag python-docker .
docker build --tag uk-house-price:v2 ..

docker build -t ${LOCAL_IMAGE_NAME} ..

docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTION_NAME="UK_house_price" \
    -e RUN_ID="a83db8840d254e9095dfe0ed2bc92158" \
    -e MODEL_LOCATION="/app/model" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="eu-west-2" \
    -e AWS_ACCESS_KEY_ID="AKIARBMT65NSJIDOVSB3"\
    -e AWS_SECRET_ACCESS_KEY="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"\
    -v $(pwd)/model:/app/model \
    # ${LOCAL_IMAGE_NAME}
    uk-house-price:v2

pipenv run python test_model.py