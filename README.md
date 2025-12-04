# `installama.sh`

_Instantly install llama.cpp._

`installama.sh` is a simple script that downloads and sets up a prebuilt `llama-server` binary for your system.
It automatically detects your OS, architecture, and GPU capabilities, so you can start using `llama.cpp` in seconds.

## Features

- Supported architectures: `x86_64`, `aarch64`.
- Supported OS: `Linux`, `macOS`, `FreeBSD`, `Windows`.
- **Automatic detection** for **CPU acceleration**.
- **Automatic detection** for **GPU acceleration**: `CUDA`, `ROCm`, `Vulkan`, `Metal`.
- Builds are kept as **lightweight** as possible without compromising performance.

> [!WARNING]
> **Active Development**
> - Some backends may be missing or incomplete.
> - Performance optimizations are still being tuned.
> - Expect rough edges and occasional bugs.

See the full list of supported hardware and build configurations in [PRESETS.md](PRESETS.md).

## Installation & Usage

### POSIX systems

Run the following command in your terminal:

    curl installama.sh | sh

Launch the server:

    ~/.installama/server -hf unsloth/Qwen3-4B-GGUF:Q4_0

In some scenarios, you may want to skip detection for specific backends.
You can do this by setting environment variables before piping to `sh`:

    curl installama.sh | SKIP_CUDA=1 sh

Available options: `SKIP_CUDA=1`, `SKIP_ROCM=1`, `SKIP_VULKAN=1`.

### Windows

Run the following command in `PowerShell`:

    irm installama.sh | iex

Launch the server:

    & $env:USERPROFILE\installama\server.exe -hf unsloth/Qwen3-4B-GGUF:Q4_0

## Enjoy!

Once the server is running with your chosen model, simply open your browser and navigate to:

　　　　**http://127.0.0.1:8080**

---
If it doesn't work on your system, please [create an issue](https://github.com/angt/installama.sh/issues/new).
