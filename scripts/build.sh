#!/bin/bash

# Builds a SimDem container.
#
# Usage:
#
# build.sh            - builds the default container (novnc)
# TODO: build.sh novnc      - builds the default container (novnc)
# TODO: build.sh cli        - builds the CLI version of the container

REPOSITORY=rgardler
FLAVOR=${1:-novnc}
CONTAINERNAME=simdem_$FLAVOR

VERSION=`grep -Po '(?<=SIMDEM_VERSION = \")(.*)(?=\")' simdem.py`

echo Building $REPOSITORY/$CONTAINERNAME:$VERSION .

docker build -f Dockerfile_$FLAVOR -t $REPOSITORY/$CONTAINERNAME:$VERSION .

echo Built $REPOSITORY/$CONTAINERNAME:$VERSION .
