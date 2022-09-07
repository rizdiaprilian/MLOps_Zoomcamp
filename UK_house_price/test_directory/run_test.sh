#!/usr/bin/env perl

cd "$(dirname "$0")"

LOCAL_TAG=`date +"%Y-%m-%d-%H-%M-%S"`
export LOCAL_IMAGE_NAME="test_model:${LOCAL_TAG}"

docker build -t ${LOCAL_IMAGE_NAME} .

docker-compose up


ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi


docker-compose down