#!/usr/bin/env perl

cd "$(dirname "$0")"

LOCAL_TAG=`date +"%Y-%m-%d-%H-%M-%S"`
export LOCAL_IMAGE_NAME="test_model:${LOCAL_TAG}"

## Docker test
docker build -t ${LOCAL_IMAGE_NAME} .

# docker build --tag uk-house-price:v2 ..

docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTION_NAME="test_UK_house_price" \
    -e RUN_ID="a83db8840d254e9095dfe0ed2bc92158" \
    -e MODEL_LOCATION="/app/model" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="eu-west-2" \
    -e AWS_ACCESS_KEY_ID="AKIARBMT65NSALJFY5NC"\
    -e AWS_SECRET_ACCESS_KEY="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"\
    -v $(pwd)/model:/app/model \
    ${LOCAL_IMAGE_NAME}

pipenv run python test_model.py


## Sourcing the .env file and exporting them as environment variables
set -a
source .env
set +a

python test_s3.py


## Showing differences in code quality
isort --diff . | less
## fixing codes
isort .
## see the changes
git diff integration_test.py

isort .
black .
pylint --recursive=y .
pytest tests/
