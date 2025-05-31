FROM ubuntu:22.04

RUN apt update && apt install -y \
    build-essential \
    git \
    libcap-dev \
    pkg-config \
    libsystemd-dev \
    curl \
    python3 \
    python3-pip \
    libxml2-utils \
    gcc \
    g++ \
    make \
    cmake \
    binutils \
    libc6-dev \
    libgcc-11-dev \
    libstdc++-11-dev \
    && pip install --no-cache-dir fastapi uvicorn httpx \
    && python3 -m pip install asciidoc

# Install isolate dependencies
RUN apt install -y libcap2-bin cgroup-tools

RUN git clone https://github.com/ioi/isolate.git /isolate
WORKDIR /isolate
RUN make isolate && make install

# Create essential symlinks
RUN ln -s /usr/bin/gcc /usr/local/bin/gcc && \
    ln -s /usr/bin/g++ /usr/local/bin/g++ && \
    ln -s /usr/bin/cpp /usr/local/bin/cpp

# Create symlinks for all GCC components
RUN for f in /usr/bin/gcc* /usr/bin/g++* /usr/bin/cpp*; do \
      ln -s $f /usr/local/bin/$(basename $f); \
    done