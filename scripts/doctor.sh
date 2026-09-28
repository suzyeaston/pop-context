#!/usr/bin/env bash
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
FAIL=0
check() {
  local name="$1"
  if command -v "$name" >/dev/null 2>&1; then
    printf '\033[32m✓\033[0m %-14s %s\n' "$name" "$(command -v "$name")"
  else
    printf '\033[31m✖\033[0m %-14s missing\n' "$name"
    FAIL=1
  fi
}

echo "POP//CONTEXT doctor"
echo
check git
check ffmpeg
check yt-dlp
check whisper-cli
check python3

if [[ -f models/ggml-tiny.en.bin ]]; then
  printf '\033[32m✓\033[0m %-14s %s\n' "tiny.en model" "installed locally"
else
  printf '\033[31m✖\033[0m %-14s %s\n' "tiny.en model" "missing"
  FAIL=1
fi

if [[ -x .venv/bin/pop-context ]]; then
  printf '\033[32m✓\033[0m %-14s %s\n' "venv" "ready"
else
  printf '\033[31m✖\033[0m %-14s %s\n' "venv" "not installed"
  FAIL=1
fi

echo
if [[ "$FAIL" -eq 0 ]]; then
  echo "Local signal path is ready."
else
  echo "Run ./scripts/install-local.sh"
fi
exit "$FAIL"
