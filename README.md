# POP//CONTEXT

**Teach machines to hear culture, not just words.**

POP//CONTEXT is a public, local-first experiment by [Suzy Easton](https://www.suzyeaston.ca/) exploring how software might understand audiovisual material as **cultural meaning**, rather than treating video as a transcript with pictures attached.

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

POP//CONTEXT is the **observer** inside the broader [SUZY//AI](https://github.com/suzyeaston/suzy-ai) architecture.

It keeps owning audiovisual evidence and media timelines while feeding approved observations into SUZY//AI's single private world model instead of creating a second cultural-memory database.

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
6. cultural memory / retrieval
7. evidence-based interpretation
8. public demonstration interface

## Public site

There is an experimental static interface in this repository, but **the local AI application is not being published as a live web service yet**.
