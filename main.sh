#!/bin/bash

# POINT TO CONFIG
CONFIG_REL_PATH="cfg_app_params.json"

# DECLARE VARIABLES
DTTM=$(date +%s)

DATA_DANYCH=$(jq -r '.data_end_date' ${CONFIG_REL_PATH})

API_URL=$(jq -r '.api_params.api_url' ${CONFIG_REL_PATH}) 
API_TOKEN=$(jq -r '.api_params.api_token' ${CONFIG_REL_PATH})

SYSTEM_USER_NAME=$(jq -r '.docker_params.system_user' ${CONFIG_REL_PATH})
APP_DIR=$(jq -r '.app_bin' ${CONFIG_REL_PATH})
FILE_PREFIX=$(jq -r '.file_prefix' ${CONFIG_REL_PATH})
OUTPUT_DIR=$(jq -r '.output_dir' ${CONFIG_REL_PATH})

DOCKER_IMG_TAG="${DTTM}"
DOCKER_IMG_NAME=$(jq -r '.docker_params.img_name' ${CONFIG_REL_PATH})
DOCKER_CONTAINER_NAME=$(jq -r '.docker_params.container_name' ${CONFIG_REL_PATH})

DOCKER_WORKDIR="/home/${SYSTEM_USER_NAME}"
DOCKER_APP_ROOT="/home/${SYSTEM_USER_NAME}/${DOCKER_CONTAINER_NAME}"

FILE_MASK="${FILE_PREFIX}_${DATA_DANYCH}_${DOCKER_IMG_TAG}.csv"

# BUILD APP DOCKER IMAGE
docker build --no-cache \
    --build-arg SYSTEM_USER_NAME=${SYSTEM_USER_NAME} \
    --build-arg FAKTURAPP_ROOT=${DOCKER_APP_ROOT} \
    --build-arg API_URL=${API_URL} \
    --build-arg DOCKER_IMG_TAG=${DOCKER_IMG_TAG} \
    --build-arg DATA_DANYCH=${DATA_DANYCH} \
    --build-arg FILE_MASK=${FILE_MASK} \
    --build-arg API_TOKEN=${API_TOKEN} \
    --tag=$DOCKER_IMG_NAME:$DOCKER_IMG_TAG \
    --progress=plain \
    $APP_DIR

# RUN APP DOCKER CONTAINER
docker run --name $DOCKER_CONTAINER_NAME $DOCKER_IMG_NAME:$DOCKER_IMG_TAG

# COPY OUTPUT FILE TO SELECTED DIRECTORY
docker cp ${DOCKER_CONTAINER_NAME}:${DOCKER_APP_ROOT}/output_dir/${FILE_MASK} ${OUTPUT_DIR}

# AFTER CODE EXECUTION, REOMOVE IMAGE(S) AND CONTAINERS
docker rm -f $DOCKER_CONTAINER_NAME
docker image rm $DOCKER_IMG_NAME:$DOCKER_IMG_TAG
