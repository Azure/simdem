#!/bin/bash

# Publishes SimDem containers.
#
# Usage:
#
# publish.sh            - publiches both containers (cli and novnc)
# publish.sh novnc      - publishes the novnc version of the container
# publish.sh cli        - publishes the CLI version of the container

REPOSITORY=rgardler
FLAVOR=${1:-}
CONTAINERNAME=simdem_$FLAVOR

VERSION=`grep -Po '(?<=SIMDEM_VERSION = \")(.*)(?=\")' config.py`

print_result() {
    if [ $1 -eq 0 ]; then
	echo "Published $2"
    else
	echo "Failed to publish $2"
	exit 1
    fi
}


if [[ $FLAVOR == "novnc" ]]; then
    docker push $REPOSITORY/$CONTAINERNAME:$VERSION
    print_result $?  "$REPOSITORY/$CONTAINERNAME:$VERSION"
elif [[ $FLAVOR == "cli" ]]; then
    docker push $REPOSITORY/$CONTAINERNAME:$VERSION
    print_result  $? "$REPOSITORY/$CONTAINERNAME:$VERSION"
				  
else
    docker push $REPOSITORY/${CONTAINERNAME}cli:$VERSION
    print_result $?  "$REPOSITORY/${CONTAINERNAME}cli:$VERSION"

    docker push $REPOSITORY/${CONTAINERNAME}novnc:$VERSION
    print_result $?  "$REPOSITORY/${CONTAINERNAME}novnc:$VERSION"
fi
