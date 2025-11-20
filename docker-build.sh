case "$1" in
(cuda) ;;
(rocm) ;;
(*) exit ;;
esac

mkdir -p output deps

docker build --platform linux/amd64 -t "installama" . &&
docker build --platform linux/amd64 -f "$1/Dockerfile" -t "installama-$1" . &&

docker run --rm --platform linux/amd64 \
	-v "$(pwd):/work" \
	--workdir /work \
	--user "$(id -u):$(id -g)" \
	"installama-$1" \
	cmake -DFILTER="$1" -P build.cmake
