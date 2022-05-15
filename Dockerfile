FROM python:3.7.12-slim
WORKDIR /opt/app

COPY . /opt/app

RUN python -m pip install -r requirements.txt
