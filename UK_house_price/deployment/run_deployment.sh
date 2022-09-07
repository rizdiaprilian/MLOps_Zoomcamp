#!/usr/bin/env perl

cd "$(dirname "$0")"

LOCAL_TAG=`date +"%Y-%m-%d-%H-%M-%S"`
export LOCAL_IMAGE_NAME="uk-house-model:${LOCAL_TAG}"

docker build -t ${LOCAL_IMAGE_NAME} .

docker run -it --rm \
    -p 9696:9696 \
    -e RUN_ID=${RUN_ID} \
    -e REGION=${REGION} \
    -e AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} \
    -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}\
    -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}\
    ${LOCAL_IMAGE_NAME}
