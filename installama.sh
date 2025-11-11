TARGET_FEATURES="https://github.com/angt/target-features/releases/latest/download"
UNZSTD="https://github.com/angt/unzstd/releases/latest/download"
REPO="https://huggingface.co/datasets/angt"

die() {
	for msg; do echo "$msg"; done >&2
	exit 111
}

check_bin() {
	command -v "$1" >/dev/null 2>/dev/null
}

datasets() {
	printf "%s/installamacpp-%s/resolve/main/%s" "$REPO" "$1" "$2"
}

dl_bin() {
	[ -x "$1" ] && return
	check_bin curl || die "Please install curl"
	case "$2" in
	(*.zst) curl -fsSL "$2" | unzstd ;;
	(*)     curl -fsSL "$2" ;;
	esac > "$1.tmp" 2>/dev/null &&
	chmod +x "$1.tmp" &&
	mv "$1.tmp" "$1" ||
	echo "Failed to download $2"
}

unzstd() (
	command -v zstd >/dev/null 2>/dev/null && exec zstd -d
	dl_bin unzstd "$UNZSTD/$ARCH-$OS-unzstd"
	exec ./unzstd
)

llama_server_cuda() {
	dl_bin cuda-probe "$(datasets cuda "cuda-probe.zst")" &&
	CUDA_ARCH=$(./cuda-probe 2>/dev/null) &&
	dl_bin llama-server "$(datasets cuda "llama-server-cuda-$CUDA_ARCH.zst")"
}

llama_server_rocm() {
	dl_bin rocm-probe "$(datasets rocm "rocm-probe.zst")" &&
	ROCM_ARCH=$(./rocm-probe 2>/dev/null) &&
	dl_bin llama-server "$(datasets rocm "llama-server-$ROCM_ARCH.zst")"
}

llama_server_cpu() {
	dl_bin target-features "$TARGET_FEATURES/$ARCH-$OS-target-features" &&
	TARGET=$(./target-features 2>/dev/null) &&
	dl_bin llama-server "$(datasets cpu "llama-server-$ARCH$TARGET.zst")"
}

llama_server_metal() {
	MODEL=$(sysctl -n machdep.cpu.brand_string 2>/dev/null) &&
	case "$MODEL" in ("Apple M"[1234]) MODEL=${MODEL#"Apple M"} ;; (*) false ;; esac &&
	dl_bin llama-server "$(datasets metal "llama-server-m$MODEL.zst")"
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
