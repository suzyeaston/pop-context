# POP//CONTEXT Architecture

POP//CONTEXT is the audiovisual input component of SUZY//AI. This document covers
the pipeline direction, including planned stages. The working v0.1 produces local
media, transcripts, representative frames and evidence reports; later perception
and shared interpretation stages are not yet implemented.

## Principle

Do not ask one model to "understand the whole video."

Create timestamped evidence first, then reason across evidence.

## Pipeline

### 1. Ingest

Input:
- URL
- uploaded/local media later

Outputs:
- source metadata
- normalized video
- normalized audio

Likely tools:
- `yt-dlp`
- `ffmpeg`

### 2. Speech

Outputs:
- timestamped transcript
- speaker/voice segments when available
- language
- confidence

### 3. Audio perception

Non-speech signals:
- music
- instrumentation
- sound events
- ambience
- crowd reaction
- sonic texture

Initial direction:
- CLAP-style audio/text embeddings
- audio event classification
- later music identification/reference enrichment

### 4. Visual perception

First detect scenes, then inspect representative frames.

Outputs:
- scene boundaries
- visual descriptions
- visible text
- objects
- people/entity candidates
- aesthetic/style observations

Initial direction:
- PySceneDetect
- ffmpeg frame extraction
- vision-language model

### 5. Unified timeline

Canonical record:

```json
{
  "start": 41.2,
  "end": 48.7,
  "speech": [],
  "audio": [],
  "visual": [],
  "entities": [],
  "references": [],
  "interpretation": [],
  "confidence": {}
}
```

Everything downstream should point back to timestamps/evidence.

### 6. Shared cultural memory in SUZY//AI

An approved transfer into SUZY//AI is planned. Cultural memory belongs to the
shared core; this pipeline should not maintain a competing memory database.
That shared layer can connect observations with entities and relationships:

```text
object / lyric / phrase / sound / person
             ↓
         cultural entity
             ↓
work ↔ artist ↔ era ↔ event ↔ meme ↔ usage ↔ association
```

This should be retrieval-based and inspectable rather than hidden inside one giant prompt.

### 7. Interpretation through SUZY//AI

Future interpretation should use shared SUZY//AI inference and relevant memory,
with this pipeline retaining the evidence references. See the
[integration boundary](suzy-ai-integration.md).

Return separate fields for:

- literal observation
- emotional function
- cultural context
- likely reference
- possible interpretation
- uncertainty / alternate interpretations

A reference is not a fact merely because a model noticed a resemblance.

## v0.1 data contract

See `examples/analysis.sample.json`.

The first meaningful milestone is:

> one video → one synchronized, inspectable `analysis.json`

No custom model training is required for this milestone.
