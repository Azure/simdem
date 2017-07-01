#!/bin/bash

# Runs a headless VNC Docker container with Simdem installed.
#
# Usage: run.sh [FLAVOR] [SCRIPT_DIR]
#
# FLAVOR is an optional parameter to define which container to run,
# either the `novnc` or the `cli` versions. If not specified the
# `novnc` version is used
#
# SCRIPT_DIR is an optional parameter to define a directory containing
# SimDem scripts that will be mounted into the final container. Default
# value is `./demo_scripts`.
#
# Connect with a browser at http://YOUR_DOCKER_HOST:8080/?password=vncpassword
#
# Based on https://github.com/ConSol/docker-headless-vnc-container


# Configuration options:
# You can configure the following variables to change behaviour of
# the container.
#
# VNC config
# ==========
VNC_COL_DEPTH='24'
VNC_RESOLUTION='1024x768'
VNC_PW='vncpassword'

FLAVOR=${1:-novnc}
SCRIPTS_DIR=${2:-`pwd`/demo_scripts}
REPOSITORY=rgardler
CONTAINER_NAME=simdem_$FLAVOR
SCRIPTS_VOLUME=${CONTAINER_NAME}_scripts
AZURE_VOLUME=azure_data
if [[ $FLAVOR == "novnc" ]]; then
    HOME="/headless"
else
    HOME=""
fi

VERSION=`grep -Po '(?<=SIMDEM_VERSION = \")(.*)(?=\")' simdem.py`

echo Runing $REPOSITORY/$CONTAINER_NAME:$VERSION

echo Stopping and removing pre-existing containers
docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME
docker stop $SCRIPTS_VOLUME
docker rm $SCRIPTS_VOLUME

echo Creating scripts data container named $SCRIPTS_VOLUME containing the scripts in $SCRIPTS_DIR
docker create -v $HOME/demo_scripts --name $SCRIPTS_VOLUME ubuntu /bin/true
docker cp $SCRIPTS_DIR/. $SCRIPTS_VOLUME:$HOME/demo_scripts/

echo starting the $CONTAINER_NAME container
if [[ $FLAVOR == "novnc" ]]; then
   docker run -d -p 5901:5901 -p 8080:6901 --name $CONTAINER_NAME \
       --volume $AZURE_VOLUME:$HOME/.azure \
       --volumes-from $SCRIPTS_VOLUME \
       -e VNC_COL_DEPTH=$VNC_COL_DEPTH \
       -e VNC_RESOLUTION=$VNC_RESOLUTION \
       -e VNC_PW=$VNC_PW \
       $REPOSITORY/$CONTAINER_NAME:$VERSION
else
    docker run -it \
       --volume $AZURE_VOLUME:$HOME/.azure \
       --volumes-from $SCRIPTS_VOLUME \
       --name $CONTAINER_NAME $REPOSITORY/$CONTAINER_NAME:$VERSION
fi
