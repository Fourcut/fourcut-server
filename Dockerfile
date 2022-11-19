FROM python:3.10.8

WORKDIR /code
# 컨테이너 내 경로

COPY ./requirements.txt /code/requirements.txt

COPY ./gunicorn.conf.py /code/gunicorn.conf.py

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN mkdir log
