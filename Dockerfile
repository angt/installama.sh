FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y \
 && apt-get install -y --no-install-recommends \
    ca-certificates wget \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /etc/apt/keyrings && cd /etc/apt/keyrings \
 && wget -qO - "https://apt.kitware.com/keys/kitware-archive-latest.asc" > kitware.asc \
 && wget -qO - "https://repo.radeon.com/rocm/rocm.gpg.key" > rocm.asc \
 && wget -qO - "https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/3bf863cc.pub" > cuda.asc

COPY <<EOF /etc/apt/sources.list.d/installama.list
deb [signed-by=/etc/apt/keyrings/kitware.asc] https://apt.kitware.com/ubuntu jammy main
deb [signed-by=/etc/apt/keyrings/rocm.asc]    https://repo.radeon.com/rocm/apt/7.0.3 jammy main
deb [signed-by=/etc/apt/keyrings/cuda.asc]    https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64 /
EOF

RUN apt-get update -y \
 && apt-get install -y --no-install-recommends \
    git ninja-build cmake zstd \
 && rm -rf /var/lib/apt/lists/*
