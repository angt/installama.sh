import os
import re
import sys

from huggingface_hub import sync_bucket
import zstandard as zstd

from elftools.elf.elffile import ELFFile
from elftools.elf.dynamic import DynamicSection
import pefile
from macholib.MachO import MachO

from pathlib import Path
from collections import defaultdict
from fnmatch import fnmatch

SKIP_LIBS = [
    "ld-linux-*.so.*",
    "libc.so.*",
    "libm.so.*",
    "libthr.so.*",
    "libdl.so.*",
    "libpthread.so.*",
    "api-ms-*.dll",
    "ADVAPI32.dll",
    "CRYPT32.dll",
    "KERNEL32.dll",
    "WS2_32.dll",
    "Accelerate",
    "CoreFoundation",
    "Foundation",
    "Metal",
    "MetalKit",
    "Security",
    "libSystem.B.dylib",
    "libc++.1.dylib",
    "libobjc.A.dylib",
]

def get_max_symbol_version(elf, sym):
    pattern = re.compile(rf"{re.escape(sym)}_(\d+(?:\.\d+)+)")
    versions = []

    if section := elf.get_section_by_name('.gnu.version_r'):
        for entry in section.iter_versions():
            for item in entry[1] if isinstance(entry, tuple) else getattr(entry, 'aux', []):
                name = getattr(item, 'name', None)
                if name is None and isinstance(item, (tuple, list)):
                    name = next((x for x in item if isinstance(x, (str, bytes))), None)
                if isinstance(name, bytes):
                    name = name.decode('utf-8', errors='ignore')
                if name and (m := pattern.search(name)):
                    versions.append(tuple(map(int, m.group(1).split('.'))))

    return f"{sym} {'.'.join(map(str, max(versions)))}" if versions else None

def analyze_elf(path, name, arch):
    match name:
        case "linux":   interp, sym = "ld-linux", "GLIBC"
        case "freebsd": interp, sym = "ld-elf",   "FBSD"
        case _: raise Exception(f"Unsupported OS: {name}")

    reqs = "None"
    libs = []

    with open(path, 'rb') as f:
        elf = ELFFile(f)

        if str(elf.header['e_machine']).replace('EM_', '').lower() != arch:
            raise Exception(f"Bad arch, expected: {arch}")

        for seg in elf.iter_segments():
            if seg['p_type'] == 'PT_INTERP':
                if interp in seg.get_interp_name():
                    break
                raise Exception(f"OS mismatch, expected: {arch}")

        for section in elf.iter_sections():
            if isinstance(section, DynamicSection):
                for tag in section.iter_tags():
                    if tag.entry.d_tag == 'DT_NEEDED':
                        libs.append(tag.needed)

        if v := get_max_symbol_version(elf, sym):
            reqs = v

    return reqs, libs

def analyze_pe(path, arch):
    libs = []
    pe = pefile.PE(path, fast_load=True)

    match pe.FILE_HEADER.Machine:
        case 0x8664 if arch ==  "x86_64": pass
        case 0xAA64 if arch == "aarch64": pass
        case _: raise Exception(f"Bad arch, expected: {arch}")

    version = 7
    winapi = {
        b"CreateFile2":   8,
        b"VirtualAlloc2": 10,
    }
    pe.parse_data_directories(directories=[
        pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT']
    ])
    for entry in getattr(pe, 'DIRECTORY_ENTRY_IMPORT', []):
        if entry.dll:
            libs.append(entry.dll.decode('utf-8', errors='ignore'))
        for imp in entry.imports:
            if imp.name and imp.name in winapi:
                if winapi[imp.name] > version:
                    version = winapi[imp.name]

    return f"Windows {version}", libs

def analyze_macho(path, arch):
    reqs = "Unknown"
    libs = []

    for header in MachO(path).headers:
        match header.header.cputype:
            case 0x1000007 if arch ==  "x86_64": pass
            case 0x100000C if arch == "aarch64": pass
            case _: continue

        for cmd, payload, data in header.commands:
            if cmd.cmd == 12:
                lib = data.decode('utf-8').strip('\x00')
                libs.append(os.path.basename(lib))
            if cmd.cmd in [0x32, 0x24]:
                version = payload.minos if cmd.cmd == 0x32 else payload.version
                major, minor = version >> 16, (version >> 8) & 0xff
                reqs = f"macOS {major}.{minor}"

        return reqs, libs

    raise Exception(f"Bad arch, expected: {arch}")

def get_backend(files, base):
    dirs = [os.path.dirname(os.path.relpath(f, base)) for f in files]
    parts = os.path.commonpath(dirs).split(os.sep)
    # parts = [arch, os, backend...]
    return os.path.join(*parts[2:]) if len(parts) > 2 else ""

def analyze(path, base):
    parts = os.path.relpath(path, base).split(os.sep)
    arch = parts[0]
    name = parts[1]

    match name:
        case "windows": reqs, libs = analyze_pe(path, arch)
        case "macos":   reqs, libs = analyze_macho(path, arch)
        case _:         reqs, libs = analyze_elf(path, name, arch)

    return name, arch, reqs, tuple(
        lib for lib in sorted(libs)
        if not any(fnmatch(lib, skip) for skip in SKIP_LIBS)
    )

def main():
    if len(sys.argv) == 2:
        if sys.argv[1].startswith('hf://'):
            local_dir = "reqs"
            sync_bucket(sys.argv[1], local_dir)
            with open(os.path.join(local_dir, "latest")) as f:
                local_dir = os.path.join(local_dir, f.read().strip())
        else:
            local_dir = sys.argv[1]
    else:
        local_dir = "output"

    groups = defaultdict(list)
    for src in Path(local_dir).rglob('*.zst'):
        dst = src.with_suffix('')
        with src.open('rb') as fsrc, dst.open('wb') as fdst:
            zstd.ZstdDecompressor().copy_stream(fsrc, fdst)
        if (entry := analyze(str(dst), local_dir)):
            groups[entry].append(str(dst))

    cols = ["Name", "Arch", "Backend", "Version", "Libraries"]
    rows = sorted([
        [
            name,
            f"`{arch}`",
            f"`{get_backend(files, local_dir)}`",
            version,
            " ".join(f"`{lib}`" for lib in libs) or "-"
        ]
        for (name, arch, version, libs), files in groups.items()
    ])
    widths = [max(map(len, x)) for x in zip(*([cols] + rows))]
    header = [[c.ljust(w) for c, w in zip(cols, widths)], ["-" * w for w in widths]]
    rows   = [[r.ljust(w) for r, w in zip(row, widths)] for row in rows]

    with open('REQUIREMENTS.md', 'w', encoding='utf-8') as f:
        f.write("# Supported Systems\n\n")
        for line in header + rows:
            f.write("| " + " | ".join(line) + " |\n")

if __name__ == '__main__':
    main()
