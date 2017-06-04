FROM azuresdk/azure-cli-python:0.2.10

RUN pip install pexpect

RUN apk add tree

COPY demo_scripts demo_scripts
COPY run.py run.py

ENTRYPOINT [ "python", "./simdem.py" ]
CMD ["-s", "tutorial", "run", "simdem"]


