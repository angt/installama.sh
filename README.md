# `installama.sh`

_Instantly install llama.cpp._

`installama.sh` is a simple script that downloads and sets up a prebuilt `llama` binary for your system.
It automatically detects your OS, architecture, and GPU capabilities, so you can start using `llama.cpp` in seconds.

> [!IMPORTANT]
> **`installama.sh` is now an official `llama.cpp` package!** 🎉
>
> The project has officially migrated to the `ggml-org` ecosystem.
> Check out the new repository at [github.com/ggml-org/llama-install.sh](https://github.com/ggml-org/llama-install.sh) or visit [llama.app](https://llama.app).

## Features

- Supported architectures: `x86_64`, `aarch64`.
- Supported OS: `Linux`, `macOS`, `FreeBSD`, `Windows`.
- **Automatic detection** for **CPU acceleration**.
- **Automatic detection** for **GPU acceleration**: `CUDA`, `ROCm`, `Vulkan`, `Metal`.
- Builds are kept as **lightweight** as possible without compromising performance.

See the full list of supported hardware and build configurations in [PRESETS.md](PRESETS.md).
Check [REQUIREMENTS.md](REQUIREMENTS.md) for the detailed requirements, including minimum OS versions and runtime library dependencies.

## Installation & Usage

### POSIX systems

Run the following command in your terminal:

    curl https://installama.sh | sh

Launch the server:

    ~/.installama/llama serve -hf unsloth/Qwen3-4B-GGUF:Q4_0

In some scenarios, you may want to skip detection for specific backends.
You can do this by setting environment variables before piping to `sh`:

    curl https://installama.sh | SKIP_CUDA=1 sh

Available options: `SKIP_CUDA=1`, `SKIP_ROCM=1`, `SKIP_VULKAN=1`.

### Windows

Run the following command in `PowerShell`:

    irm https://installama.sh | iex

Launch the server:

    llama.exe serve -hf unsloth/Qwen3-4B-GGUF:Q4_0

## Enjoy!

Once the server is running with your chosen model, simply open your browser and navigate to:

　　　　**http://127.0.0.1:8080**

---
If it doesn't work on your system, please [create an issue](https://github.com/angt/installama.sh/issues/new).
