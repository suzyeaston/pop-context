# POP//CONTEXT

**The audiovisual input pipeline for SUZY//AI.**

POP//CONTEXT is the local audiovisual input component of [SUZY//AI](https://github.com/suzyeaston/suzy-ai), the music and cultural-intelligence project by [Suzy Easton](https://www.suzyeaston.ca/). It prepares inspectable media evidence for a shared system of memory, interpretation, and developing musical taste. The pipeline lives in its own repository so its media tools can be developed and run independently.

## Current milestone: local evidence pipeline

The repository is public. The analysis itself runs locally.

```text
VIDEO URL
   ↓
short local media window
   ↓
speech + representative frames
   ↓
timestamped evidence
   ↓
analysis.json + local report
```

The current v0.1 deliberately stops **before** cultural AI interpretation. First we make perception inspectable and reproducible.

## Mac setup

```bash
git clone https://github.com/suzyeaston/pop-context.git
cd pop-context
./scripts/install-local.sh
```

Then:

```bash
./run-local.sh "https://www.youtube.com/watch?v=..." --duration 30
```

Diagnostics:

```bash
./scripts/doctor.sh
```

## Privacy / repository boundaries

These are intentionally ignored by Git:

```text
models/
workspace/
```

Downloaded media, transcripts, model weights and generated reports stay on the local machine.

## Current output

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

<!-- SUZY-AI-INTEGRATION -->

## SUZY//AI

POP//CONTEXT owns media ingest, timestamped evidence and the local evidence report. Shared memory, cultural interpretation and musical taste belong to SUZY//AI. Approved media observations are intended to join the context supplied by threads, album reviews and musical examples.

That transfer is not automated today. Running this pipeline produces local files; it does not write to SUZY//AI memory or publish observations. The core currently supports text inference and retrieval, with world teachings stored separately. There is no second cultural-memory database planned here.

See [`docs/suzy-ai-integration.md`](docs/suzy-ai-integration.md).

## Architecture

- [`docs/local-first.md`](docs/local-first.md)
- [`docs/architecture.md`](docs/architecture.md)

## Roadmap

1. **local ingest + transcript + representative frames** ← now
2. scene-aware sampling
3. semantic non-speech audio
4. visual-language perception
5. synchronized multimodal timeline
6. approved evidence transfer into SUZY//AI
7. evidence-based interpretation through SUZY//AI shared memory and inference
8. selected public demonstration interface

Steps after the current milestone are planned. Cultural memory and developing
musical taste are shared SUZY//AI work, supported by this input pipeline.

## Public site

There is an experimental static interface in this repository, but **the local AI application is not being published as a live web service yet**.
