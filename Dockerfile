# We use Ubuntu as base image
FROM ubuntu:18.04

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
 && rm -rf /var/lib/apt/lists/*

# Set the locale
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

COPY . /app/

RUN git clone https://github.com/python-pillow/Pillow.git \
 && cd Pillow \
 && git checkout 7.0.x \
 && python3 setup.py build_ext --enable-freetype install

RUN python3 setup.py install
RUN pip3 install -r requirements.txt
RUN pip3 install pytest
RUN pip3 install codecov

