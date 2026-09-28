# Local-first v0.1

POP//CONTEXT intentionally begins as a local application.

The public GitHub repository contains the code. It does **not** contain downloaded source video/audio, model weights, transcripts, or generated reports. Those stay under `workspace/` and `models/`, both ignored by Git.

## v0.1 pipeline

```text
video URL
   ↓
yt-dlp
   ↓
short local video window (default 60 sec)
   ↓
ffmpeg
   ├── 16 kHz mono WAV
   └── representative frames
   ↓
whisper.cpp tiny.en
   ↓
timestamped transcript
   ↓
analysis.json
   ↓
local report.html
```

There is no cultural interpretation model yet. That is deliberate: evidence first.

## Install on macOS

```bash
./scripts/install-local.sh
```

## Analyze

```bash
./run-local.sh "https://www.youtube.com/watch?v=..."
```

Smaller slice:

```bash
./run-local.sh "URL" --duration 30
```

Later section:

```bash
./run-local.sh "URL" --start 120 --duration 45
```

Each source gets a private ignored workspace folder:

```text
workspace/<video-id>/
├── metadata.json
├── source.mp4
├── audio.wav
├── transcript.json
├── frames/
├── analysis.json
└── report.html
```

## Next

1. scene-aware frame extraction
2. semantic non-speech audio perception
3. visual-language description
4. synchronized evidence timeline
5. cultural retrieval/memory
6. interpretation with confidence + provenance
