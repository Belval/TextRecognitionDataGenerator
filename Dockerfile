# We use Ubuntu as base image
FROM ubuntu:18.04

WORKDIR /app

# Install dependencies
RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y \
    locales \
    python3-pip \
    libsm6 \
    libfontconfig1 \
    libxrender1 \
    libxext6 \
 && rm -rf /var/lib/apt/lists/*

# Set the locale
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8  

COPY . /app

RUN python3 setup.py install

