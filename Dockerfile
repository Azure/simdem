FROM consol/ubuntu-xfce-vnc

USER 0

RUN apt-get update
RUN apt-get install python3-pip -y

RUN mkdir src
COPY . src
RUN pip3 install -r src/requirements.txt

RUN apt-get install tree -y

COPY demo_scripts demo_scripts
COPY simdem.py /usr/local/bin/simdem.py
RUN chmod +x /usr/local/bin/simdem.py
RUN ln -s /usr/local/bin/simdem.py /usr/local/bin/simdem

USER 1984

