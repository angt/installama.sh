# `installama.sh`

_The fastest way to install `llama.cpp` on Linux and macOS._

`installama.sh` is a simple shell script that downloads and sets up a prebuilt `llama-server` binary for your system.
It automatically detects your OS, architecture, and GPU capabilities, so you can start using `llama.cpp` in seconds.

## Features

- **Automatic detection** of CPU architecture (`x86_64` / `aarch64`) and OS (`Linux` / `macOS`).
- Support for **GPU acceleration**:
  - CUDA: `50` `61` `70` `75` `80` `86` `89`.
  - ROCm: `gfx803` `gfx900` `gfx906` `gfx908` `gfx90a` `gfx942` `gfx1010` `gfx1011` `gfx1030` `gfx1032` `gfx1100` `gfx1101` `gfx1102` `gfx1200` `gfx1201` `gfx1151`.
  - Metal: `M1` `M2` `M3` `M4`.
- Fallback to **CPU optimized** builds if the GPU is not available.
- **Lightweight** and **Fast**!


## Usage

Install `llama-server` in one easy step:

    curl https://angt.github.io/installama.sh | sh

Then run the server, for example, with the [new awesome WebGUI](https://github.com/ggml-org/llama.cpp/discussions/16938):

    ~/.installama/llama-server -hf ggml-org/gpt-oss-20b-GGUF --jinja -c 0 --port 8033

And open your favorite browser to http://127.0.0.1:8033/


---
If it doesn't work on your system, please [create an issue](https://github.com/angt/installama.sh/issues/new). 

