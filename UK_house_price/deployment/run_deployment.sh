#!/usr/bin/env perl

cd "$(dirname "$0")"

LOCAL_TAG=`date +"%Y-%m-%d-%H-%M-%S"`
export LOCAL_IMAGE_NAME="uk-house-model:${LOCAL_TAG}"

docker build -t ${LOCAL_IMAGE_NAME} .

docker run -it --rm \
    -p 9696:9696 \
    -e RUN_ID="a83db8840d254e9095dfe0ed2bc92158" \
    -e AWS_DEFAULT_REGION="eu-west-2" \
    -e AWS_ACCESS_KEY_ID="AKIARBMT65NSALJFY5NC"\
    -e AWS_SECRET_ACCESS_KEY="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"\
    ${LOCAL_IMAGE_NAME}