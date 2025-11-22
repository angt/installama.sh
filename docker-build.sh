case "$1" in
(cuda) ;;
(rocm) ;;
(*) exit ;;
esac

mkdir -p output

docker build --platform linux/amd64 -t installama . &&
docker build --platform linux/amd64 -f "$1/Dockerfile" -t "installama-$1" . &&

docker run --rm --platform linux/amd64 \
	-v "$(pwd):/work" \
	--tmpfs /work/deps \
	--tmpfs /work/build \
	--workdir /work \
	"installama-$1" \
	cmake -DFILTER="$1" -P build.cmake

