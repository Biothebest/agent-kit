---
name: local-whisper-transcribe
description: "Use when audio needs a free, offline transcript on an Apple silicon Mac (voice memos, test clips, recordings), or when comparing local Whisper with a cloud transcription API. Runs Whisper large-v3-turbo through mlx-whisper; nothing leaves the machine."
compatibility: Apple silicon macOS with Python 3.10+, uv or a venv with mlx-whisper, and the mlx-community/whisper-large-v3-turbo model cached locally.
---

# Local Whisper transcription (mlx-whisper)

Open-source Whisper large-v3-turbo (MLX build) transcribes on-device for free. Check whether it is
already cached before telling the user it is missing or offering a different Whisper install.

- Model: `mlx-community/whisper-large-v3-turbo` (about 1.6 GB), cached under
  `~/.cache/huggingface/hub/models--mlx-community--whisper-large-v3-turbo`. The snapshot links
  into the shared blob store, so `du` on the model folder alone reports only a few KB.
- mlx-whisper installs no command on PATH by default, so `command -v whisper` finding nothing does
  not mean the model is missing. Check the cache directory instead.
- Without ffmpeg, `mlx_whisper <file>` and `transcribe("file.wav")` fail. Pass a float32 numpy
  array at 16 kHz instead (recipe below).
- Set `HF_HUB_OFFLINE=1` to use the cached model without touching the network. Omit it only for
  the first download, and only when the user agreed to it.

## Recipe

Convert to 16 kHz mono first with the built-in macOS converter (works for 8 kHz telephony WAV,
m4a and aiff): `afconvert -f WAVE -d LEI16@16000 -c 1 in.wav out16k.wav`

```python
import wave, numpy as np, mlx_whisper
w = wave.open("out16k.wav")
audio = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
r = mlx_whisper.transcribe(audio, path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="en")
print(r["text"])            # r["segments"] has start/end timestamps
```

Run it with `HF_HUB_OFFLINE=1 uv run --quiet --no-project --with mlx-whisper python script.py`,
or with a pinned venv's interpreter when results must be comparable across runs.

Measured on an Apple M5 with 16 GB (2026-10-08): about 3.8 s for the first clip including model
load, then about 0.4 s per short clip.

## Comparing with a cloud transcription API

- Freeze the test clips first and keep them synthetic or consented.
- Compare word error rate on the worst pass, key-detail recall (names, numbers, dates) and
  hallucinated content, not overall impressions.
- Cap cloud spend before running, and delete any copied credentials file afterwards.

## Boundaries

- MLX runs only on Apple silicon; it cannot replace a Linux server transcription path as-is.
- Keep recordings of real people local. Never paste their transcripts into lessons, docs, or Git.
- Embedding models cannot transcribe. They only score closeness between audio and existing text,
  and they cannot tell 0142 from 0124 or Johnson from Jonson.
