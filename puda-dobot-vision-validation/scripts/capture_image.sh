#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  printf 'Usage: %s /absolute/output.jpg\n' "$0" >&2
  exit 2
fi

output=$1
stream_url=${DOBOT_VISION_RTSP_URL:-}

if [[ -z "$stream_url" ]]; then
  printf 'DOBOT_VISION_RTSP_URL is required. Use a credential-free local proxy/stream URL.\n' >&2
  exit 2
fi

if [[ "$output" != /* ]]; then
  printf 'Output path must be absolute: %s\n' "$output" >&2
  exit 2
fi

for command in ffmpeg ffprobe sha256sum stat date; do
  if ! command -v "$command" >/dev/null 2>&1; then
    printf 'Missing required command: %s\n' "$command" >&2
    exit 127
  fi
done

mkdir -p "$(dirname "$output")"
extension=${output##*.}
if [[ "$extension" == "$output" ]]; then
  extension=jpg
fi
tmp="${output%.*}.partial.$$.${extension}"
cleanup() { rm -f "$tmp"; }
trap cleanup EXIT

capture_utc=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
redact_stream() {
  sed -E 's#(rtsp://)[^/@[:space:]]+:[^/@[:space:]]+@#\1[REDACTED]@#g'
}

if ! ffmpeg -hide_banner -loglevel error -y -rtsp_transport tcp \
  -i "$stream_url" -frames:v 1 -q:v 2 "$tmp" \
  2> >(redact_stream >&2); then
  printf 'Passive IP-camera capture failed. No robot or camera movement was requested.\n' >&2
  exit 1
fi

read -r width height < <(
  ffprobe -v error -select_streams v:0 \
    -show_entries stream=width,height -of csv=s=x:p=0 "$tmp" | tr 'x' ' '
)

if [[ ! "$width" =~ ^[1-9][0-9]*$ || ! "$height" =~ ^[1-9][0-9]*$ ]]; then
  printf 'Captured file has invalid dimensions.\n' >&2
  exit 1
fi

mv "$tmp" "$output"
trap - EXIT

size=$(stat -c '%s' "$output")
hash=$(sha256sum "$output" | cut -d' ' -f1)
printf 'capture_utc=%s\n' "$capture_utc"
printf 'path=%s\n' "$output"
printf 'size_bytes=%s\n' "$size"
printf 'dimensions=%sx%s\n' "$width" "$height"
printf 'sha256=%s\n' "$hash"
printf 'passive=true\n'
printf 'motion_commanded=false\n'
