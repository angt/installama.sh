# Supported Systems

| Name    | Arch      | Backend        | Version     | Libraries                                              |
| ------- | --------- | -------------- | ----------- | ------------------------------------------------------ |
| freebsd | `aarch64` | `cpu`          | FBSD 1.7    | -                                                      |
| freebsd | `x86_64`  | `cpu`          | FBSD 1.7    | -                                                      |
| linux   | `aarch64` | `cpu`          | None        | -                                                      |
| linux   | `aarch64` | `cuda/probe`   | GLIBC 2.34  | -                                                      |
| linux   | `aarch64` | `cuda`         | GLIBC 2.35  | `libcuda.so.1`                                         |
| linux   | `aarch64` | `vulkan/probe` | GLIBC 2.17  | `libvulkan.so.1`                                       |
| linux   | `aarch64` | `vulkan`       | GLIBC 2.27  | `libvulkan.so.1`                                       |
| linux   | `x86_64`  | `cpu`          | None        | -                                                      |
| linux   | `x86_64`  | `cuda/probe`   | GLIBC 2.34  | -                                                      |
| linux   | `x86_64`  | `cuda`         | GLIBC 2.35  | `libcuda.so.1`                                         |
| linux   | `x86_64`  | `rocm`         | GLIBC 2.35  | `libamdhip64.so.7` `libhipblas.so.3` `librocblas.so.5` |
| linux   | `x86_64`  | `vulkan/probe` | GLIBC 2.2.5 | `libvulkan.so.1`                                       |
| linux   | `x86_64`  | `vulkan`       | GLIBC 2.27  | `libvulkan.so.1`                                       |
| macos   | `aarch64` | `metal/m3`     | macOS 14.0  | -                                                      |
| macos   | `aarch64` | `metal/m4`     | macOS 15.0  | -                                                      |
| macos   | `aarch64` | `metal/m5`     | macOS 16.0  | -                                                      |
| macos   | `aarch64` | `metal`        | macOS 13.3  | -                                                      |
| windows | `aarch64` | `cpu`          | Windows 8   | -                                                      |
| windows | `aarch64` | `vulkan/probe` | Windows 7   | `vulkan-1.dll`                                         |
| windows | `aarch64` | `vulkan`       | Windows 8   | `vulkan-1.dll`                                         |
| windows | `x86_64`  | `cpu`          | Windows 8   | -                                                      |
| windows | `x86_64`  | `vulkan/probe` | Windows 7   | `vulkan-1.dll`                                         |
| windows | `x86_64`  | `vulkan`       | Windows 8   | `vulkan-1.dll`                                         |
