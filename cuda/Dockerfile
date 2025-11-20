FROM installama

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    gcc g++ cuda-toolkit-12-4 \
 && rm -rf /var/lib/apt/lists/*

ENV PATH=/usr/local/cuda-12.4/bin:${PATH}
