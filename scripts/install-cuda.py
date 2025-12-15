import sys
import os
import json
from urllib.request import urlopen
import tarfile
import shutil
import platform
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ROOT = Path.cwd() / "deps" / "cuda"
DEST = ROOT.with_suffix(".tmp")

VERSION = os.getenv("CUDA_VERSION", "12.8.1")
URL = "https://developer.download.nvidia.com/compute/cuda/redist"
COMPONENTS = [
    "cuda_nvprune",
    "cuda_nvcc",
    "cuda_cudart",
    "cuda_cccl",
    "libcublas"
]

def detect_arch():
    machine = platform.machine().lower()
    if machine in ["x86_64", "amd64"]:
        return "x86_64"
    if machine in ["aarch64", "arm64"]:
        return "aarch64"
    return machine

def install(args):
    name, file = args

    def members(tar):
        for member in tar:
            parts = Path(member.name).parts
            if len(parts) > 1:
                member.name = str(Path(*parts[1:]))
                yield member

    with urlopen(f"{URL}/{file}") as r:
        with tarfile.open(fileobj=r, mode="r|*") as tar:
            tar.extractall(DEST, members=members(tar), filter='tar')

    return f" - {name}"

def main():
    arch = sys.argv[1] if len(sys.argv) >= 2 else detect_arch()
    arch_map = {
        "x86_64": "linux-x86_64",
        "aarch64": "linux-sbsa"
    }
    platform_key = arch_map.get(arch)

    shutil.rmtree(DEST, ignore_errors=True)
    DEST.mkdir(parents=True)

    print(f"Installing CUDA {VERSION} ({platform_key})...")

    with urlopen(f"{URL}/redistrib_{VERSION}.json") as r:
        manifest = json.load(r)

    tasks = []
    for c in COMPONENTS:
        data = manifest[c]
        name = f"{data['name']} version {data['version']}"
        tasks.append((name, data[platform_key]["relative_path"]))

    with ThreadPoolExecutor(len(tasks)) as pool:
        for res in pool.map(install, tasks):
            print(res)

    DEST.rename(ROOT)
    (ROOT / "lib64").symlink_to("lib")

if __name__ == "__main__":
    main()
