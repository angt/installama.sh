# Build Presets Reference

## CPU

### AArch64 (ARM64)

| Code | Architecture | Features |
|---|---|---|
| `yk` | **ARMv8.2-a** | `fullfp16` `dotprod` `i8mm` `sve` |
| `uk` | **ARMv8.2-a** | `fullfp16` `dotprod` `sve` |
| `sk` | **ARMv8.2-a** | `fullfp16` `sve` |
| `lk` | **ARMv8.2-a** | `fullfp16` |
| `nk` | **ARMv8.2-a** | `fullfp16` `dotprod` |
| `rk` | **ARMv8.2-a** | `fullfp16` `dotprod` `i8mm` |
| `ql` | **ARMv9-a** | `fullfp16` `dotprod` `i8mm` `sve` `sve2` |
| `ml` | **ARMv9-a** | `fullfp16` `dotprod` `sve` `sve2` |
| `qn` | **ARMv9-a** | `fullfp16` `dotprod` `i8mm` `sve` `sve2` `sme` |
| `ym` | **ARMv8.7-a** | `fullfp16` `dotprod` `i8mm` `sve` `sme` |
| `qm` | **ARMv8.7-a** | `fullfp16` `dotprod` `i8mm` `sme` |
| `qk` | **ARMv8.2-a** | `dotprod` `i8mm` |
| `mk` | **ARMv8.2-a** | `dotprod` |
| `kk` | **ARMv8.0-a** | - |


### x86_64 (Intel/AMD)

| Code | Architecture | Features |
|---|---|---|
| `knxrk` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avxvnni` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512vnni` `avx512vbmi` `avx512bf16` `evex512` |
| `klxrk` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512vnni` `avx512vbmi` `avx512bf16` `evex512` |
| `krxrk` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avxvnni` `avxvnniint8` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512vnni` `avx512vbmi` `avx512bf16` `evex512` |
| `krxqk` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avxvnni` `avxvnniint8` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512vbmi` `avx512bf16` `evex512` |
| `knxqk` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avxvnni` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512vbmi` `avx512bf16` `evex512` |
| `klxqk` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512vbmi` `avx512bf16` `evex512` |
| `klxok` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512bf16` `evex512` |
| `knxok` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avxvnni` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512bf16` `evex512` |
| `krxok` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avxvnni` `avxvnniint8` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512bf16` `evex512` |
| `krxpk` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avxvnni` `avxvnniint8` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512vnni` `avx512bf16` `evex512` |
| `knxpk` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avxvnni` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512vnni` `avx512bf16` `evex512` |
| `klxpk` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512vnni` `avx512bf16` `evex512` |
| `klzlk` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512vnni` `evex512` |
| `knzlk` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avxvnni` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512vnni` `evex512` |
| `krzlk` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avxvnni` `avxvnniint8` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512vnni` `evex512` |
| `krzkk` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avxvnni` `avxvnniint8` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `evex512` |
| `knzkk` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avxvnni` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `evex512` |
| `klzkk` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `evex512` |
| `klokk` | **x86_64_v3** | `avx` `f16c` `fma` `avx2` `bmi2` `avx512f` `avx512cd` `evex512` |
| `knokk` | **x86_64_v3** | `avx` `f16c` `fma` `avx2` `bmi2` `avxvnni` `avx512f` `avx512cd` `evex512` |
| `krokk` | **x86_64_v3** | `avx` `f16c` `fma` `avx2` `bmi2` `avxvnni` `avxvnniint8` `avx512f` `avx512cd` `evex512` |
| `qrkkk` | **x86_64_v3** | `avx` `f16c` `fma` `avx2` `bmi2` `avxvnni` `avxvnniint8` |
| `qnkkk` | **x86_64_v3** | `avx` `f16c` `fma` `avx2` `bmi2` `avxvnni` |
| `ylkkk` | **x86_64_v3** | `avx` `f16c` `fma` `avx2` `bmi2` |
| `qkkkk` | **x86_64_v2** | `avx` `f16c` `fma` |
| `mkkkk` | **x86_64_v2** | `avx` `f16c` |
| `lkkkk` | **x86_64_v2** | `avx` |
| `klxmk` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512vbmi` `evex512` |
| `knxmk` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avxvnni` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512vbmi` `evex512` |
| `krxmk` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avxvnni` `avxvnniint8` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512vbmi` `evex512` |
| `krxnk` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avxvnni` `avxvnniint8` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512vnni` `avx512vbmi` `evex512` |
| `knxnk` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avxvnni` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512vnni` `avx512vbmi` `evex512` |
| `klxnk` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512vnni` `avx512vbmi` `evex512` |
| `knxrn` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avxvnni` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512vnni` `avx512vbmi` `avx512bf16` `amx-tile` `amx-int8` `amx-bf16` `evex512` |
| `krxrn` | **x86_64_v4** | `avx` `f16c` `fma` `avx2` `bmi2` `avxvnni` `avxvnniint8` `avx512f` `avx512vl` `avx512bw` `avx512dq` `avx512cd` `avx512vnni` `avx512vbmi` `avx512bf16` `amx-tile` `amx-int8` `amx-bf16` `evex512` |
| `kkkkk` | **x86_64** | - |


## GPU

### CUDA (NVIDIA)

- **Supported Architectures:** `50` `61` `70` `75` `80` `86` `89`


### ROCm (AMD)

| Suffix | Features |
|---|---|
| `gfx803` | - |
| `gfx900` | - |
| `gfx906` | - |
| `gfx908` | ROCWMMA+FlashAttn |
| `gfx90a` | ROCWMMA+FlashAttn |
| `gfx942` | ROCWMMA+FlashAttn |
| `gfx1010` | - |
| `gfx1011` | - |
| `gfx1030` | - |
| `gfx1032` | - |
| `gfx1100` | ROCWMMA+FlashAttn |
| `gfx1101` | ROCWMMA+FlashAttn |
| `gfx1102` | ROCWMMA+FlashAttn |
| `gfx1151` | ROCWMMA+FlashAttn |
| `gfx1200` | ROCWMMA+FlashAttn |
| `gfx1201` | ROCWMMA+FlashAttn |


### Metal (Apple Silicon)

| Suffix | Chip | macOS | Features |
|---|---|---|---|
| `m1` | Apple M1 | 13.3+ | - |
| `m2` | Apple M2 | 13.3+ | - |
| `m3` | Apple M3 | 14.0+ | BF16 |
| `m4` | Apple M4 | 15.0+ | BF16 |

