FEATCODE="https://github.com/angt/featcode/releases/latest/download"
UNZSTD="https://github.com/angt/unzstd/releases/latest/download"
REPO="https://huggingface.co/datasets/angt/installama.sh/resolve/main"

die() {
	printf "%s\n" "$@" >&2
	exit 111
}

check_bin() {
	command -v "$1" >/dev/null 2>/dev/null
}

dl_bin() {
	[ -x "$1" ] && return
	check_bin curl || die "Please install curl"
	printf "Downloading %s...\n" "$1"
	case "$2" in
	(*.zst) curl -fsSL "$2" | unzstd ;;
	(*)     curl -fsSL "$2" ;;
	esac > "$1.tmp" 2>/dev/null &&
	chmod +x "$1.tmp" && mv "$1.tmp" "$1" && return
	printf "Failed to download\n" >&2
	return 1
}

unzstd() (
	command -v zstd >/dev/null 2>/dev/null && exec zstd -d
	dl_bin unzstd "$UNZSTD/$ARCH-$OS-unzstd"
	exec ./unzstd
)

llama_server_cuda() {
	[ -z "$SKIP_CUDA" ] && printf "Probing CUDA...\n" &&
	dl_bin cuda-probe "$REPO/$ARCH/$OS/cuda/probe/probe.zst" &&
	CONFIG=$(./cuda-probe 2>/dev/null) &&
	printf "Found: %s\n" "$CONFIG" &&
	dl_bin llama-server "$REPO/$ARCH/$OS/cuda/$CONFIG/llama-server.zst"
}

llama_server_rocm() {
	[ -z "$SKIP_ROCM" ] && printf "Probing ROCm...\n" &&
	dl_bin rocm-probe "$REPO/$ARCH/$OS/rocm/probe/probe.zst" &&
	CONFIG=$(./rocm-probe 2>/dev/null) &&
	printf "Found: %s\n" "$CONFIG" &&
	dl_bin llama-server "$REPO/$ARCH/$OS/rocm/$CONFIG/llama-server.zst"
}

llama_server_cpu() {
	printf "Probing CPU...\n" &&
	dl_bin featcode "$FEATCODE/$ARCH-$OS-featcode" &&
	CONFIG=$(./featcode 2>/dev/null) &&
	for F in $(./featcode "$CONFIG"); do printf "Found: %s\n" "$F"; done &&
	dl_bin llama-server "$REPO/$ARCH/$OS/cpu/$CONFIG/llama-server.zst"
}

llama_server_metal() {
	printf "Probing Metal...\n" &&
	CONFIG=$(sysctl -n machdep.cpu.brand_string 2>/dev/null | grep -o "Apple M[1-4]") &&
	CONFIG=m${CONFIG##*M} &&
	printf "Found: %s\n" "$CONFIG" &&
	dl_bin llama-server "$REPO/$ARCH/$OS/metal/$CONFIG/llama-server.zst"
}

main() {
	case "$(uname -m)" in
	(arm64|aarch64) ARCH=aarch64 ;;
	(amd64|x86_64)  ARCH=x86_64  ;;
	(*) die "Arch not supported"
	esac

	case "$(uname -s)" in
	(Linux)   OS=linux ;;
	(FreeBSD) OS=freebsd ;;
	(Darwin)  OS=macos ;;
	(*) die "OS not supported"
	esac

	[ "$HOME" ] || die "No HOME, please check your OS"

	rm -rf ~/.installama
	mkdir -p ~/.installama
	cd ~/.installama || exit 1

	case "$OS" in
	(macos)   [ -x llama-server ] || llama_server_metal ;;
	(linux)   [ -x llama-server ] || llama_server_cuda
	          [ -x llama-server ] || llama_server_rocm
	          [ -x llama-server ] || llama_server_cpu ;;
	(freebsd) [ -x llama-server ] || llama_server_cpu ;;
	esac

	[ -x llama-server ] || die \
		"No prebuilt llama-server binary is available for your system." \
		"Please compile llama.cpp from source instead."

	[ "$MODEL" ] && set -- -hf "$MODEL" --jinja
	[ $# -gt 0 ] && exec ./llama-server "$@"

	printf "Run ~/.installama/llama-server to launch the llama.cpp server\n"
}

main "$@"
