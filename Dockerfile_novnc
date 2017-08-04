FROM consol/ubuntu-xfce-vnc

# FIXME: For consistency with CLI we should use /home/simdem, currently using /headless because that's what comes with novnc container
ENV HOME /headless
WORKDIR $HOME

### VNC config
ENV NO_VNC_PORT 8080
ENV VNC_COL_DEPTH 24
ENV VNC_RESOLUTION 1024x768
ENV VNC_PW vncpassword

USER 0

RUN apt-get update

# Not really needed but handy when debugging
RUN apt-get install emacs -y

# Not really needed, but used in the SimDem demo script
RUN apt-get install tree -y

# Azure CLI
RUN echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ wheezy main" | tee /etc/apt/sources.list.d/azure-cli.list
RUN apt-get install apt-transport-https -y
RUN apt-get update
RUN apt-key adv --keyserver packages.microsoft.com --recv-keys 417A0893
RUN apt-get install azure-cli -y --allow-unauthenticated

# Python
RUN apt-get install python3-pip -y

# Desktop
USER 1984
COPY ./novnc/ /headless/
USER 0
RUN rm .config/bg_sakuli.png
RUN rm Desktop/chromium-browser.desktop

# Create SimDem User
USER 0
RUN apt-get install sudo -y
RUN apt-get install whois -y
RUN useradd simdem -u 1984 -p `mkpasswd password` -d $HOME -s /bin/bash
RUN usermod -aG sudo simdem
RUN echo "simdem ALL=NOPASSWD: ALL" >> /etc/sudoers
RUN mkdir -p $HOME && chown -R 1984 $HOME
RUN mkdir -p $HOME/.azure && chown -R 1984 $HOME/.azure
RUN mkdir -p $HOME/.ssh && chown -R 1984 $HOME/.ssh
RUN mkdir -p $HOME/demo_scripts && chown -R 1984 $HOME/demo_scripts

# SimDem
COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN mkdir /usr/local/bin/simdem_cli
COPY *.py /usr/local/bin/simdem_cli/
RUN chmod +x /usr/local/bin/simdem_cli/main.py
RUN ln -s /usr/local/bin/simdem_cli/main.py /usr/local/bin/simdem

# Demo Scripts
COPY demo_scripts/simdem demo_scripts

USER 1984

COPY demo_scripts demo_scripts
