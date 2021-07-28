FROM ubuntu:18.04 AS BUILD

RUN apt-get update && apt-get -y install make python3.7 python3-pip git mc && \
    python3.7 -m pip install --upgrade pip && \
    apt-get -y install build-essential python3.7-dev && \
    apt-get -y install python3-uvloop

COPY . /app
WORKDIR /app

RUN PIP=pip PYTHON=python3.7 make deps
CMD PIP=pip PYTHON=python3.7 APP_ENV=${APP_ENV}  make run
