FROM python:3

WORKDIR /usr/src/app
RUN apt-get update

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install -v -e .

# The default prompt is # which throws off the initialization
RUN echo 'export PS1="$ "' >> /root/.bashrc

CMD [ "simdem" ]

