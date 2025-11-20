FEATCODE="https://github.com/angt/featcode/releases/latest/download"
UNZSTD="https://github.com/angt/unzstd/releases/latest/download"
REPO="https://huggingface.co/datasets/angt/installama.sh/resolve/main"

die() {
	for msg; do echo "$msg"; done >&2
	exit 111
}

check_bin() {
	command -v "$1" >/dev/null 2>/dev/null
}

dl_bin() {
	[ -x "$1" ] && return
	check_bin curl || die "Please install curl"
	case "$2" in
	(*.zst) curl -fsSL "$2" | unzstd ;;
	(*)     curl -fsSL "$2" ;;
	esac > "$1.tmp" 2>/dev/null &&
	chmod +x "$1.tmp" && mv "$1.tmp" "$1" && return
	echo "Failed to download $2" >&2
	return 1
}

unzstd() (
	command -v zstd >/dev/null 2>/dev/null && exec zstd -d
	dl_bin unzstd "$UNZSTD/$ARCH-$OS-unzstd"
	exec ./unzstd
)

llama_server_cuda() {
	[ -z "$SKIP_CUDA" ] &&
	dl_bin cuda-probe "$REPO/$ARCH/$OS/cuda/probe/probe.zst" &&
	CONFIG=$(./cuda-probe 2>/dev/null) &&
	dl_bin llama-server "$REPO/$ARCH/$OS/cuda/$CONFIG/llama-server.zst"
}

llama_server_rocm() {
	[ -z "$SKIP_ROCM" ] &&
	dl_bin rocm-probe "$REPO/$ARCH/$OS/rocm/probe/probe.zst" &&
	CONFIG=$(./rocm-probe 2>/dev/null) &&
	dl_bin llama-server "$REPO/$ARCH/$OS/rocm/$CONFIG/llama-server.zst"
}

llama_server_cpu() {
	dl_bin featcode "$FEATCODE/$ARCH-$OS-featcode" &&
	CONFIG=$(./featcode 2>/dev/null) &&
	dl_bin llama-server "$REPO/$ARCH/$OS/cpu/$CONFIG/llama-server.zst"
}

llama_server_metal() {
	CONFIG=$(sysctl -n machdep.cpu.brand_string 2>/dev/null | grep -o "Apple M[1-4]") &&
	CONFIG=m${CONFIG##*M} &&
	dl_bin llama-server "$REPO/$ARCH/$OS/metal/$CONFIG/llama-server.zst"
}

main() {
	case "$(uname -m)" in
	(arm64|aarch64) ARCH=aarch64 ;;
	(amd64|x86_64)  ARCH=x86_64  ;;
	(*) die "Arch not supported"
	esac

	case "$(uname -s)" in
	(Linux)  OS=linux ;;
	(Darwin) OS=macos ;;
	(*) die "OS not supported"
	esac

	[ "$HOME" ] || die "No HOME, please check your OS"

	rm -rf ~/.installama
	mkdir -p ~/.installama
	cd ~/.installama || exit 1

	if [ "$OS" = macos ]; then
		[ -x llama-server ] || llama_server_metal
	else
		[ -x llama-server ] || llama_server_cuda
		[ -x llama-server ] || llama_server_rocm
		[ -x llama-server ] || llama_server_cpu
	fi

	[ -x llama-server ] || die \
		"No prebuilt llama-server binary is available for your system." \
		"Please compile llama.cpp from source instead."

	[ $# -gt 0 ] && exec ./llama-server "$@"

	echo "Run ~/.installama/llama-server to launch the llama.cpp server"
}

main "$@"
