FROM installama

COPY <<EOF /etc/apt/preferences.d/rocm-pin
Package: *
Pin: origin repo.radeon.com
Pin-Priority: 1001
EOF

# libxml2 is missing: /opt/rocm-7.0.3/lib/llvm/bin/ld.lld: error while loading shared libraries: libxml2.so.2
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    libxml2 rocm-hip-sdk \
 && rm -rf /var/lib/apt/lists/*
