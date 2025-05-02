FROM ubuntu:22.04

RUN apt update && apt install -y \
    build-essential \
    git \
    libcap-dev \
    pkg-config \
    libsystemd-dev \
    python3 \
    python3-pip \
    libxml2-utils && \  
    pip install --no-cache-dir fastapi uvicorn httpx && \
    python3 -m pip install asciidoc

RUN git clone https://github.com/ioi/isolate.git /isolate

WORKDIR /isolate
RUN make isolate
RUN make install
