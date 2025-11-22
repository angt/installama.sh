FROM installama

RUN apt-get update -y \
 && apt-get install -y --no-install-recommends \
    libxml2 rocm-hip-sdk \
 && rm -rf /var/lib/apt/lists/*
