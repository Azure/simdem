FROM consol/ubuntu-xfce-vnc

USER 0

RUN apt-get update
RUN apt-get install tree -y
RUN apt-get install python3-pip -y

RUN mkdir src
COPY . src
RUN pip3 install -r src/requirements.txt

COPY demo_scripts demo_scripts
COPY simdem.py /usr/local/bin/simdem.py
RUN chmod +x /usr/local/bin/simdem.py
RUN ln -s /usr/local/bin/simdem.py /usr/local/bin/simdem

### VNC config
ENV VNC_COL_DEPTH 24
ENV VNC_RESOLUTION 1024x768
ENV VNC_PW vncpassword

USER 1984

