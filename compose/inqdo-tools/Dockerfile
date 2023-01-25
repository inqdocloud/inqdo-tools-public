FROM python:3.8.7-alpine

RUN mkdir /usr/src/app

RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo libressl-dev bash make

COPY requirements-dev.txt .editorconfig setup.cfg Makefile /usr/src/app/

WORKDIR /usr/src/app

RUN python3 -m ensurepip
RUN pip install --no-cache --upgrade pip setuptools
RUN pip install -r requirements-dev.txt

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/inqdo_tools"

CMD tail -f /dev/null
