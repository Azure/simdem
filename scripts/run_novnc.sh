#!/bin/bash

# Runs a headless VNC Docker container with Simdem installed.
#
# Usage: run_novnc.sh [SCRPT_DIR]
#
# SCRIPT_DIR is an optional parameter to define a directory containing
# SimDem scripts that will be mounted into the final container. Default
# value is `demo_scripts`.
#
# Connect with a browser at http://YOUR_DOCKER_HOST:8080/?password=vncpassword
#
# Based on https://github.com/ConSol/docker-headless-vnc-container
#
# Configuration options:
# You can configure the following variables to change behaviour of
# the container.
#
# VNC config
# ==========
VNC_COL_DEPTH='24'
VNC_RESOLUTION='1024x768'
VNC_PW='vncpassword'

SCRIPT_DIR=demo_scripts

docker stop simdem_novnc
docker rm simdem_novnc

docker run -d -p 5901:5901 -p 8080:6901 --name simdem_novnc \
       --volume azure_data:/headless/.azure \
       -e VNC_COL_DEPTH=$VNC_COL_DEPTH \
       -e VNC_RESOLUTION=$VNC_RESOLUTION \
       -e VNC_PW=$VNC_PW \
       rgardler/simdem:novnc
