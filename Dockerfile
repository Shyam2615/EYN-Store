# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

WORKDIR /app

COPY requirments.txt requirments.txt

RUN pip3 install -r requirments.txt

COPY . .

EXPOSE 8000

CMD python manage.py runserver