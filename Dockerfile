FROM debian
FROM python:3.7

EXPOSE 2020

WORKDIR /messenger
COPY . /messenger

RUN ["pip", "install", "sqlalchemy"]
RUN ["pip", "install", "flask"]
RUN ["python3", "setup.py", "develop"]


