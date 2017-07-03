#!/bin/bash

# Builds a SimDem container.
#
# Usage:
#
# build.sh                  - builds both containers (cli and novnc)
# TODO: build.sh novnc      - builds the novnc version of the container
# TODO: build.sh cli        - builds the CLI version of the container

REPOSITORY=rgardler
FLAVOR=${1:-}
CONTAINERNAME=simdem_$FLAVOR

VERSION=`grep -Po '(?<=SIMDEM_VERSION = \")(.*)(?=\")' simdem.py`

echo Building $REPOSITORY/$CONTAINERNAME:$VERSION .


print_result() {
    if [ $1 -eq 0 ]; then
	echo "Built $2"
    else
	echo "Failed to build $2"
	exit 1
    fi
}


if [[ $FLAVOR == "novnc" ]]; then
    docker build -f Dockerfile_$FLAVOR -t $REPOSITORY/$CONTAINERNAME:$VERSION .
    print_result $?  "$REPOSITORY/$CONTAINERNAME:$VERSION ."
elif [[ $FLAVOR == "cli" ]]; then
    docker build -f Dockerfile_$FLAVOR -t $REPOSITORY/$CONTAINERNAME:$VERSION .
    print_result  $? "$REPOSITORY/$CONTAINERNAME:$VERSION ."
				  
else
    docker build -f Dockerfile_cli -t $REPOSITORY/${CONTAINERNAME}cli:$VERSION .
    print_result $?  "$REPOSITORY/${CONTAINERNAME}cli:$VERSION ."
    docker build -f Dockerfile_novnc -t $REPOSITORY/${CONTAINERNAME}novnc:$VERSION .
    print_result $?  "$REPOSITORY/${CONTAINERNAME}novnc:$VERSION ."
fi    
