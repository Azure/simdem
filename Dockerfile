FROM python:3.5.1

COPY demo_scripts demo_scripts
COPY run.py run.py

ENTRYPOINT [ "python", "./run.py" ]
CMD ["-s", "tutorial", "run", "simdem"]


