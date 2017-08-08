#!/bin/bash

# Builds a SimDem container.
#
# Usage:
#
# build.sh            - builds both containers (cli and novnc)
# build.sh novnc      - builds the novnc version of the container
# build.sh cli        - builds the CLI version of the container

REPOSITORY=rgardler
FLAVOR=${1:-}
IMAGE_NAME_PREFIX=simdem_

VERSION=`grep -Po '(?<=SIMDEM_VERSION = \")(.*)(?=\")' config.py`

build_container() {
    docker build -f Dockerfile_$1 -t $REPOSITORY/${IMAGE_NAME_PREFIX}$1:$VERSION .

    if [ $? -eq 0 ]; then
	echo "Built $REPOSITORY/${IMAGE_NAME_PREFIX}$1:$VERSION"
    else
	echo "Failed to build $REPOSITORY/${IMAGE_NAME_PREFIX}$1:$VERSION"
	return 0
    fi
}

if [[ $FLAVOR == "novnc" ]]; then
    build_container novnc
elif [[ $FLAVOR == "cli" ]]; then
    build_container cli
else
    build_container cli
    if [ $? -ne 0 ]; then
    	echo "Building container failed. Exiting"
	exit 1
    fi
    build_container novnc
fi

exit $?
