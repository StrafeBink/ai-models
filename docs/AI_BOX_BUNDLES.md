# AI Box Bundles

Purpose: practical transfer batches for manually copying verified models from the file-server library to the separate AI box.

Use with:

```bash
python scripts/generate_ai_box_transfer_manifest.py --bundle <bundle-name>
```

The script writes a dated checklist under `transfer-manifests/`.

## Bundle summary

| Bundle | Goal | Approx size | Copy priority |
|---|---|---:|---|
| `minimal-rag` | Small working RAG/safety/chat stack | ~23.50 GiB | First |
| `coding-assistant` | Coding assistant trial stack | ~55.97 GiB | High |
| `speech-and-docs` | STT + OCR + embeddings tests | ~8.42 GiB | High |
| `image-generation-small-first` | Image-generation trial without moving every huge model | ~62.67 GiB | Medium/high |
| `llm-comparison` | Compare active reasoning/chat candidates | ~85.95 GiB | Medium |

## `minimal-rag`

Use this first if the AI box is going to run local RAG/agent experiments.

```text
Embeddings/all-MiniLM-L6-v2
Safety-Moderation/Prompt-Guard-86M
LLM/Qwen3-32B-Q5_K_M
```

Why:

- small embeddings baseline,
- small prompt-safety guardrail,
- one serious local LLM candidate.

Generate manifest:

```bash
python scripts/generate_ai_box_transfer_manifest.py --bundle minimal-rag
```

## `coding-assistant`

Use this for coding-assistant benchmarks on the AI box.

```text
Coding/Qwen3-Coder-30B-A3B-UD-Q4_K_XL
LLM/GPT-OSS-20B
Safety-Moderation/Prompt-Guard-86M
```

Why:

- dedicated GGUF coding model,
- general reasoning/chat fallback,
- prompt-safety guardrail.

Generate manifest:

```bash
python scripts/generate_ai_box_transfer_manifest.py --bundle coding-assistant
```

## `speech-and-docs`

Use this for transcription, OCR, and document/RAG experiments.

```text
Speech-STT/whisper-large-v3-turbo
Vision-OCR/DeepSeek-OCR-2
Embeddings/all-MiniLM-L6-v2
```

Why:

- small Whisper turbo STT candidate,
- OCR/document extraction model,
- embeddings baseline for downstream retrieval.

Generate manifest:

```bash
python scripts/generate_ai_box_transfer_manifest.py --bundle speech-and-docs
```

## `image-generation-small-first`

Use this before moving very large image-generation folders.

```text
Diffusion-Image/FLUX.2-klein-9b-fp8
Diffusion-Image/FLUX.1-schnell
```

Why:

- tests ComfyUI/diffusers image workflow with smaller/faster candidates,
- avoids copying `FLUX.2-dev` until there is a specific reason.

Generate manifest:

```bash
python scripts/generate_ai_box_transfer_manifest.py --bundle image-generation-small-first
```

## `llm-comparison`

Use this when the AI box is ready to compare active chat/reasoning models.

```text
LLM/Qwen3-32B-Q5_K_M
LLM/GPT-OSS-20B
LLM/Ministral-3-14B-Q5_K_M
LLM/Gemma-3-27B-QAT-Q4_0
```

Why:

- compares active local reasoning/chat candidates,
- avoids archive-only models,
- gives a mix of size/performance tradeoffs.

Generate manifest:

```bash
python scripts/generate_ai_box_transfer_manifest.py --bundle llm-comparison
```

## General rules

- Copy one bundle at a time.
- Verify size, payload file count, and `_hermes_model_metadata.json` after transfer.
- Record AI-box benchmark results back into this project.
- Do not routinely move `Archive-Huge/` models unless there is a specific future-hardware or comparison test.
