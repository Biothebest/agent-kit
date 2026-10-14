---
name: local-embeddinggemma
description: "Use when a task needs vector embeddings, semantic search, clustering, dedup, or text/image/audio similarity and EmbeddingGemma 2 is served by a local Ollama. Free and offline."
compatibility: Requires Ollama on 127.0.0.1:11434 with the embeddinggemma-2 model available (check with `ollama list`).
---

# Local EmbeddingGemma 2 (Ollama)

EmbeddingGemma 2 (Google, 740M, Apache 2.0) returns 768-dim vectors in one shared space for text,
code, images, and 16 kHz mono audio. Ollama serves it locally; nothing leaves the machine.

- Server: `http://127.0.0.1:11434`. Check: `curl -s localhost:11434/api/version`. On macOS, start
  it with `open -a Ollama` if it is down.
- Model id: `embeddinggemma-2` (`embeddinggemma-2:latest`, text+image+audio). Confirm with
  `ollama list` before relying on it.
- It is an embedding model, not a chat model. Never select it as a chat or session model. Use it
  by asking the agent for a result (search, group, dedup by meaning); the agent calls Ollama as
  shown below.
- In OMP it appears as `ollama/embeddinggemma-2:latest` with kind `embedding`
  (`omp models --kind all`) when the profile's `models.yml` declares it; no OMP role accepts it.
- CLI: `ollama run embeddinggemma-2 "text"` prints one JSON vector.

## Prompt prefixes (required for good retrieval)

Ollama does NOT add them. Prepend them yourself:

| Use | Prefix |
|---|---|
| Search query | `task: search result \| query: ` |
| Document / corpus item | `title: none \| text: ` (or `title: <title> \| text: `) |
| Question answering query | `task: question answering \| query: ` |
| Code retrieval query | `task: code retrieval \| query: ` |
| Classification | `task: classification \| query: ` |
| Clustering | `task: clustering \| query: ` |
| Similarity (symmetric) | `task: sentence similarity \| query: ` |
| Fact checking | `task: fact checking \| query: ` |

Embed queries and documents with different prefixes. Images and audio need no prefix.

## API

Native endpoint (multimodal):

```bash
curl -s localhost:11434/api/embed -d '{"model":"embeddinggemma-2","input":["task: search result | query: refund policy", {"image":"<base64>"}, {"audio":"<base64 16kHz mono wav>"}]}'
```

- `input`: a string, a list, or objects with `text`, `image`, or `audio` (base64). Video is not accepted.
- `dimensions`: 512, 256, or 128 for Matryoshka truncation (256 keeps quality close to 768).
- Response: `{"embeddings": [[...], ...]}`. Vectors are normalized; use cosine similarity or dot product.

OpenAI-compatible (text only): `POST http://127.0.0.1:11434/v1/embeddings` with `{"model":"embeddinggemma-2","input":[...]}`.
Any key works if a client requires one.

Batch inputs (hundreds per request). Measured on an Apple M5 with 16 GB: about 87 text docs/s,
about 1 s per image or short audio clip. The model uses about 1.3 GB of GPU memory and unloads
after 5 minutes idle (`keep_alive` overrides). On macOS, make speech audio 16 kHz mono with
`afconvert -f WAVE -d LEI16@16000 -c 1 in.m4a out.wav`.

## Limits

- Ollama serves a quantized build (`ollama show embeddinggemma-2`). For full-precision or
  video embeddings, use `sentence-transformers>=6.1` with `google/embeddinggemma-2` in bf16 or
  fp32 (never fp16) in a throwaway venv.
- Do not wire an agent memory backend to this model without the user's approval.
- OMP's `auth-gateway` does not route to this local model (404). Call Ollama directly.
