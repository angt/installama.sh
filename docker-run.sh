case "$1" in
(cuda) ;;
(rocm) ;;
(*) exit ;;
esac

IMG="$1"
shift 1

mkdir -p output

docker build --platform linux/amd64 -t installama . &&
docker build --platform linux/amd64 -f "$IMG/Dockerfile" -t "installama-$IMG" . &&

docker run --rm --platform linux/amd64 \
	-v "$(pwd):/work" \
	--tmpfs /work/deps \
	--tmpfs /work/build \
	--workdir /work \
	"installama-$IMG" \
	"$@"

