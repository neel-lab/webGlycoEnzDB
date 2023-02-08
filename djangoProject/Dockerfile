FROM python:3.8-slim

WORKDIR /app

EXPOSE 8000

RUN apt-get update
RUN apt-get install -y python3-dev default-libmysqlclient-dev build-essential libpq-dev
#RUN apt-get install -y
RUN pip install --upgrade pip

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

RUN python manage.py makemigrations
RUN python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]