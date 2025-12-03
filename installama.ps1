$FEATCODE = "https://github.com/angt/featcode/releases/latest/download"
$UNZSTD = "https://github.com/angt/unzstd/releases/latest/download"
$REPO = "https://huggingface.co/datasets/angt/installama.sh/resolve/main"

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
            Download "unzstd.exe" "$UNZSTD/$ARCH-windows-unzstd.exe"
            irm $URL -OutFile "tmp.zst"
            Start-Process -FilePath ".\unzstd.exe" -RedirectStandardInput "tmp.zst" -RedirectStandardOutput $FILE -NoNewWindow -Wait
            Remove-Item "tmp.zst"
        } else {
            irm $URL -OutFile $FILE
        }
    } catch {
        Die "Failed to download"
    }
}

function LlamaServerCpu {
    "Probing CPU..."
    Download "featcode.exe" "$FEATCODE/$ARCH-windows-featcode.exe"
    $CONFIG = & .\featcode.exe 2>$null
    .\featcode.exe $CONFIG 2>$null | % { "Found: $_" }
    Download "llama-server.exe" "$REPO/$ARCH/windows/cpu/$CONFIG/llama-server.zst"
}

function Main {
    switch ($env:PROCESSOR_ARCHITECTURE) {
        "ARM64" { $ARCH = "aarch64" }
        "AMD64" { $ARCH = "x86_64"  }
        default { Die "Arch not supported" }
    }
    $DIR = Join-Path $env:USERPROFILE "installama"

    if (Test-Path $DIR) {
        Remove-Item -Path $DIR -Recurse -Force
    }
    New-Item -Path $DIR -ItemType Directory -Force | Out-Null
    Set-Location $DIR

    LlamaServerCpu

    if (!(Test-Path "llama-server.exe")) {
        Die "No prebuilt llama-server binary is available for your system." `
            "Please compile llama.cpp from source instead."
    }
    if ($args.Length -gt 0) {
        & ".\llama-server.exe" @args
        exit $LASTEXITCODE
    }
    "Run $DIR/llama-server.exe to launch the llama.cpp server"
}

Main @args
