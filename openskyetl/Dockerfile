FROM python:3.10.2-slim-bullseye AS base

WORKDIR /app

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN python setup.py install

CMD ["openskyetl", "--async-run"]
