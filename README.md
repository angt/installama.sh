# `installama.sh`

_The fastest way to install `llama.cpp` on Linux and macOS._

`installama.sh` is a simple shell script that downloads and sets up a prebuilt `llama-server` binary for your system.
It automatically detects your OS, architecture, and GPU capabilities, so you can start using `llama.cpp` in seconds.

## Features

- Supported architectures: `x86_64`, `aarch64`.
- Supported OS: `Linux`, `macOS`, `FreeBSD`.
- **Automatic detection** for **CPU acceleration**.
- **Automatic detection** for **GPU acceleration**: `CUDA`, `ROCm`, `Vulkan`, `Metal`.
- Builds are kept as **lightweight** as possible without compromising performance.

See the full list of supported hardware and build configurations in [PRESETS.md](PRESETS.md).

## Usage

Install `llama-server` in one easy step:

    curl angt.github.io/installama.sh | sh

Then run the server, for example, with the [new awesome WebGUI](https://github.com/ggml-org/llama.cpp/discussions/16938):

    ~/.installama/llama-server -hf unsloth/Qwen3-4B-GGUF:Q4_0

And open your favorite browser to http://127.0.0.1:8080/.

You can also directly launch a model in a single command:

    curl angt.github.io/installama.sh | MODEL=unsloth/Qwen3-4B-GGUF:Q4_0 sh

In some scenarios, you may want to skip the CUDA backend.
You can do this with the following command:

    curl angt.github.io/installama.sh | SKIP_CUDA=1 sh

Skipping ROCm is also possible by setting `SKIP_ROCM=1`.


---
⚠️ This is still a PoC. If it doesn't work on your system, please [create an issue](https://github.com/angt/installama.sh/issues/new).
