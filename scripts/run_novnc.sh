# Runs a headless VNC Docker container with Simdem installed.
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


docker stop simdem_novnc
docker rm simdem_novnc

docker run -d -p 5901:5901 -p 8080:6901 --name simdem_novnc \
       -v ~/.azure:/headless/.azure \
       -e VNC_COL_DEPTH=$VNC_COL_DEPTH \
       -e VNC_RESOLUTION=$VNC_RESOLUTION \
       -e VNC_PW=$VNC_PW \
       rgardler/simdem:novnc
