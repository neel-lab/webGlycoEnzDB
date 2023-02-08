FROM python:3.8-slim

WORKDIR /app

RUN apt-get update
RUN apt-get install -y python3-dev default-libmysqlclient-dev build-essential libpq-dev
#RUN apt-get install -y
RUN pip install --upgrade pip

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app


CMD ["python", "loadGlycoEnzOnto.py"]

