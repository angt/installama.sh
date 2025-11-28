FROM installama

RUN apt-get update -y \
 && apt-get install -y --no-install-recommends \
    xz-utils \
 && rm -rf /var/lib/apt/lists/*

ARG ZIG_VERSION=0.15.2
ENV ZIG_GLOBAL_CACHE_DIR="/tmp/zig-cache"
ENV ZIG_LOCAL_CACHE_DIR="/tmp/zig-local"

RUN ZIG="zig-$(uname -m)-linux-$ZIG_VERSION" \
 && wget -qO- "https://ziglang.org/download/$ZIG_VERSION/$ZIG.tar.xz" | tar -Jxf- -C ~ \
 && ln -sf ~/"$ZIG"/zig /usr/bin/zig

ARG VULKAN_VERSION=1.4.328.1

RUN VULKAN="vulkansdk-linux-$(uname -m)-$VULKAN_VERSION" \
 && wget -qO- "https://sdk.lunarg.com/sdk/download/$VULKAN_VERSION/linux/$VULKAN.tar.xz" | tar -Jxf- -C /opt \
 && mv /opt/"$VULKAN_VERSION/$(uname -m)" /opt/vulkan-sdk
