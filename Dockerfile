FROM consol/ubuntu-xfce-vnc

USER 0

RUN apt-get update

# Not really needed, but used in the SimDem demo script
RUN apt-get install tree -y
RUN apt-get install python3-pip -y

# Azure CLI
RUN echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ wheezy main" | tee /etc/apt/sources.list.d/azure-cli.list
RUN apt-get install apt-transport-https -y
RUN apt-get update
RUN apt-key adv --keyserver packages.microsoft.com --recv-keys 417A0893
RUN apt-get install azure-cli -y --allow-unauthenticated
RUN mkdir -p .azure

RUN mkdir src
COPY . src
RUN pip3 install -r src/requirements.txt

# Desktop
COPY ./novnc/ /headless/
RUN install/set_user_permission.sh /headless
RUN rm /headless/.config/bg_sakuli.png

# SimDem
COPY demo_scripts demo_scripts
COPY simdem.py /usr/local/bin/simdem.py
RUN chmod +x /usr/local/bin/simdem.py
RUN ln -s /usr/local/bin/simdem.py /usr/local/bin/simdem

### VNC config
ENV VNC_COL_DEPTH 24
ENV VNC_RESOLUTION 1024x768
ENV VNC_PW vncpassword

USER 1984
