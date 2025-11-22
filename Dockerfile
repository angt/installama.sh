FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y \
 && apt-get install -y --no-install-recommends \
    ca-certificates wget \
 && rm -rf /var/lib/apt/lists/*

RUN cd /etc/apt/trusted.gpg.d \
 && wget -qO kitware.asc "https://apt.kitware.com/keys/kitware-archive-latest.asc" \
 && wget -qO rocm.asc    "https://repo.radeon.com/rocm/rocm.gpg.key" \
 && wget -qO cuda.asc    "https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/3bf863cc.pub"

COPY <<EOF /etc/apt/sources.list.d/installama.list
deb https://apt.kitware.com/ubuntu jammy main
deb https://repo.radeon.com/rocm/apt/7.0.3 jammy main
deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64 /
EOF

COPY <<EOF /etc/apt/preferences.d/rocm-pin
Package: *
Pin: release o=repo.radeon.com
Pin-Priority: 600
EOF

RUN apt-get update -y \
 && apt-get install -y --no-install-recommends \
    git ninja-build cmake zstd \
 && rm -rf /var/lib/apt/lists/*
