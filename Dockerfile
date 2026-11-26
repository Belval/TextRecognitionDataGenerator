# We use Ubuntu as base image
FROM ubuntu:22.04

WORKDIR /app

# Install dependencies
RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y \
    git \
    locales \
    python3-pip \
    libsm6 \
    libfontconfig1 \
    libxrender1 \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    libxext6 \
    libraqm-dev \
    virtualenv \
    libgl1-mesa-glx \
 && rm -rf /var/lib/apt/lists/*

# Set the locale
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN virtualenv --python python3 /env
ENV PATH="/env/bin:$PATH"
COPY . /app/

RUN pip install --upgrade pip
RUN pip install codecov

RUN python setup.py install
RUN pip install -r requirements.txt
RUN pip install pytest

