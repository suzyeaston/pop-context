# POP//CONTEXT

**Teach machines to hear culture, not just words.**

POP//CONTEXT is an experimental multimodal cultural-intelligence system by [Suzy Easton](https://www.suzyeaston.ca/).

The project begins with a deceptively simple input:

```text
video URL
```

and works toward an evidence-based interpretation of:

- what is being said,
- what is being heard beyond speech,
- what is happening visually,
- which people, songs, films, memes, objects, aesthetics, and cultural references are present,
- and how those layers alter the meaning of a moment.

## Core idea

```text
VIDEO
  ↓
INGEST
video + audio + transcript + metadata
  ↓
PERCEPTION
speech | music | sound | scenes | objects | text
  ↓
TIMELINE
everything synchronized by timestamp
  ↓
CULTURAL MEMORY
works | people | events | memes | references | associations
  ↓
INTERPRETATION
literal | emotional | cultural | uncertain/inferred
```

The system deliberately separates **observation** from **interpretation**. A model should be able to say what evidence it saw, where it occurred, what reference it believes is present, and how confident it is.

## v0.1 goal

Produce a synchronized `analysis.json` for one video containing:

- timestamped transcript,
- scene boundaries,
- representative frames,
- semantic descriptions of non-speech audio,
- visual descriptions,
- detected/reference candidates,
- evidence and confidence,
- higher-level interpretation.

See [`docs/architecture.md`](docs/architecture.md).

## Site

GitHub Pages deploys automatically from `main`:

https://suzyeaston.github.io/pop-context/

The first page is intentionally a project/prototype interface. Later it can become the public front end while the analysis engine runs locally or through an API.

## Local development

Python 3.11+ recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
python -m pop_context.cli --help
```

Static site:

```bash
python3 -m http.server 8080 --directory site
```

Then open http://localhost:8080.

## Roadmap

1. URL → media + metadata
2. transcript with timestamps
3. scene detection + representative frames
4. semantic audio events
5. unified multimodal timeline
6. cultural entity/reference memory
7. evidence-based interpretation
8. searchable visual timeline
9. local-first model experiments
10. public demo/API

## Status

Very early public research build. Expect sharp edges, strange questions, and rapidly evolving architecture.
