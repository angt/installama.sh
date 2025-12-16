import sys
import os
import json
import time
from urllib.request import urlopen
import tarfile
import shutil
import platform
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import wraps

ROOT = Path.cwd() / "deps" / "cuda"
DEST = ROOT.with_suffix(".tmp")

VERSION = os.getenv("CUDA_VERSION", "12.8.1")
URL = "https://developer.download.nvidia.com/compute/cuda/redist"
COMPONENTS = [
    "libcublas",
    "cuda_cudart",
    "cuda_nvcc",
    "cuda_cccl",
    "cuda_nvprune",
]

def retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for i in reversed(range(5)):
            try:
                return func(*args, **kwargs)
            except Exception:
                if not i:
                    raise
                time.sleep(10)
    return wrapper

def detect_arch():
    machine = platform.machine().lower()
    if machine in ["x86_64", "amd64"]:
        return "x86_64"
    if machine in ["aarch64", "arm64"]:
        return "aarch64"
    return machine

@retry
def install(args):
    name, file = args

    def members(tar):
        for member in tar:
            parts = Path(member.name).parts
            if len(parts) > 1:
                member.name = str(Path(*parts[1:]))
                yield member

    with urlopen(f"{URL}/{file}", timeout=60) as r:
        with tarfile.open(fileobj=r, mode="r|*") as tar:
            tar.extractall(DEST, members=members(tar), filter='tar')

    return f" - {name}"

@retry
def download_manifest():
    with urlopen(f"{URL}/redistrib_{VERSION}.json", timeout=60) as r:
        return json.load(r)

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
    manifest = download_manifest()

    tasks = []
    for c in COMPONENTS:
        data = manifest[c]
        name = f"{data['name']} version {data['version']}"
        tasks.append((name, data[platform_key]["relative_path"]))

    with ThreadPoolExecutor(2) as pool:
        futures = [pool.submit(install, task) for task in tasks]
        for f in as_completed(futures):
            print(f.result())

    DEST.rename(ROOT)
    (ROOT / "lib64").symlink_to("lib")

if __name__ == "__main__":
    main()
