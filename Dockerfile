FROM azuresdk/azure-cli-python:0.2.10

RUN pip install pexpect

RUN apk add tree

COPY demo_scripts demo_scripts
COPY simdem.py /usr/local/bin/simdem.py
RUN chmod +x /usr/local/bin/simdem.py
RUN ln -s /usr/local/bin/simdem.py /usr/local/bin/simdem

ENTRYPOINT [ "simdem" ]
CMD ["-s", "tutorial", "run", "simdem"]


