import os
import sys
import subprocess
from collections import defaultdict
import json
from ortools.sat.python import cp_model

ROCM_ARCHS = [
    "803",  "900",  "906",  "908",  "90a",  "942",
    "1010", "1011", "1030", "1032", "1100", "1101",
    "1102", "1151", "1200", "1201"
]
CUDA_ARCHS = ["50", "61", "70", "75", "80", "86", "89"]
METAL_ARCHS = {1: "13.3", 2: "13.3", 3: "14.0", 4: "15.0"}
CPU_ARCHS = {}

def generate_features(features, implications):
    m = cp_model.CpModel()
    v = {f: m.NewBoolVar(f) for f in features}

    for child, parent in implications:
        m.Add(v[child] <= v[parent])

    class CB(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(self):
            ret.append([f for f in features if self.Value(v[f])])

    ret = []
    s = cp_model.CpSolver()
    s.SearchForAllSolutions(m, CB())
    return ret

def generate_aarch64_features():
    features = [
        'fp16',
        'dotprod',
        'i8mm',
        'sve',
        'sve2', # only to detect v9a
        'sme',
    ]
    implications = [
        # strict
        ('sve',  'fp16'   ),
        ('sme',  'fp16'   ),
        ('sve2', 'sve'    ),
        # observed so far
        ('sme',  'fp16'   ),
        ('i8mm', 'dotprod'),
        ('sve2', 'dotprod'),
        ('sme',  'dotprod'),
        ('sme',  'i8mm'   ),
    ]
    return generate_features(features, implications)

def generate_x86_64_features():
    features = [
        'avx',
        'f16c',
        'fma',
        'avx2',
        'bmi2',
        'avxvnni',
        'avxvnniint8',
        'avx512f',
        'avx512vl',
        'avx512bw',
        'avx512dq',
        'avx512cd',
        'avx512vnni',
        'avx512vbmi',
        'avx512bf16',
        'amx-tile',
        'amx-int8',
        'amx-bf16',
    ]
    implications = [
        # strict
        ('f16c',        'avx'       ),
        ('fma',         'avx'       ),
        ('avx2',        'avx'       ),
        ('avxvnni',     'avx2'      ),
        ('avxvnniint8', 'avx2'      ),
        ('avx512f',     'avx2'      ),
        ('avx512f',     'f16c'      ),
        ('avx512f',     'fma'       ),
        ('avx512vl',    'avx512f'   ),
        ('avx512bw',    'avx512f'   ),
        ('avx512dq',    'avx512f'   ),
        ('avx512cd',    'avx512f'   ),
        ('avx512vnni',  'avx512f'   ),
        ('avx512vbmi',  'avx512bw'  ),
        ('avx512bf16',  'avx512bw'  ),
        ('amx-int8',    'amx-tile'  ),
        ('amx-bf16',    'amx-tile'  ),
        # observed so far
        ('fma',         'f16c'      ),
        ('avx2',        'bmi2'      ),
        ('avx2',        'fma'       ),
        ('bmi2',        'avx2'      ),
        ('avxvnniint8', 'avxvnni'   ),
        ('avx512f',     'avx512cd'  ),
        ('avx512bw',    'avx512dq'  ),
        ('avx512dq',    'avx512vl'  ),
        ('avx512vl',    'avx512bw'  ),
        ('avx512vnni',  'avx512bw'  ),
        ('amx-tile',    'avxvnni'   ),
        ('amx-tile',    'avx512vnni'),
        ('amx-tile',    'avx512vbmi'),
        ('amx-tile',    'avx512bf16'),
        ('amx-tile',    'amx-int8'  ),
        ('amx-tile',    'amx-bf16'  ),
    ]
    return generate_features(features, implications)

def select_min_aarch64_arch(features):
    march = {
        'sve2':    'generic+v9a',
        'sme':     'generic+v8_7a', # only because of apple-m4
        'i8mm':    'generic+v8_2a',
        'sve':     'generic+v8_2a',
        'dotprod': 'generic+v8_2a',
        'fp16':    'generic+v8_2a',
    }
    return next((march[f] for f in march if f in set(features)), 'generic')

def select_min_x86_64_arch(features):
    march = {
        'amx-bf16':    'x86_64_v4',
        'amx-int8':    'x86_64_v4',
        'amx-tile':    'x86_64_v4',
        'avx512bf16':  'x86_64_v4',
        'avx512vbmi':  'x86_64_v4',
        'avx512vnni':  'x86_64_v4',
        'avx512bw':    'x86_64_v4',
        'avx512dq':    'x86_64_v4',
        'avx512vl':    'x86_64_v4',
        'avx512cd':    'x86_64_v3',
        'avx512f':     'x86_64_v3',
        'avxvnniint8': 'x86_64_v3',
        'avxvnni':     'x86_64_v3',
        'bmi2':        'x86_64_v3',
        'avx2':        'x86_64_v3',
        'fma':         'x86_64_v2',
        'f16c':        'x86_64_v2',
        'avx':         'x86_64_v2',
    }
    return next((march[f] for f in march if f in set(features)), 'x86_64')

def featcode(arch, features):
    args = ['+' + feat for feat in features]
    result = subprocess.run(
        ['featcode', '+'] + ['+' + feat for feat in features],
        env={**os.environ, 'FEATCODE_ARCH': arch},
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()

def generate_aarch64_flags(features):
    mcpu = '+'.join([
        select_min_aarch64_arch(features),
        *('fullfp16' if f == 'fp16' else f for f in features)
    ])
    return f"-mcpu={mcpu}"

def generate_x86_64_flags(features):
    arch = select_min_x86_64_arch(features)

    if 'avx512f' in features:
        features += ['evex512']

    flags = ' '.join([
        f"-march={arch}",
        *(f"-m{feat}" for feat in features),
    ])
    return flags

def generate_cpu_archs():
    CPU_ARCHS['aarch64'] = {}

    for features in generate_aarch64_features():
        name = featcode('aarch64', features)
        flags = generate_aarch64_flags(features)
        CPU_ARCHS['aarch64'][name] = flags

    CPU_ARCHS['x86_64'] = {}

    for features in generate_x86_64_features():
        name = featcode('x86_64', features)
        flags = generate_x86_64_flags(features)
        CPU_ARCHS['x86_64'][name] = flags

def generate_presets(name, processor, backend, toolchain, configs):
    name_map = {
        "Linux":   "linux",
        "FreeBSD": "freebsd",
        "Darwin":  "macos",
    }
    processor_map = {
        "x86_64":  "x86_64",
        "amd64":   "x86_64",
        "AMD64":   "x86_64",
        "aarch64": "aarch64",
        "arm64":   "aarch64",
        "ARM64":   "aarch64",
    }
    osname = name_map[name]
    arch = processor_map[processor]

    configure = []
    build = []
    workflow = []

    for config_name, config_cache in configs:
        preset_name = f"{arch}-{osname}-{backend}-{config_name}"
        preset_path = f"{arch}/{osname}/{backend}/{config_name}"
        configure.append({
            "name": preset_name,
            "binaryDir": "build/${presetName}",
            "cacheVariables": {
                "INSTALLAMA_DIR": f"${{sourceDir}}/output/{preset_path}",
            } | config_cache,
            "environment": {
                "CMAKE_SYSTEM_NAME": name,
                "CMAKE_SYSTEM_PROCESSOR": processor
            },
            "toolchainFile": toolchain,
            "generator": "Ninja",
        })
        build.append({
            "name": preset_name,
            "configurePreset": preset_name,
            "jobs": 0,
            "targets": ["installama"],
        })
        workflow.append({
            "name": preset_name,
            "steps": [
                {"type": "configure", "name": preset_name},
                {"type": "build", "name": preset_name}
            ]
        })

    return configure, build, workflow

def generate_cpu_presets(system_name, processor):
    configs = []
    for name, flags in CPU_ARCHS[processor].items():
        cache = {
            "INSTALLAMA_FLAGS": flags,
        }
        configs.append((name, cache))

    return generate_presets(
        name      = system_name,
        processor = processor,
        backend   = 'cpu',
        toolchain = 'toolchains/cross.cmake',
        configs   = configs,
    )

def generate_aarch64_linux_cpu_presets():
    return generate_cpu_presets('Linux', 'aarch64')

def generate_x86_64_linux_cpu_presets():
    return generate_cpu_presets('Linux', 'x86_64')

def generate_aarch64_freebsd_cpu_presets():
    return generate_cpu_presets('FreeBSD', 'aarch64')

def generate_x86_64_freebsd_cpu_presets():
    return generate_cpu_presets('FreeBSD', 'x86_64')

def rocwmma(arch):
    return arch.startswith(('11', '12')) or (arch.startswith('9') and arch not in {'900', '906'})

def generate_x86_64_linux_rocm_presets():
    configs = []
    for arch in ROCM_ARCHS:
        name = f"gfx{arch}"
        cache = {
            "GGML_HIP": "ON",
            "GGML_HIP_ROCWMMA_FATTN": "ON" if rocwmma(arch) else "OFF",
            "CMAKE_HIP_ARCHITECTURES": name,
        }
        configs.append((name, cache))

    return generate_presets(
        name      = 'Linux',
        processor = 'x86_64',
        backend   = 'rocm',
        toolchain = 'toolchains/rocm.cmake',
        configs   = configs,
    )

def generate_x86_64_linux_rocm_probe_preset():
    configs = []
    name = "probe"
    cache = {
        "INSTALLAMA_PROBE": "rocm",
    }
    configs.append((name, cache))

    return generate_presets(
        name      = 'Linux',
        processor = 'x86_64',
        backend   = 'rocm',
        toolchain = 'toolchains/rocm.cmake',
        configs   = configs,
    )

def generate_x86_64_linux_cuda_presets():
    configs = []
    for arch in CUDA_ARCHS:
        name = arch
        cache = {
            "GGML_CUDA": "ON",
            "GGML_STATIC": "ON",
            "CMAKE_CUDA_ARCHITECTURES": f"{arch}-real",
        }
        configs.append((name, cache))

    return generate_presets(
        name      = 'Linux',
        processor = 'x86_64',
        backend   = 'cuda',
        toolchain = 'toolchains/cuda.cmake',
        configs   = configs,
    )

def generate_x86_64_linux_cuda_probe_preset():
    configs = []
    name = "probe"
    cache = {
        "INSTALLAMA_PROBE": "cuda",
        "INSTALLAMA_PROBE_ARCHS": ",".join(CUDA_ARCHS),
        "CMAKE_CUDA_ARCHITECTURES": ";".join(CUDA_ARCHS), # useless
    }
    configs.append((name, cache))

    return generate_presets(
        name      = 'Linux',
        processor = 'x86_64',
        backend   = 'cuda',
        toolchain = 'toolchains/cuda.cmake',
        configs   = configs,
    )

def generate_linux_vulkan_presets(processor):
    configs = []
    for name, flags in CPU_ARCHS[processor].items():
        cache = {
            "INSTALLAMA_FLAGS": flags,
            "GGML_VULKAN": "ON",
        }
        configs.append((name, cache))

    return generate_presets(
        name      = 'Linux',
        processor = processor,
        backend   = 'vulkan',
        toolchain = 'toolchains/vulkan.cmake',
        configs   = configs,
    )

def generate_linux_vulkan_probe_preset(processor):
    configs = []
    name = "probe"
    cache = {
        "INSTALLAMA_PROBE": "vulkan",
    }
    configs.append((name, cache))

    return generate_presets(
        name      = 'Linux',
        processor = processor,
        backend   = 'vulkan',
        toolchain = 'toolchains/vulkan.cmake',
        configs   = configs,
    )

def generate_x86_64_linux_vulkan_presets():
    return generate_linux_vulkan_presets('x86_64')

def generate_x86_64_linux_vulkan_probe_preset():
    return generate_linux_vulkan_probe_preset('x86_64')

def generate_aarch64_linux_vulkan_presets():
    return generate_linux_vulkan_presets('aarch64')

def generate_aarch64_linux_vulkan_probe_preset():
    return generate_linux_vulkan_probe_preset('aarch64')

def metal_use_bf16(cpu):
    return cpu >= 3

def generate_metal_presets():
    configs = []
    for cpu, osx in METAL_ARCHS.items():
        name = f"m{cpu}"
        cache = {
            "GGML_METAL": "ON",
            "GGML_METAL_EMBED_LIBRARY": "ON",
            "GGML_METAL_USE_BF16": "ON" if metal_use_bf16(cpu) else "OFF",
            "CMAKE_OSX_ARCHITECTURES": "arm64",
            "CMAKE_OSX_DEPLOYMENT_TARGET": osx,
            "INSTALLAMA_FLAGS": f"-mcpu=apple-m{cpu}"
        }
        configs.append((name, cache))

    return generate_presets(
        name      = 'Darwin',
        processor = 'arm64',
        backend   = 'metal',
        toolchain = 'toolchains/base.cmake',
        configs   = configs
    )

def format_x86_64_features(flags):
    feats = []
    arch = ""
    parts = flags.split()
    for p in parts:
        if p.startswith("-march="):
            arch = p.replace("-march=", "")
        elif p.startswith("-m"):
            feats.append(p[2:])
    return arch, feats

def format_aarch64_features(flags):
    feats = []
    arch = ""
    parts = flags.replace("-mcpu=", "").split("+")
    arch_map = {
        "v8_2a":   "ARMv8.2-a",
        "v8_7a":   "ARMv8.7-a",
        "v9a":     "ARMv9-a",
        "generic": "ARMv8.0-a"
    }
    for p in parts:
        if p in arch_map:
            arch = arch_map[p]
        else:
            feats.append(p)
    return arch, feats

def generate_report():
    lines = []
    lines.append("# Build Presets Reference\n")
    lines.append("## CPU\n")

    lines.append("### AArch64 (ARM64)\n")
    lines.append("| Code | Architecture | Features |")
    lines.append("|---|---|---|")
    for code, flags in CPU_ARCHS['aarch64'].items():
        arch, feats = format_aarch64_features(flags)
        feats = " ".join(f"`{f}`" for f in feats) if feats else "-"
        lines.append(f"| `{code}` | **{arch}** | {feats} |")
    lines.append("\n")

    lines.append("### x86_64 (Intel/AMD)\n")
    lines.append("| Code | Architecture | Features |")
    lines.append("|---|---|---|")
    for code, flags in CPU_ARCHS['x86_64'].items():
        arch, feats = format_x86_64_features(flags)
        feats = " ".join(f"`{f}`" for f in feats) if feats else "-"
        lines.append(f"| `{code}` | **{arch}** | {feats} |")
    lines.append("\n")

    lines.append("## GPU\n")

    lines.append("### CUDA (NVIDIA)\n")
    cuda_list = " ".join(f"`{a}`" for a in CUDA_ARCHS)
    lines.append(f"- **Supported Architectures:** {cuda_list}")
    lines.append("\n")

    lines.append("### ROCm (AMD)\n")
    lines.append("| Suffix | Features |")
    lines.append("|---|---|")
    for arch in ROCM_ARCHS:
        feat = "**ROCWMMA** + FlashAttn" if rocwmma(arch) else "-"
        lines.append(f"| `gfx{arch}` | {feat} |")
    lines.append("\n")

    lines.append("### Metal (Apple Silicon)\n")
    lines.append("| Suffix | Chip | macOS | Features |")
    lines.append("|---|---|---|---|")
    for cpu, osx in METAL_ARCHS.items():
        feat = "**BF16**" if metal_use_bf16(cpu) else "-"
        lines.append(f"| `m{cpu}` | Apple **M{cpu}** | {osx}+ | {feat} |")
    lines.append("\n")

    return "\n".join(lines)

def main():
    generate_cpu_archs()

    generators = [
        generate_aarch64_freebsd_cpu_presets,
        generate_x86_64_freebsd_cpu_presets,
        generate_aarch64_linux_cpu_presets,
        generate_x86_64_linux_cpu_presets,
        generate_x86_64_linux_rocm_presets,
        generate_x86_64_linux_rocm_probe_preset,
        generate_x86_64_linux_cuda_presets,
        generate_x86_64_linux_cuda_probe_preset,
        generate_x86_64_linux_vulkan_presets,
        generate_x86_64_linux_vulkan_probe_preset,
        generate_aarch64_linux_vulkan_presets,
        generate_aarch64_linux_vulkan_probe_preset,
        generate_metal_presets,
    ]
    data = {
        "version": 7,
        "configurePresets": [],
        "buildPresets": [],
        "workflowPresets": []
    }
    for gen in generators:
        c, b, w = gen()
        data["configurePresets"].extend(c)
        data["buildPresets"].extend(b)
        data["workflowPresets"].extend(w)

    with open("CMakePresets.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    report = generate_report()

    with open("PRESETS.md", "w", encoding="utf-8") as f:
        f.write(report)

if __name__ == "__main__":
    main()
