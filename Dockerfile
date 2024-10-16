# pull the official base image
FROM python:3.10-slim-bullseye

RUN mkdir -p /usr/src/app
# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt

# copy project
ADD . /usr/src/app

EXPOSE 7000
