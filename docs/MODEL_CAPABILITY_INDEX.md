# Model Capability Index

Generated from the latest clean local-library audit. This is a human decision layer over the verified model folders.

## Status meanings

| Status | Meaning |
|---|---|
| `runnable_with_runtime_install` | Files are present; install/use the named runtime stack before running. |
| `archive_only` | Strategic/future-hardware store, not expected to run today. |
| `unknown` | Needs manual runtime/capability review. |

## Capability cards

| Location | Model | Capability | Runnable status | Keep status | Runtime | Size | Use |
|---|---|---|---|---|---|---:|---|
| Archive-Huge/Coding | `Qwen3-Coder-30B-A3B-Instruct` | Coding LLM | `archive_only` | `strategic_archive` | llama.cpp for GGUF; transformers/vLLM for safetensors archive. | 57.17 GiB | Local coding assistant, code generation, code review. |
| Archive-Huge/Coding | `Qwen3-Coder-30B-A3B-Instruct-FP8` | Coding LLM | `archive_only` | `strategic_archive` | llama.cpp for GGUF; transformers/vLLM for safetensors archive. | 29.05 GiB | Local coding assistant, code generation, code review. |
| Archive-Huge/LLM | `Kimi-K3` | LLM / reasoning-chat | `archive_only` | `strategic_archive` | llama.cpp for GGUF; transformers/vLLM for safetensors archives. | 1453.79 GiB | Local chat, reasoning, drafting, agent backend. |
| Archive-Huge/LLM | `Llama-2-7b-chat-hf` | LLM / reasoning-chat | `archive_only` | `strategic_archive` | llama.cpp for GGUF; transformers/vLLM for safetensors archives. | 25.11 GiB | Local chat, reasoning, drafting, agent backend. |
| Archive-Huge/LLM | `Llama-3.1-8B-Instruct` | LLM / reasoning-chat | `archive_only` | `strategic_archive` | llama.cpp for GGUF; transformers/vLLM for safetensors archives. | 29.93 GiB | Local chat, reasoning, drafting, agent backend. |
| Archive-Huge/LLM | `Llama-3.2-1B-Instruct` | LLM / reasoning-chat | `archive_only` | `strategic_archive` | llama.cpp for GGUF; transformers/vLLM for safetensors archives. | 4.61 GiB | Local chat, reasoning, drafting, agent backend. |
| Archive-Huge/LLM | `Meta-Llama-3-8B` | LLM / reasoning-chat | `archive_only` | `strategic_archive` | llama.cpp for GGUF; transformers/vLLM for safetensors archives. | 29.93 GiB | Local chat, reasoning, drafting, agent backend. |
| Archive-Huge/Multimodal | `Qwen-AgentWorld-35B-A3B` | LLM / reasoning-chat | `archive_only` | `strategic_archive` | llama.cpp for GGUF; transformers/vLLM for safetensors archives. | 64.58 GiB | Local chat, reasoning, drafting, agent backend. |
| Archive-Huge/Multimodal | `Qwen2.5-VL-3B-Instruct` | LLM / reasoning-chat | `archive_only` | `strategic_archive` | llama.cpp for GGUF; transformers/vLLM for safetensors archives. | 7.00 GiB | Local chat, reasoning, drafting, agent backend. |
| Archive-Huge/Multimodal | `Qwen2.5-VL-7B-Instruct` | LLM / reasoning-chat | `archive_only` | `strategic_archive` | llama.cpp for GGUF; transformers/vLLM for safetensors archives. | 15.46 GiB | Local chat, reasoning, drafting, agent backend. |
| Archive-Huge/Multimodal | `Qwen3.6-35B-A3B-FP8` | LLM / reasoning-chat | `archive_only` | `strategic_archive` | llama.cpp for GGUF; transformers/vLLM for safetensors archives. | 33.45 GiB | Local chat, reasoning, drafting, agent backend. |
| Audio | `personaplex-7b-v1` | Audio generation / audio model | `runnable_with_runtime_install` | `active` | Model-specific audio/diffusers stack. | 15.96 GiB | Audio/music/SFX generation or audio-specific workflows. |
| Audio | `stable-audio-3-medium` | Audio generation / audio model | `runnable_with_runtime_install` | `active` | Model-specific audio/diffusers stack. | 9.73 GiB | Audio/music/SFX generation or audio-specific workflows. |
| Audio | `stable-audio-3-small-sfx` | Audio generation / audio model | `runnable_with_runtime_install` | `active` | Model-specific audio/diffusers stack. | 3.25 GiB | Audio/music/SFX generation or audio-specific workflows. |
| Audio | `stable-audio-open-1.0` | Audio generation / audio model | `runnable_with_runtime_install` | `active` | Model-specific audio/diffusers stack. | 14.60 GiB | Audio/music/SFX generation or audio-specific workflows. |
| Coding | `Qwen3-Coder-30B-A3B-UD-Q4_K_XL` | Coding LLM | `runnable_with_runtime_install` | `active` | llama.cpp for GGUF; transformers/vLLM for safetensors archive. | 16.45 GiB | Local coding assistant, code generation, code review. |
| Coding | `Qwen3-Coder-Next-Q4_K_M` | Coding LLM | `runnable_with_runtime_install` | `active` | llama.cpp for GGUF; transformers/vLLM for safetensors archive. | 45.09 GiB | Local coding assistant, code generation, code review. |
| Diffusion-Image | `FLUX.1-dev` | Image generation/editing | `runnable_with_runtime_install` | `active` | ComfyUI or diffusers. | 60.59 GiB | Text-to-image, image editing, diffusion workflows. |
| Diffusion-Image | `FLUX.1-Fill-dev` | Image generation/editing | `runnable_with_runtime_install` | `active` | ComfyUI or diffusers. | 54.07 GiB | Text-to-image, image editing, diffusion workflows. |
| Diffusion-Image | `FLUX.1-Kontext-dev` | Image generation/editing | `runnable_with_runtime_install` | `active` | ComfyUI or diffusers. | 53.92 GiB | Text-to-image, image editing, diffusion workflows. |
| Diffusion-Image | `FLUX.1-schnell` | Image generation/editing | `runnable_with_runtime_install` | `active` | ComfyUI or diffusers. | 53.87 GiB | Text-to-image, image editing, diffusion workflows. |
| Diffusion-Image | `FLUX.2-dev` | Image generation/editing | `runnable_with_runtime_install` | `active` | ComfyUI or diffusers. | 165.44 GiB | Text-to-image, image editing, diffusion workflows. |
| Diffusion-Image | `FLUX.2-klein-9B` | Image generation/editing | `runnable_with_runtime_install` | `active` | ComfyUI or diffusers. | 49.26 GiB | Text-to-image, image editing, diffusion workflows. |
| Diffusion-Image | `FLUX.2-klein-9b-fp8` | Image generation/editing | `runnable_with_runtime_install` | `active` | ComfyUI or diffusers. | 8.79 GiB | Text-to-image, image editing, diffusion workflows. |
| Diffusion-Image | `stable-diffusion-3-medium` | Image generation/editing | `runnable_with_runtime_install` | `active` | ComfyUI or diffusers. | 49.66 GiB | Text-to-image, image editing, diffusion workflows. |
| Diffusion-Image | `stable-diffusion-3.5-large` | Image generation/editing | `runnable_with_runtime_install` | `active` | ComfyUI or diffusers. | 66.67 GiB | Text-to-image, image editing, diffusion workflows. |
| Embeddings | `all-MiniLM-L12-v2` | Embeddings / retrieval | `runnable_with_runtime_install` | `active` | sentence-transformers or transformers; GGUF embedding runtime for GGUF quants. | 1.21 GiB | Semantic search, RAG retrieval, clustering, similarity. |
| Embeddings | `all-MiniLM-L6-v2` | Embeddings / retrieval | `runnable_with_runtime_install` | `active` | sentence-transformers or transformers; GGUF embedding runtime for GGUF quants. | 0.83 GiB | Semantic search, RAG retrieval, clustering, similarity. |
| Embeddings | `all-mpnet-base-v2` | Embeddings / retrieval | `runnable_with_runtime_install` | `active` | sentence-transformers or transformers; GGUF embedding runtime for GGUF quants. | 3.56 GiB | Semantic search, RAG retrieval, clustering, similarity. |
| Embeddings | `embeddinggemma-300m` | Embeddings / retrieval | `runnable_with_runtime_install` | `active` | sentence-transformers or transformers; GGUF embedding runtime for GGUF quants. | 1.18 GiB | Semantic search, RAG retrieval, clustering, similarity. |
| Embeddings | `paraphrase-multilingual-MiniLM-L12-v2` | Embeddings / retrieval | `runnable_with_runtime_install` | `active` | sentence-transformers or transformers; GGUF embedding runtime for GGUF quants. | 3.87 GiB | Semantic search, RAG retrieval, clustering, similarity. |
| Embeddings | `paraphrase-multilingual-mpnet-base-v2` | Embeddings / retrieval | `runnable_with_runtime_install` | `active` | sentence-transformers or transformers; GGUF embedding runtime for GGUF quants. | 9.07 GiB | Semantic search, RAG retrieval, clustering, similarity. |
| Embeddings | `Qwen3-Embedding-8B-Q4_K_M` | Embeddings / retrieval | `runnable_with_runtime_install` | `active` | sentence-transformers or transformers; GGUF embedding runtime for GGUF quants. | 4.36 GiB | Semantic search, RAG retrieval, clustering, similarity. |
| Embeddings | `Qwen3-VL-Embedding-8B` | Embeddings / retrieval | `runnable_with_runtime_install` | `active` | sentence-transformers or transformers; GGUF embedding runtime for GGUF quants. | 15.19 GiB | Semantic search, RAG retrieval, clustering, similarity. |
| LLM | `DeepSeek-R1-Distill-Qwen-32B-Q5_K_M` | LLM / reasoning-chat | `runnable_with_runtime_install` | `active` | llama.cpp for GGUF; transformers/vLLM for safetensors archives. | 21.66 GiB | Local chat, reasoning, drafting, agent backend. |
| LLM | `Gemma-3-27B-QAT-Q4_0` | LLM / reasoning-chat | `runnable_with_runtime_install` | `active` | llama.cpp for GGUF; transformers/vLLM for safetensors archives. | 16.05 GiB | Local chat, reasoning, drafting, agent backend. |
| LLM | `GLM-4.7-Flash-Q4_K_M` | LLM / reasoning-chat | `runnable_with_runtime_install` | `active` | llama.cpp for GGUF; transformers/vLLM for safetensors archives. | 17.21 GiB | Local chat, reasoning, drafting, agent backend. |
| LLM | `GPT-OSS-20B` | LLM / reasoning-chat | `runnable_with_runtime_install` | `active` | llama.cpp for GGUF; transformers/vLLM for safetensors archives. | 38.47 GiB | Local chat, reasoning, drafting, agent backend. |
| LLM | `Ministral-3-14B-Q5_K_M` | LLM / reasoning-chat | `runnable_with_runtime_install` | `active` | llama.cpp for GGUF; transformers/vLLM for safetensors archives. | 8.96 GiB | Local chat, reasoning, drafting, agent backend. |
| LLM | `Qwen3-32B-Q5_K_M` | LLM / reasoning-chat | `runnable_with_runtime_install` | `active` | llama.cpp for GGUF; transformers/vLLM for safetensors archives. | 21.62 GiB | Local chat, reasoning, drafting, agent backend. |
| LLM | `Qwen3.6-35B-A3B-NVFP4` | LLM / reasoning-chat | `runnable_with_runtime_install` | `active` | llama.cpp for GGUF; transformers/vLLM for safetensors archives. | 21.85 GiB | Local chat, reasoning, drafting, agent backend. |
| LLM | `Qwen3.6-35B-A3B-UD-Q4_K_M` | LLM / reasoning-chat | `runnable_with_runtime_install` | `active` | llama.cpp for GGUF; transformers/vLLM for safetensors archives. | 20.61 GiB | Local chat, reasoning, drafting, agent backend. |
| Safety-Moderation | `Prompt-Guard-86M` | Prompt safety / moderation | `runnable_with_runtime_install` | `active` | transformers sequence-classification. | 1.05 GiB | Prompt-injection and jailbreak risk classifier for agents/RAG. |
| Speech-STT | `nemotron-3.5-asr-streaming-0.6b` | Speech-to-text | `runnable_with_runtime_install` | `active` | faster-whisper preferred; transformers fallback. | 5.27 GiB | Transcription and speech recognition. |
| Speech-STT | `whisper-large-v2` | Speech-to-text | `runnable_with_runtime_install` | `review_after_benchmark` | faster-whisper preferred; transformers fallback. | 23.00 GiB | Transcription and speech recognition. |
| Speech-STT | `whisper-large-v3` | Speech-to-text | `runnable_with_runtime_install` | `active` | faster-whisper preferred; transformers fallback. | 23.01 GiB | Transcription and speech recognition. |
| Speech-STT | `whisper-large-v3-turbo` | Speech-to-text | `runnable_with_runtime_install` | `active` | faster-whisper preferred; transformers fallback. | 1.51 GiB | Transcription and speech recognition. |
| Video | `stable-video-diffusion-img2vid-xt-1-1` | Video generation | `runnable_with_runtime_install` | `active` | ComfyUI or diffusers Stable Video pipeline. | 17.06 GiB | Image-to-video generation. |
| Vision-OCR | `DeepSeek-OCR-2` | OCR / document extraction | `runnable_with_runtime_install` | `active` | transformers/custom model code, likely GPU/accelerator dependent. | 6.32 GiB | Image/PDF text extraction and document understanding. |

## Notes by model

### `Qwen3-Coder-30B-A3B-Instruct`

- Repo: `Qwen/Qwen3-Coder-30B-A3B-Instruct`
- Location: `Archive-Huge/Coding`
- Capability: Coding LLM
- Runtime: llama.cpp for GGUF; transformers/vLLM for safetensors archive.
- Runnable status: `archive_only`
- Keep status: `strategic_archive`
- Size: `57.17 GiB`; payload files: `29`
- Recommended use: Local coding assistant, code generation, code review.
- Notes: GGUF quants are the most likely current runnable path.

### `Qwen3-Coder-30B-A3B-Instruct-FP8`

- Repo: `Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8`
- Location: `Archive-Huge/Coding`
- Capability: Coding LLM
- Runtime: llama.cpp for GGUF; transformers/vLLM for safetensors archive.
- Runnable status: `archive_only`
- Keep status: `strategic_archive`
- Size: `29.05 GiB`; payload files: `17`
- Recommended use: Local coding assistant, code generation, code review.
- Notes: GGUF quants are the most likely current runnable path.

### `Kimi-K3`

- Repo: `moonshotai/Kimi-K3`
- Location: `Archive-Huge/LLM`
- Capability: LLM / reasoning-chat
- Runtime: llama.cpp for GGUF; transformers/vLLM for safetensors archives.
- Runnable status: `archive_only`
- Keep status: `strategic_archive`
- Size: `1453.79 GiB`; payload files: `119`
- Recommended use: Local chat, reasoning, drafting, agent backend.
- Notes: Benchmark tokens/sec and answer quality before choosing default.

### `Llama-2-7b-chat-hf`

- Repo: `meta-llama/Llama-2-7b-chat-hf`
- Location: `Archive-Huge/LLM`
- Capability: LLM / reasoning-chat
- Runtime: llama.cpp for GGUF; transformers/vLLM for safetensors archives.
- Runnable status: `archive_only`
- Keep status: `strategic_archive`
- Size: `25.11 GiB`; payload files: `17`
- Recommended use: Local chat, reasoning, drafting, agent backend.
- Notes: Benchmark tokens/sec and answer quality before choosing default.

### `Llama-3.1-8B-Instruct`

- Repo: `meta-llama/Llama-3.1-8B-Instruct`
- Location: `Archive-Huge/LLM`
- Capability: LLM / reasoning-chat
- Runtime: llama.cpp for GGUF; transformers/vLLM for safetensors archives.
- Runnable status: `archive_only`
- Keep status: `strategic_archive`
- Size: `29.93 GiB`; payload files: `18`
- Recommended use: Local chat, reasoning, drafting, agent backend.
- Notes: Benchmark tokens/sec and answer quality before choosing default.

### `Llama-3.2-1B-Instruct`

- Repo: `meta-llama/Llama-3.2-1B-Instruct`
- Location: `Archive-Huge/LLM`
- Capability: LLM / reasoning-chat
- Runtime: llama.cpp for GGUF; transformers/vLLM for safetensors archives.
- Runnable status: `archive_only`
- Keep status: `strategic_archive`
- Size: `4.61 GiB`; payload files: `14`
- Recommended use: Local chat, reasoning, drafting, agent backend.
- Notes: Benchmark tokens/sec and answer quality before choosing default.

### `Meta-Llama-3-8B`

- Repo: `meta-llama/Meta-Llama-3-8B`
- Location: `Archive-Huge/LLM`
- Capability: LLM / reasoning-chat
- Runtime: llama.cpp for GGUF; transformers/vLLM for safetensors archives.
- Runnable status: `archive_only`
- Keep status: `strategic_archive`
- Size: `29.93 GiB`; payload files: `18`
- Recommended use: Local chat, reasoning, drafting, agent backend.
- Notes: Benchmark tokens/sec and answer quality before choosing default.

### `Qwen-AgentWorld-35B-A3B`

- Repo: `Qwen/Qwen-AgentWorld-35B-A3B`
- Location: `Archive-Huge/Multimodal`
- Capability: LLM / reasoning-chat
- Runtime: llama.cpp for GGUF; transformers/vLLM for safetensors archives.
- Runnable status: `archive_only`
- Keep status: `strategic_archive`
- Size: `64.58 GiB`; payload files: `36`
- Recommended use: Local chat, reasoning, drafting, agent backend.
- Notes: Benchmark tokens/sec and answer quality before choosing default.

### `Qwen2.5-VL-3B-Instruct`

- Repo: `Qwen/Qwen2.5-VL-3B-Instruct`
- Location: `Archive-Huge/Multimodal`
- Capability: LLM / reasoning-chat
- Runtime: llama.cpp for GGUF; transformers/vLLM for safetensors archives.
- Runnable status: `archive_only`
- Keep status: `strategic_archive`
- Size: `7.00 GiB`; payload files: `15`
- Recommended use: Local chat, reasoning, drafting, agent backend.
- Notes: Benchmark tokens/sec and answer quality before choosing default.

### `Qwen2.5-VL-7B-Instruct`

- Repo: `Qwen/Qwen2.5-VL-7B-Instruct`
- Location: `Archive-Huge/Multimodal`
- Capability: LLM / reasoning-chat
- Runtime: llama.cpp for GGUF; transformers/vLLM for safetensors archives.
- Runnable status: `archive_only`
- Keep status: `strategic_archive`
- Size: `15.46 GiB`; payload files: `17`
- Recommended use: Local chat, reasoning, drafting, agent backend.
- Notes: Benchmark tokens/sec and answer quality before choosing default.

### `Qwen3.6-35B-A3B-FP8`

- Repo: `Qwen/Qwen3.6-35B-A3B-FP8`
- Location: `Archive-Huge/Multimodal`
- Capability: LLM / reasoning-chat
- Runtime: llama.cpp for GGUF; transformers/vLLM for safetensors archives.
- Runnable status: `archive_only`
- Keep status: `strategic_archive`
- Size: `33.45 GiB`; payload files: `57`
- Recommended use: Local chat, reasoning, drafting, agent backend.
- Notes: Benchmark tokens/sec and answer quality before choosing default.

### `personaplex-7b-v1`

- Repo: `nvidia/personaplex-7b-v1`
- Location: `Audio`
- Capability: Audio generation / audio model
- Runtime: Model-specific audio/diffusers stack.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `15.96 GiB`; payload files: `17`
- Recommended use: Audio/music/SFX generation or audio-specific workflows.
- Notes: Needs model-specific generation smoke test.

### `stable-audio-3-medium`

- Repo: `stabilityai/stable-audio-3-medium`
- Location: `Audio`
- Capability: Audio generation / audio model
- Runtime: Model-specific audio/diffusers stack.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `9.73 GiB`; payload files: `18`
- Recommended use: Audio/music/SFX generation or audio-specific workflows.
- Notes: Needs model-specific generation smoke test.

### `stable-audio-3-small-sfx`

- Repo: `stabilityai/stable-audio-3-small-sfx`
- Location: `Audio`
- Capability: Audio generation / audio model
- Runtime: Model-specific audio/diffusers stack.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `3.25 GiB`; payload files: `18`
- Recommended use: Audio/music/SFX generation or audio-specific workflows.
- Notes: Needs model-specific generation smoke test.

### `stable-audio-open-1.0`

- Repo: `stabilityai/stable-audio-open-1.0`
- Location: `Audio`
- Capability: Audio generation / audio model
- Runtime: Model-specific audio/diffusers stack.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `14.60 GiB`; payload files: `26`
- Recommended use: Audio/music/SFX generation or audio-specific workflows.
- Notes: Needs model-specific generation smoke test.

### `Qwen3-Coder-30B-A3B-UD-Q4_K_XL`

- Repo: `unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF`
- Location: `Coding`
- Capability: Coding LLM
- Runtime: llama.cpp for GGUF; transformers/vLLM for safetensors archive.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `16.45 GiB`; payload files: `2`
- Recommended use: Local coding assistant, code generation, code review.
- Notes: GGUF quants are the most likely current runnable path.

### `Qwen3-Coder-Next-Q4_K_M`

- Repo: `DanyDA/unsloth_Qwen3-Coder-Next-Q4_K_M-GGUF-SPLIT`
- Location: `Coding`
- Capability: Coding LLM
- Runtime: llama.cpp for GGUF; transformers/vLLM for safetensors archive.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `45.09 GiB`; payload files: `5`
- Recommended use: Local coding assistant, code generation, code review.
- Notes: GGUF quants are the most likely current runnable path.

### `FLUX.1-dev`

- Repo: `black-forest-labs/FLUX.1-dev`
- Location: `Diffusion-Image`
- Capability: Image generation/editing
- Runtime: ComfyUI or diffusers.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `60.59 GiB`; payload files: `30`
- Recommended use: Text-to-image, image editing, diffusion workflows.
- Notes: Use ComfyUI/diffusers smoke workflow to confirm exact pipeline support.

### `FLUX.1-Fill-dev`

- Repo: `black-forest-labs/FLUX.1-Fill-dev`
- Location: `Diffusion-Image`
- Capability: Image generation/editing
- Runtime: ComfyUI or diffusers.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `54.07 GiB`; payload files: `29`
- Recommended use: Text-to-image, image editing, diffusion workflows.
- Notes: Use ComfyUI/diffusers smoke workflow to confirm exact pipeline support.

### `FLUX.1-Kontext-dev`

- Repo: `black-forest-labs/FLUX.1-Kontext-dev`
- Location: `Diffusion-Image`
- Capability: Image generation/editing
- Runtime: ComfyUI or diffusers.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `53.92 GiB`; payload files: `30`
- Recommended use: Text-to-image, image editing, diffusion workflows.
- Notes: Use ComfyUI/diffusers smoke workflow to confirm exact pipeline support.

### `FLUX.1-schnell`

- Repo: `black-forest-labs/FLUX.1-schnell`
- Location: `Diffusion-Image`
- Capability: Image generation/editing
- Runtime: ComfyUI or diffusers.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `53.87 GiB`; payload files: `29`
- Recommended use: Text-to-image, image editing, diffusion workflows.
- Notes: Use ComfyUI/diffusers smoke workflow to confirm exact pipeline support.

### `FLUX.2-dev`

- Repo: `black-forest-labs/FLUX.2-dev`
- Location: `Diffusion-Image`
- Capability: Image generation/editing
- Runtime: ComfyUI or diffusers.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `165.44 GiB`; payload files: `40`
- Recommended use: Text-to-image, image editing, diffusion workflows.
- Notes: Use ComfyUI/diffusers smoke workflow to confirm exact pipeline support. Large active model; confirm storage/runtime value periodically.

### `FLUX.2-klein-9B`

- Repo: `black-forest-labs/FLUX.2-klein-9B`
- Location: `Diffusion-Image`
- Capability: Image generation/editing
- Runtime: ComfyUI or diffusers.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `49.26 GiB`; payload files: `30`
- Recommended use: Text-to-image, image editing, diffusion workflows.
- Notes: Use ComfyUI/diffusers smoke workflow to confirm exact pipeline support.

### `FLUX.2-klein-9b-fp8`

- Repo: `black-forest-labs/FLUX.2-klein-9b-fp8`
- Location: `Diffusion-Image`
- Capability: Image generation/editing
- Runtime: ComfyUI or diffusers.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `8.79 GiB`; payload files: `8`
- Recommended use: Text-to-image, image editing, diffusion workflows.
- Notes: Use ComfyUI/diffusers smoke workflow to confirm exact pipeline support.

### `stable-diffusion-3-medium`

- Repo: `stabilityai/stable-diffusion-3-medium`
- Location: `Diffusion-Image`
- Capability: Image generation/editing
- Runtime: ComfyUI or diffusers.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `49.66 GiB`; payload files: `29`
- Recommended use: Text-to-image, image editing, diffusion workflows.
- Notes: Use ComfyUI/diffusers smoke workflow to confirm exact pipeline support.

### `stable-diffusion-3.5-large`

- Repo: `stabilityai/stable-diffusion-3.5-large`
- Location: `Diffusion-Image`
- Capability: Image generation/editing
- Runtime: ComfyUI or diffusers.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `66.67 GiB`; payload files: `46`
- Recommended use: Text-to-image, image editing, diffusion workflows.
- Notes: Use ComfyUI/diffusers smoke workflow to confirm exact pipeline support.

### `all-MiniLM-L12-v2`

- Repo: `sentence-transformers/all-MiniLM-L12-v2`
- Location: `Embeddings`
- Capability: Embeddings / retrieval
- Runtime: sentence-transformers or transformers; GGUF embedding runtime for GGUF quants.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `1.21 GiB`; payload files: `30`
- Recommended use: Semantic search, RAG retrieval, clustering, similarity.
- Notes: Benchmark retrieval quality and latency before choosing default RAG embedding.

### `all-MiniLM-L6-v2`

- Repo: `sentence-transformers/all-MiniLM-L6-v2`
- Location: `Embeddings`
- Capability: Embeddings / retrieval
- Runtime: sentence-transformers or transformers; GGUF embedding runtime for GGUF quants.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `0.83 GiB`; payload files: `30`
- Recommended use: Semantic search, RAG retrieval, clustering, similarity.
- Notes: Benchmark retrieval quality and latency before choosing default RAG embedding.

### `all-mpnet-base-v2`

- Repo: `sentence-transformers/all-mpnet-base-v2`
- Location: `Embeddings`
- Capability: Embeddings / retrieval
- Runtime: sentence-transformers or transformers; GGUF embedding runtime for GGUF quants.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `3.56 GiB`; payload files: `29`
- Recommended use: Semantic search, RAG retrieval, clustering, similarity.
- Notes: Benchmark retrieval quality and latency before choosing default RAG embedding.

### `embeddinggemma-300m`

- Repo: `google/embeddinggemma-300m`
- Location: `Embeddings`
- Capability: Embeddings / retrieval
- Runtime: sentence-transformers or transformers; GGUF embedding runtime for GGUF quants.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `1.18 GiB`; payload files: `20`
- Recommended use: Semantic search, RAG retrieval, clustering, similarity.
- Notes: Benchmark retrieval quality and latency before choosing default RAG embedding.

### `paraphrase-multilingual-MiniLM-L12-v2`

- Repo: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- Location: `Embeddings`
- Capability: Embeddings / retrieval
- Runtime: sentence-transformers or transformers; GGUF embedding runtime for GGUF quants.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `3.87 GiB`; payload files: `28`
- Recommended use: Semantic search, RAG retrieval, clustering, similarity.
- Notes: Benchmark retrieval quality and latency before choosing default RAG embedding.

### `paraphrase-multilingual-mpnet-base-v2`

- Repo: `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`
- Location: `Embeddings`
- Capability: Embeddings / retrieval
- Runtime: sentence-transformers or transformers; GGUF embedding runtime for GGUF quants.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `9.07 GiB`; payload files: `27`
- Recommended use: Semantic search, RAG retrieval, clustering, similarity.
- Notes: Benchmark retrieval quality and latency before choosing default RAG embedding.

### `Qwen3-Embedding-8B-Q4_K_M`

- Repo: `enacimie/Qwen3-Embedding-8B-Q4_K_M-GGUF`
- Location: `Embeddings`
- Capability: Embeddings / retrieval
- Runtime: sentence-transformers or transformers; GGUF embedding runtime for GGUF quants.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `4.36 GiB`; payload files: `2`
- Recommended use: Semantic search, RAG retrieval, clustering, similarity.
- Notes: Benchmark retrieval quality and latency before choosing default RAG embedding.

### `Qwen3-VL-Embedding-8B`

- Repo: `Qwen/Qwen3-VL-Embedding-8B`
- Location: `Embeddings`
- Capability: Embeddings / retrieval
- Runtime: sentence-transformers or transformers; GGUF embedding runtime for GGUF quants.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `15.19 GiB`; payload files: `23`
- Recommended use: Semantic search, RAG retrieval, clustering, similarity.
- Notes: Benchmark retrieval quality and latency before choosing default RAG embedding.

### `DeepSeek-R1-Distill-Qwen-32B-Q5_K_M`

- Repo: `roleplaiapp/DeepSeek-R1-Distill-Qwen-32B-Q5_K_M-GGUF`
- Location: `LLM`
- Capability: LLM / reasoning-chat
- Runtime: llama.cpp for GGUF; transformers/vLLM for safetensors archives.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `21.66 GiB`; payload files: `2`
- Recommended use: Local chat, reasoning, drafting, agent backend.
- Notes: Benchmark tokens/sec and answer quality before choosing default.

### `Gemma-3-27B-QAT-Q4_0`

- Repo: `google/gemma-3-27b-it-qat-q4_0-gguf`
- Location: `LLM`
- Capability: LLM / reasoning-chat
- Runtime: llama.cpp for GGUF; transformers/vLLM for safetensors archives.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `16.05 GiB`; payload files: `2`
- Recommended use: Local chat, reasoning, drafting, agent backend.
- Notes: Benchmark tokens/sec and answer quality before choosing default.

### `GLM-4.7-Flash-Q4_K_M`

- Repo: `yybl/Qwen3-30B-A3B-Thinking-2507-GLM-4.7-Flash-High-Reasoning-Q4_K_M-GGUF`
- Location: `LLM`
- Capability: LLM / reasoning-chat
- Runtime: llama.cpp for GGUF; transformers/vLLM for safetensors archives.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `17.21 GiB`; payload files: `2`
- Recommended use: Local chat, reasoning, drafting, agent backend.
- Notes: Benchmark tokens/sec and answer quality before choosing default.

### `GPT-OSS-20B`

- Repo: `openai/gpt-oss-20b`
- Location: `LLM`
- Capability: LLM / reasoning-chat
- Runtime: llama.cpp for GGUF; transformers/vLLM for safetensors archives.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `38.47 GiB`; payload files: `19`
- Recommended use: Local chat, reasoning, drafting, agent backend.
- Notes: Benchmark tokens/sec and answer quality before choosing default.

### `Ministral-3-14B-Q5_K_M`

- Repo: `NikolayKozloff/Ministral-3-14B-Reasoning-2512-Q5_K_M-GGUF`
- Location: `LLM`
- Capability: LLM / reasoning-chat
- Runtime: llama.cpp for GGUF; transformers/vLLM for safetensors archives.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `8.96 GiB`; payload files: `2`
- Recommended use: Local chat, reasoning, drafting, agent backend.
- Notes: Benchmark tokens/sec and answer quality before choosing default.

### `Qwen3-32B-Q5_K_M`

- Repo: `jacobcarajo/Qwen3-32B-Q5_K_M-GGUF`
- Location: `LLM`
- Capability: LLM / reasoning-chat
- Runtime: llama.cpp for GGUF; transformers/vLLM for safetensors archives.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `21.62 GiB`; payload files: `2`
- Recommended use: Local chat, reasoning, drafting, agent backend.
- Notes: Benchmark tokens/sec and answer quality before choosing default.

### `Qwen3.6-35B-A3B-NVFP4`

- Repo: `nvidia/Qwen3.6-35B-A3B-NVFP4`
- Location: `LLM`
- Capability: LLM / reasoning-chat
- Runtime: llama.cpp for GGUF; transformers/vLLM for safetensors archives.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `21.85 GiB`; payload files: `18`
- Recommended use: Local chat, reasoning, drafting, agent backend.
- Notes: Benchmark tokens/sec and answer quality before choosing default.

### `Qwen3.6-35B-A3B-UD-Q4_K_M`

- Repo: `juan1995-dev/Qwen3.6-35B-A3B-UD-Q4_K_M_GGUF`
- Location: `LLM`
- Capability: LLM / reasoning-chat
- Runtime: llama.cpp for GGUF; transformers/vLLM for safetensors archives.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `20.61 GiB`; payload files: `2`
- Recommended use: Local chat, reasoning, drafting, agent backend.
- Notes: Benchmark tokens/sec and answer quality before choosing default.

### `Prompt-Guard-86M`

- Repo: `meta-llama/Prompt-Guard-86M`
- Location: `Safety-Moderation`
- Capability: Prompt safety / moderation
- Runtime: transformers sequence-classification.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `1.05 GiB`; payload files: `12`
- Recommended use: Prompt-injection and jailbreak risk classifier for agents/RAG.
- Notes: Good candidate for default safety guardrail once transformers/torch runtime is installed.

### `nemotron-3.5-asr-streaming-0.6b`

- Repo: `nvidia/nemotron-3.5-asr-streaming-0.6b`
- Location: `Speech-STT`
- Capability: Speech-to-text
- Runtime: faster-whisper preferred; transformers fallback.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `5.27 GiB`; payload files: `23`
- Recommended use: Transcription and speech recognition.
- Notes: Keep v2 only if benchmark shows accuracy/use-case value over v3/v3-turbo.

### `whisper-large-v2`

- Repo: `openai/whisper-large-v2`
- Location: `Speech-STT`
- Capability: Speech-to-text
- Runtime: faster-whisper preferred; transformers fallback.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `review_after_benchmark`
- Size: `23.00 GiB`; payload files: `17`
- Recommended use: Transcription and speech recognition.
- Notes: Keep v2 only if benchmark shows accuracy/use-case value over v3/v3-turbo.

### `whisper-large-v3`

- Repo: `openai/whisper-large-v3`
- Location: `Speech-STT`
- Capability: Speech-to-text
- Runtime: faster-whisper preferred; transformers fallback.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `23.01 GiB`; payload files: `22`
- Recommended use: Transcription and speech recognition.
- Notes: Keep v2 only if benchmark shows accuracy/use-case value over v3/v3-turbo.

### `whisper-large-v3-turbo`

- Repo: `openai/whisper-large-v3-turbo`
- Location: `Speech-STT`
- Capability: Speech-to-text
- Runtime: faster-whisper preferred; transformers fallback.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `1.51 GiB`; payload files: `14`
- Recommended use: Transcription and speech recognition.
- Notes: Keep v2 only if benchmark shows accuracy/use-case value over v3/v3-turbo.

### `stable-video-diffusion-img2vid-xt-1-1`

- Repo: `stabilityai/stable-video-diffusion-img2vid-xt-1-1`
- Location: `Video`
- Capability: Video generation
- Runtime: ComfyUI or diffusers Stable Video pipeline.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `17.06 GiB`; payload files: `18`
- Recommended use: Image-to-video generation.
- Notes: Verified structurally; runtime test needs diffusion stack.

### `DeepSeek-OCR-2`

- Repo: `deepseek-ai/DeepSeek-OCR-2`
- Location: `Vision-OCR`
- Capability: OCR / document extraction
- Runtime: transformers/custom model code, likely GPU/accelerator dependent.
- Runnable status: `runnable_with_runtime_install`
- Keep status: `active`
- Size: `6.32 GiB`; payload files: `17`
- Recommended use: Image/PDF text extraction and document understanding.
- Notes: Needs a known sample-image benchmark.
