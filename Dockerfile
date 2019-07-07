# We use Ubuntu as base image
FROM ubuntu:18.04

WORKDIR /app

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3-pip \
                       libsm6 \
                       libfontconfig1 \
                       libxrender1 \
                       libxext6

COPY requirements.txt /app/

RUN pip3 install -r requirements.txt

COPY TextRecognitionDataGenerator/ /app
