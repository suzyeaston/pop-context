#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
say() { printf '\033[36m→\033[0m %s\n' "$*"; }
ok()  { printf '\033[32m✓\033[0m %s\n' "$*"; }

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "This installer currently targets macOS."
  exit 1
fi

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew is required. Install it from https://brew.sh/ then rerun."
  exit 1
fi

say "Installing/checking local media + AI tools…"
brew install ffmpeg yt-dlp whisper.cpp

PYTHON=""
for candidate in python3.13 python3.12 python3.11 python3; do
  if command -v "$candidate" >/dev/null 2>&1; then
    if "$candidate" - <<'PY' >/dev/null 2>&1
import sys
raise SystemExit(0 if sys.version_info >= (3, 11) else 1)
PY
    then
      PYTHON="$candidate"
      break
    fi
  fi
done

if [[ -z "$PYTHON" ]]; then
  say "Installing Python 3.12…"
  brew install python@3.12
  PYTHON="$(brew --prefix python@3.12)/bin/python3.12"
fi

if [[ ! -d .venv ]]; then
  say "Creating Python virtual environment…"
  "$PYTHON" -m venv .venv
fi

source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install -e .

mkdir -p models workspace
MODEL="${ROOT}/models/ggml-tiny.en.bin"
MODEL_URL="https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.en.bin"

if [[ ! -f "$MODEL" ]]; then
  say "Downloading tiny.en Whisper model (~75 MB)…"
  curl -L --fail --progress-bar "$MODEL_URL" -o "${MODEL}.tmp"
  mv "${MODEL}.tmp" "$MODEL"
else
  ok "tiny.en model already present"
fi

ok "Local install complete"
echo
echo 'Try:'
echo '  ./run-local.sh "https://www.youtube.com/watch?v=VIDEO_ID" --duration 30'
