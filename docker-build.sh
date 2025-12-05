BACKEND="$1"
FILTER="$2"
case "$FILTER" in
(*-*) ;;
(*) FILTER="$BACKEND-$FILTER" ;;
esac
sh docker-run.sh "$BACKEND" cmake -DFILTER="$FILTER" -P build.cmake

