# SUZY//AI input-pipeline integration

POP//CONTEXT is SUZY//AI's audiovisual input pipeline. The repository boundary
separates media tooling from the shared intelligence core; it does not define a
second AI identity or cultural-memory system.

## Working now

POP//CONTEXT produces local media, transcripts, frames, timestamped evidence and a
report. SUZY//AI provides local text inference, approved retrieval memory, world
teachings and timeline storage. The core does not consume raw audio or video.
There is no automatic evidence transfer between the repositories.

## Intended connection

1. Inspect the local evidence and select observations for inclusion.
2. Preserve source media identifiers, timestamps, exact excerpts, attribution and
   uncertainty. Distinguish direct evidence from generated interpretations.
3. Submit approved material to the appropriate core store. `/v1/teach` records world
   teachings; `/v1/memory` records explicitly approved chat-retrievable notes.
   These are separate stores: teaching does not automatically enable chat recall.
4. Retrieve relevant evidence alongside contributed threads, album reviews and
   musical examples to support shared interpretation and musical suggestions.

This workflow needs an explicit transfer implementation and evaluation. The
existing endpoints are building blocks, not an already connected pipeline.
See SUZY//AI's [memory API](https://github.com/suzyeaston/suzy-ai/blob/main/docs/local-chat.md)
and [teaching surfaces](https://github.com/suzyeaston/suzy-ai/blob/main/docs/teaching-surfaces.md)
for their actual request contracts.

Do not create a second cultural-memory database inside POP//CONTEXT. Temporary
media outputs remain local working evidence. Public examples or reports require a
separate deliberate publication step; private memory is not synchronized to GitHub.

Perception is not automatically truth. Keep direct evidence, Suzy's teachings,
sourced research and model-inferred connections distinguishable. Automated research
and richer audiovisual interpretation remain future work.
