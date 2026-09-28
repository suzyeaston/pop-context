#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [[ ! -d .venv ]] || [[ ! -x .venv/bin/pop-context ]]; then
  echo "POP//CONTEXT local environment is not installed yet."
  echo "Run: ./scripts/install-local.sh"
  exit 1
fi

if [[ $# -lt 1 ]]; then
  echo 'Usage: ./run-local.sh "YOUTUBE_URL" [extra options]'
  echo 'Example: ./run-local.sh "https://youtu.be/..." --duration 30'
  exit 1
fi

source .venv/bin/activate
exec pop-context analyze "$@"
