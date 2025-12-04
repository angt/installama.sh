$FEATCODE = "https://github.com/angt/featcode/releases/latest/download"
$UNZSTD   = "https://github.com/angt/unzstd/releases/latest/download"
$REPO     = "https://huggingface.co/datasets/angt/installama.sh/resolve/main"

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
            rm "tmp.zst"
        } else {
            irm $URL -OutFile $FILE
        }
    } catch {
        Die "Failed to download"
    }
}

function ProbeCPU {
    "Probing CPU..."
    Download "featcode.exe" "$FEATCODE/$ARCH-windows-featcode.exe"
    $CONFIG = .\featcode.exe 2>$null
    .\featcode.exe $CONFIG 2>$null | % { "Found: $_" }
    Download "server.exe" "$REPO/$ARCH/windows/cpu/$CONFIG/llama-server.zst"
}

function Main {
    switch ($env:PROCESSOR_ARCHITECTURE) {
        "ARM64" { $ARCH = "aarch64" }
        "AMD64" { $ARCH = "x86_64"  }
        default { Die "Arch not supported" }
    }
    $DIR = Join-Path $env:USERPROFILE "installama"

    rm $DIR -Recurse -Force 2>$null
    md $DIR -Force | Out-Null
    cd $DIR

    ProbeCPU

    if (!(Test-Path "server.exe")) {
        Die "No prebuilt server binary is available for your system." `
            "Please compile llama.cpp from source instead."
    }
    if ($args.Length -gt 0) {
        .\server.exe @args
        exit $LASTEXITCODE
    }
    "Run $DIR\server.exe to launch the llama.cpp server"
}

Main @args
