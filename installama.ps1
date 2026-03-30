$REPO = "https://huggingface.co/buckets/angt/installama/resolve"

function Die {
    param([string[]]$Messages)
    $Messages | % { [Console]::Error.WriteLine($_) }
    exit 111
}

function Download {
    param($FILE, $URL)
    if (Test-Path $FILE) {
        return
    }
    "Downloading $FILE..."
    try {
        if ($URL -like "*.zst") {
            Download "unzstd.exe" "$ARCH/windows/unzstd.exe"
            Invoke-RestMethod "$REPO/$VERSION/$URL" -OutFile "tmp.zst"
            Start-Process -FilePath ".\unzstd.exe" -RedirectStandardInput "tmp.zst" -RedirectStandardOutput $FILE -NoNewWindow -Wait
            Remove-Item "tmp.zst"
        } else {
            Invoke-RestMethod "$REPO/$VERSION/$URL" -OutFile $FILE
        }
    } catch {
        Die "Failed to download"
    }
}

function ProbeVulkan {
    if ($env:SKIP_VULKAN) { return }
    "Probing Vulkan..."
    Download "vulkan-probe.exe" "$ARCH/windows/vulkan/probe/probe.zst"
    Download "featcode.exe" "$ARCH/windows/featcode.exe"
    .\vulkan-probe.exe 2>$null
    if ($LASTEXITCODE) { return }
    $CONFIG = .\featcode.exe 2>$null
    .\featcode.exe $CONFIG 2>$null | % { "Found: $_" }
    Download "server.exe" "$ARCH/windows/vulkan/$CONFIG/llama-server.zst"
}

function ProbeCPU {
    "Probing CPU..."
    Download "featcode.exe" "$ARCH/windows/featcode.exe"
    $CONFIG = .\featcode.exe 2>$null
    .\featcode.exe $CONFIG 2>$null | % { "Found: $_" }
    Download "server.exe" "$ARCH/windows/cpu/$CONFIG/llama-server.zst"
}

function Main {
    switch ($env:PROCESSOR_ARCHITECTURE) {
        "ARM64" { $ARCH = "aarch64" }
        "AMD64" { $ARCH = "x86_64"  }
        default { Die "Arch not supported" }
    }

    $VERSION = Invoke-RestMethod "$REPO/latest"
    if (!$VERSION) { Die "No version found" }
    "Version: $VERSION"

    $DIR = Join-Path $env:USERPROFILE "installama"

    Remove-Item $DIR -Recurse -Force 2>$null
    New-Item -Path $DIR -Force -ItemType "Directory" | Out-Null
    Push-Location $DIR

    try {
        if (!(Test-Path "server.exe")) { ProbeVulkan }
        if (!(Test-Path "server.exe")) { ProbeCPU    }
        if (!(Test-Path "server.exe")) {
            Die "No prebuilt server binary is available for your system." `
                "Please compile llama.cpp from source instead."
        }
    }
    finally {
        Pop-Location
    }
    if ($args.Length -gt 0) {
        & "$DIR\server.exe" @args
        exit $LASTEXITCODE
    }
    "Run $DIR\server.exe to launch the llama.cpp server"
}

Main @args
