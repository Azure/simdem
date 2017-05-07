FROM azuresdk/azure-cli-python:0.2.7

COPY demo_scripts demo_scripts
COPY run.py run.py

ENTRYPOINT [ "python", "./run.py" ]
CMD ["-s", "tutorial", "run", "simdem"]


