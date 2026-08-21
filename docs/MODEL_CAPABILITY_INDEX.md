# Model Capability Index

This is a decision layer for the model file server. It describes what each verified library folder is for, how valuable it is to transfer to the separate AI box, and what runtime the AI box is likely to need.

## Status meanings

| Status | Meaning |
|---|---|
| `verified_file_server_copy` | The model folder is present, named, categorized, metadata-complete, and structurally verified on the file server. |
| `high` | Strong candidate to copy to the AI box soon. |
| `medium` | Useful, but copy when a specific test/workflow needs it. |
| `archive_only` | Keep on file server; do not routinely transfer to AI box. |
| `review` | Needs manual purpose/runtime review first. |

## Capability cards

| Location | Model | Capability | Transfer priority | Keep status | AI-box runtime | Size | Use |
|---|---|---|---|---|---|---:|---|
| Archive-Huge/Coding | `Qwen3-Coder-30B-A3B-Instruct` | Coding LLM | `archive_only` | `strategic_archive` | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archive. | 57.17 GiB | Move to AI box for local coding assistant/code generation tests. |
| Archive-Huge/Coding | `Qwen3-Coder-30B-A3B-Instruct-FP8` | Coding LLM | `archive_only` | `strategic_archive` | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archive. | 29.05 GiB | Move to AI box for local coding assistant/code generation tests. |
| Archive-Huge/LLM | `Kimi-K3` | LLM / reasoning-chat | `archive_only` | `strategic_archive` | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | 1453.79 GiB | Move to AI box for chat, reasoning, drafting, and agent-backend trials. |
| Archive-Huge/LLM | `Llama-2-7b-chat-hf` | LLM / reasoning-chat | `archive_only` | `strategic_archive` | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | 25.11 GiB | Move to AI box for chat, reasoning, drafting, and agent-backend trials. |
| Archive-Huge/LLM | `Llama-3.1-8B-Instruct` | LLM / reasoning-chat | `archive_only` | `strategic_archive` | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | 29.93 GiB | Move to AI box for chat, reasoning, drafting, and agent-backend trials. |
| Archive-Huge/LLM | `Llama-3.2-1B-Instruct` | LLM / reasoning-chat | `archive_only` | `strategic_archive` | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | 4.61 GiB | Move to AI box for chat, reasoning, drafting, and agent-backend trials. |
| Archive-Huge/LLM | `Meta-Llama-3-8B` | LLM / reasoning-chat | `archive_only` | `strategic_archive` | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | 29.93 GiB | Move to AI box for chat, reasoning, drafting, and agent-backend trials. |
| Archive-Huge/Multimodal | `Qwen-AgentWorld-35B-A3B` | Multimodal / vision-language | `archive_only` | `strategic_archive` | transformers/vLLM/custom multimodal runtime on AI box. | 64.58 GiB | Move to AI box for image-understanding/multimodal agent tests. |
| Archive-Huge/Multimodal | `Qwen2.5-VL-3B-Instruct` | Multimodal / vision-language | `archive_only` | `strategic_archive` | transformers/vLLM/custom multimodal runtime on AI box. | 7.00 GiB | Move to AI box for image-understanding/multimodal agent tests. |
| Archive-Huge/Multimodal | `Qwen2.5-VL-7B-Instruct` | Multimodal / vision-language | `archive_only` | `strategic_archive` | transformers/vLLM/custom multimodal runtime on AI box. | 15.46 GiB | Move to AI box for image-understanding/multimodal agent tests. |
| Archive-Huge/Multimodal | `Qwen3.6-35B-A3B-FP8` | Multimodal / vision-language | `archive_only` | `strategic_archive` | transformers/vLLM/custom multimodal runtime on AI box. | 33.45 GiB | Move to AI box for image-understanding/multimodal agent tests. |
| Audio | `personaplex-7b-v1` | Audio generation / audio model | `medium` | `active` | Model-specific audio/diffusers stack on AI box. | 15.96 GiB | Move to AI box for audio/music/SFX model-specific workflows. |
| Audio | `stable-audio-3-medium` | Audio generation / audio model | `medium` | `active` | Model-specific audio/diffusers stack on AI box. | 9.73 GiB | Move to AI box for audio/music/SFX model-specific workflows. |
| Audio | `stable-audio-3-small-sfx` | Audio generation / audio model | `medium` | `active` | Model-specific audio/diffusers stack on AI box. | 3.25 GiB | Move to AI box for audio/music/SFX model-specific workflows. |
| Audio | `stable-audio-open-1.0` | Audio generation / audio model | `medium` | `active` | Model-specific audio/diffusers stack on AI box. | 14.60 GiB | Move to AI box for audio/music/SFX model-specific workflows. |
| Coding | `Qwen3-Coder-30B-A3B-UD-Q4_K_XL` | Coding LLM | `high` | `active` | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archive. | 16.45 GiB | Move to AI box for local coding assistant/code generation tests. |
| Coding | `Qwen3-Coder-Next-Q4_K_M` | Coding LLM | `high` | `active` | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archive. | 45.09 GiB | Move to AI box for local coding assistant/code generation tests. |
| Diffusion-Image | `FLUX.1-dev` | Image generation/editing | `medium` | `active` | ComfyUI or diffusers on AI box. | 60.59 GiB | Move to AI box for ComfyUI/diffusers image generation and editing. |
| Diffusion-Image | `FLUX.1-Fill-dev` | Image generation/editing | `medium` | `active` | ComfyUI or diffusers on AI box. | 54.07 GiB | Move to AI box for ComfyUI/diffusers image generation and editing. |
| Diffusion-Image | `FLUX.1-Kontext-dev` | Image generation/editing | `medium` | `active` | ComfyUI or diffusers on AI box. | 53.92 GiB | Move to AI box for ComfyUI/diffusers image generation and editing. |
| Diffusion-Image | `FLUX.1-schnell` | Image generation/editing | `high` | `active` | ComfyUI or diffusers on AI box. | 53.87 GiB | Move to AI box for ComfyUI/diffusers image generation and editing. |
| Diffusion-Image | `FLUX.2-dev` | Image generation/editing | `medium` | `active` | ComfyUI or diffusers on AI box. | 165.44 GiB | Move to AI box for ComfyUI/diffusers image generation and editing. |
| Diffusion-Image | `FLUX.2-klein-9B` | Image generation/editing | `high` | `active` | ComfyUI or diffusers on AI box. | 49.26 GiB | Move to AI box for ComfyUI/diffusers image generation and editing. |
| Diffusion-Image | `FLUX.2-klein-9b-fp8` | Image generation/editing | `high` | `active` | ComfyUI or diffusers on AI box. | 8.79 GiB | Move to AI box for ComfyUI/diffusers image generation and editing. |
| Diffusion-Image | `stable-diffusion-3-medium` | Image generation/editing | `medium` | `active` | ComfyUI or diffusers on AI box. | 49.66 GiB | Move to AI box for ComfyUI/diffusers image generation and editing. |
| Diffusion-Image | `stable-diffusion-3.5-large` | Image generation/editing | `medium` | `active` | ComfyUI or diffusers on AI box. | 66.67 GiB | Move to AI box for ComfyUI/diffusers image generation and editing. |
| Embeddings | `all-MiniLM-L12-v2` | Embeddings / retrieval | `medium` | `active` | sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants. | 1.21 GiB | Move to AI box for semantic search, RAG retrieval, clustering, similarity. |
| Embeddings | `all-MiniLM-L6-v2` | Embeddings / retrieval | `high` | `active` | sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants. | 0.83 GiB | Move to AI box for semantic search, RAG retrieval, clustering, similarity. |
| Embeddings | `all-mpnet-base-v2` | Embeddings / retrieval | `high` | `active` | sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants. | 3.56 GiB | Move to AI box for semantic search, RAG retrieval, clustering, similarity. |
| Embeddings | `embeddinggemma-300m` | Embeddings / retrieval | `medium` | `active` | sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants. | 1.18 GiB | Move to AI box for semantic search, RAG retrieval, clustering, similarity. |
| Embeddings | `paraphrase-multilingual-MiniLM-L12-v2` | Embeddings / retrieval | `medium` | `active` | sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants. | 3.87 GiB | Move to AI box for semantic search, RAG retrieval, clustering, similarity. |
| Embeddings | `paraphrase-multilingual-mpnet-base-v2` | Embeddings / retrieval | `high` | `active` | sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants. | 9.07 GiB | Move to AI box for semantic search, RAG retrieval, clustering, similarity. |
| Embeddings | `Qwen3-Embedding-8B-Q4_K_M` | Embeddings / retrieval | `medium` | `active` | sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants. | 4.36 GiB | Move to AI box for semantic search, RAG retrieval, clustering, similarity. |
| Embeddings | `Qwen3-VL-Embedding-8B` | Embeddings / retrieval | `medium` | `active` | sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants. | 15.19 GiB | Move to AI box for semantic search, RAG retrieval, clustering, similarity. |
| LLM | `DeepSeek-R1-Distill-Qwen-32B-Q5_K_M` | LLM / reasoning-chat | `high` | `active` | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | 21.66 GiB | Move to AI box for chat, reasoning, drafting, and agent-backend trials. |
| LLM | `Gemma-3-27B-QAT-Q4_0` | LLM / reasoning-chat | `medium` | `active` | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | 16.05 GiB | Move to AI box for chat, reasoning, drafting, and agent-backend trials. |
| LLM | `GLM-4.7-Flash-Q4_K_M` | LLM / reasoning-chat | `high` | `active` | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | 17.21 GiB | Move to AI box for chat, reasoning, drafting, and agent-backend trials. |
| LLM | `GPT-OSS-20B` | LLM / reasoning-chat | `high` | `active` | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | 38.47 GiB | Move to AI box for chat, reasoning, drafting, and agent-backend trials. |
| LLM | `Ministral-3-14B-Q5_K_M` | LLM / reasoning-chat | `high` | `active` | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | 8.96 GiB | Move to AI box for chat, reasoning, drafting, and agent-backend trials. |
| LLM | `Qwen3-32B-Q5_K_M` | LLM / reasoning-chat | `high` | `active` | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | 21.62 GiB | Move to AI box for chat, reasoning, drafting, and agent-backend trials. |
| LLM | `Qwen3.6-35B-A3B-NVFP4` | LLM / reasoning-chat | `high` | `active` | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | 21.85 GiB | Move to AI box for chat, reasoning, drafting, and agent-backend trials. |
| LLM | `Qwen3.6-35B-A3B-UD-Q4_K_M` | LLM / reasoning-chat | `high` | `active` | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | 20.61 GiB | Move to AI box for chat, reasoning, drafting, and agent-backend trials. |
| Safety-Moderation | `Prompt-Guard-86M` | Prompt safety / moderation | `high` | `active` | transformers sequence-classification on AI box. | 1.05 GiB | Move to AI box for prompt-injection and jailbreak checks in agents/RAG. |
| Speech-STT | `nemotron-3.5-asr-streaming-0.6b` | Speech-to-text | `medium` | `active` | faster-whisper preferred; transformers fallback on AI box. | 5.27 GiB | Move to AI box for transcription/STT testing. |
| Speech-STT | `whisper-large-v2` | Speech-to-text | `medium` | `review_after_benchmark` | faster-whisper preferred; transformers fallback on AI box. | 23.00 GiB | Move to AI box for transcription/STT testing. |
| Speech-STT | `whisper-large-v3` | Speech-to-text | `medium` | `active` | faster-whisper preferred; transformers fallback on AI box. | 23.01 GiB | Move to AI box for transcription/STT testing. |
| Speech-STT | `whisper-large-v3-turbo` | Speech-to-text | `high` | `active` | faster-whisper preferred; transformers fallback on AI box. | 1.51 GiB | Move to AI box for transcription/STT testing. |
| Video | `stable-video-diffusion-img2vid-xt-1-1` | Video generation | `medium` | `active` | ComfyUI or diffusers Stable Video pipeline on AI box. | 17.06 GiB | Move to AI box for image-to-video generation workflows. |
| Vision-OCR | `DeepSeek-OCR-2` | OCR / document extraction | `medium` | `active` | transformers/custom model code on AI box. | 6.32 GiB | Move to AI box for image/PDF text extraction experiments. |

## Notes by model

### `Qwen3-Coder-30B-A3B-Instruct`

- Repo: `Qwen/Qwen3-Coder-30B-A3B-Instruct`
- Location: `Archive-Huge/Coding`
- Capability: Coding LLM
- Library status: `verified_file_server_copy`
- Transfer priority: `archive_only`
- Keep status: `strategic_archive`
- AI-box runtime: llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archive.
- Size: `57.17 GiB`; payload files: `29`
- Recommended use: Move to AI box for local coding assistant/code generation tests.
- Notes: Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. GGUF quants are likely the most useful current AI-box transfer candidates.

### `Qwen3-Coder-30B-A3B-Instruct-FP8`

- Repo: `Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8`
- Location: `Archive-Huge/Coding`
- Capability: Coding LLM
- Library status: `verified_file_server_copy`
- Transfer priority: `archive_only`
- Keep status: `strategic_archive`
- AI-box runtime: llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archive.
- Size: `29.05 GiB`; payload files: `17`
- Recommended use: Move to AI box for local coding assistant/code generation tests.
- Notes: Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. GGUF quants are likely the most useful current AI-box transfer candidates.

### `Kimi-K3`

- Repo: `moonshotai/Kimi-K3`
- Location: `Archive-Huge/LLM`
- Capability: LLM / reasoning-chat
- Library status: `verified_file_server_copy`
- Transfer priority: `archive_only`
- Keep status: `strategic_archive`
- AI-box runtime: llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives.
- Size: `1453.79 GiB`; payload files: `119`
- Recommended use: Move to AI box for chat, reasoning, drafting, and agent-backend trials.
- Notes: Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. Benchmark tokens/sec and answer quality on the AI box before setting defaults.

### `Llama-2-7b-chat-hf`

- Repo: `meta-llama/Llama-2-7b-chat-hf`
- Location: `Archive-Huge/LLM`
- Capability: LLM / reasoning-chat
- Library status: `verified_file_server_copy`
- Transfer priority: `archive_only`
- Keep status: `strategic_archive`
- AI-box runtime: llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives.
- Size: `25.11 GiB`; payload files: `17`
- Recommended use: Move to AI box for chat, reasoning, drafting, and agent-backend trials.
- Notes: Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. Benchmark tokens/sec and answer quality on the AI box before setting defaults.

### `Llama-3.1-8B-Instruct`

- Repo: `meta-llama/Llama-3.1-8B-Instruct`
- Location: `Archive-Huge/LLM`
- Capability: LLM / reasoning-chat
- Library status: `verified_file_server_copy`
- Transfer priority: `archive_only`
- Keep status: `strategic_archive`
- AI-box runtime: llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives.
- Size: `29.93 GiB`; payload files: `18`
- Recommended use: Move to AI box for chat, reasoning, drafting, and agent-backend trials.
- Notes: Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. Benchmark tokens/sec and answer quality on the AI box before setting defaults.

### `Llama-3.2-1B-Instruct`

- Repo: `meta-llama/Llama-3.2-1B-Instruct`
- Location: `Archive-Huge/LLM`
- Capability: LLM / reasoning-chat
- Library status: `verified_file_server_copy`
- Transfer priority: `archive_only`
- Keep status: `strategic_archive`
- AI-box runtime: llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives.
- Size: `4.61 GiB`; payload files: `14`
- Recommended use: Move to AI box for chat, reasoning, drafting, and agent-backend trials.
- Notes: Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. Benchmark tokens/sec and answer quality on the AI box before setting defaults.

### `Meta-Llama-3-8B`

- Repo: `meta-llama/Meta-Llama-3-8B`
- Location: `Archive-Huge/LLM`
- Capability: LLM / reasoning-chat
- Library status: `verified_file_server_copy`
- Transfer priority: `archive_only`
- Keep status: `strategic_archive`
- AI-box runtime: llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives.
- Size: `29.93 GiB`; payload files: `18`
- Recommended use: Move to AI box for chat, reasoning, drafting, and agent-backend trials.
- Notes: Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. Benchmark tokens/sec and answer quality on the AI box before setting defaults.

### `Qwen-AgentWorld-35B-A3B`

- Repo: `Qwen/Qwen-AgentWorld-35B-A3B`
- Location: `Archive-Huge/Multimodal`
- Capability: Multimodal / vision-language
- Library status: `verified_file_server_copy`
- Transfer priority: `archive_only`
- Keep status: `strategic_archive`
- AI-box runtime: transformers/vLLM/custom multimodal runtime on AI box.
- Size: `64.58 GiB`; payload files: `36`
- Recommended use: Move to AI box for image-understanding/multimodal agent tests.
- Notes: Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. Requires AI-box multimodal runtime compatibility test.

### `Qwen2.5-VL-3B-Instruct`

- Repo: `Qwen/Qwen2.5-VL-3B-Instruct`
- Location: `Archive-Huge/Multimodal`
- Capability: Multimodal / vision-language
- Library status: `verified_file_server_copy`
- Transfer priority: `archive_only`
- Keep status: `strategic_archive`
- AI-box runtime: transformers/vLLM/custom multimodal runtime on AI box.
- Size: `7.00 GiB`; payload files: `15`
- Recommended use: Move to AI box for image-understanding/multimodal agent tests.
- Notes: Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. Requires AI-box multimodal runtime compatibility test.

### `Qwen2.5-VL-7B-Instruct`

- Repo: `Qwen/Qwen2.5-VL-7B-Instruct`
- Location: `Archive-Huge/Multimodal`
- Capability: Multimodal / vision-language
- Library status: `verified_file_server_copy`
- Transfer priority: `archive_only`
- Keep status: `strategic_archive`
- AI-box runtime: transformers/vLLM/custom multimodal runtime on AI box.
- Size: `15.46 GiB`; payload files: `17`
- Recommended use: Move to AI box for image-understanding/multimodal agent tests.
- Notes: Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. Requires AI-box multimodal runtime compatibility test.

### `Qwen3.6-35B-A3B-FP8`

- Repo: `Qwen/Qwen3.6-35B-A3B-FP8`
- Location: `Archive-Huge/Multimodal`
- Capability: Multimodal / vision-language
- Library status: `verified_file_server_copy`
- Transfer priority: `archive_only`
- Keep status: `strategic_archive`
- AI-box runtime: transformers/vLLM/custom multimodal runtime on AI box.
- Size: `33.45 GiB`; payload files: `57`
- Recommended use: Move to AI box for image-understanding/multimodal agent tests.
- Notes: Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. Requires AI-box multimodal runtime compatibility test.

### `personaplex-7b-v1`

- Repo: `nvidia/personaplex-7b-v1`
- Location: `Audio`
- Capability: Audio generation / audio model
- Library status: `verified_file_server_copy`
- Transfer priority: `medium`
- Keep status: `active`
- AI-box runtime: Model-specific audio/diffusers stack on AI box.
- Size: `15.96 GiB`; payload files: `17`
- Recommended use: Move to AI box for audio/music/SFX model-specific workflows.
- Notes: Needs model-specific AI-box generation smoke test.

### `stable-audio-3-medium`

- Repo: `stabilityai/stable-audio-3-medium`
- Location: `Audio`
- Capability: Audio generation / audio model
- Library status: `verified_file_server_copy`
- Transfer priority: `medium`
- Keep status: `active`
- AI-box runtime: Model-specific audio/diffusers stack on AI box.
- Size: `9.73 GiB`; payload files: `18`
- Recommended use: Move to AI box for audio/music/SFX model-specific workflows.
- Notes: Needs model-specific AI-box generation smoke test.

### `stable-audio-3-small-sfx`

- Repo: `stabilityai/stable-audio-3-small-sfx`
- Location: `Audio`
- Capability: Audio generation / audio model
- Library status: `verified_file_server_copy`
- Transfer priority: `medium`
- Keep status: `active`
- AI-box runtime: Model-specific audio/diffusers stack on AI box.
- Size: `3.25 GiB`; payload files: `18`
- Recommended use: Move to AI box for audio/music/SFX model-specific workflows.
- Notes: Needs model-specific AI-box generation smoke test.

### `stable-audio-open-1.0`

- Repo: `stabilityai/stable-audio-open-1.0`
- Location: `Audio`
- Capability: Audio generation / audio model
- Library status: `verified_file_server_copy`
- Transfer priority: `medium`
- Keep status: `active`
- AI-box runtime: Model-specific audio/diffusers stack on AI box.
- Size: `14.60 GiB`; payload files: `26`
- Recommended use: Move to AI box for audio/music/SFX model-specific workflows.
- Notes: Needs model-specific AI-box generation smoke test.

### `Qwen3-Coder-30B-A3B-UD-Q4_K_XL`

- Repo: `unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF`
- Location: `Coding`
- Capability: Coding LLM
- Library status: `verified_file_server_copy`
- Transfer priority: `high`
- Keep status: `active`
- AI-box runtime: llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archive.
- Size: `16.45 GiB`; payload files: `2`
- Recommended use: Move to AI box for local coding assistant/code generation tests.
- Notes: GGUF quants are likely the most useful current AI-box transfer candidates.

### `Qwen3-Coder-Next-Q4_K_M`

- Repo: `DanyDA/unsloth_Qwen3-Coder-Next-Q4_K_M-GGUF-SPLIT`
- Location: `Coding`
- Capability: Coding LLM
- Library status: `verified_file_server_copy`
- Transfer priority: `high`
- Keep status: `active`
- AI-box runtime: llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archive.
- Size: `45.09 GiB`; payload files: `5`
- Recommended use: Move to AI box for local coding assistant/code generation tests.
- Notes: GGUF quants are likely the most useful current AI-box transfer candidates.

### `FLUX.1-dev`

- Repo: `black-forest-labs/FLUX.1-dev`
- Location: `Diffusion-Image`
- Capability: Image generation/editing
- Library status: `verified_file_server_copy`
- Transfer priority: `medium`
- Keep status: `active`
- AI-box runtime: ComfyUI or diffusers on AI box.
- Size: `60.59 GiB`; payload files: `30`
- Recommended use: Move to AI box for ComfyUI/diffusers image generation and editing.
- Notes: Transfer smaller/fast variants before huge full models unless a workflow needs them.

### `FLUX.1-Fill-dev`

- Repo: `black-forest-labs/FLUX.1-Fill-dev`
- Location: `Diffusion-Image`
- Capability: Image generation/editing
- Library status: `verified_file_server_copy`
- Transfer priority: `medium`
- Keep status: `active`
- AI-box runtime: ComfyUI or diffusers on AI box.
- Size: `54.07 GiB`; payload files: `29`
- Recommended use: Move to AI box for ComfyUI/diffusers image generation and editing.
- Notes: Transfer smaller/fast variants before huge full models unless a workflow needs them.

### `FLUX.1-Kontext-dev`

- Repo: `black-forest-labs/FLUX.1-Kontext-dev`
- Location: `Diffusion-Image`
- Capability: Image generation/editing
- Library status: `verified_file_server_copy`
- Transfer priority: `medium`
- Keep status: `active`
- AI-box runtime: ComfyUI or diffusers on AI box.
- Size: `53.92 GiB`; payload files: `30`
- Recommended use: Move to AI box for ComfyUI/diffusers image generation and editing.
- Notes: Transfer smaller/fast variants before huge full models unless a workflow needs them.

### `FLUX.1-schnell`

- Repo: `black-forest-labs/FLUX.1-schnell`
- Location: `Diffusion-Image`
- Capability: Image generation/editing
- Library status: `verified_file_server_copy`
- Transfer priority: `high`
- Keep status: `active`
- AI-box runtime: ComfyUI or diffusers on AI box.
- Size: `53.87 GiB`; payload files: `29`
- Recommended use: Move to AI box for ComfyUI/diffusers image generation and editing.
- Notes: Transfer smaller/fast variants before huge full models unless a workflow needs them.

### `FLUX.2-dev`

- Repo: `black-forest-labs/FLUX.2-dev`
- Location: `Diffusion-Image`
- Capability: Image generation/editing
- Library status: `verified_file_server_copy`
- Transfer priority: `medium`
- Keep status: `active`
- AI-box runtime: ComfyUI or diffusers on AI box.
- Size: `165.44 GiB`; payload files: `40`
- Recommended use: Move to AI box for ComfyUI/diffusers image generation and editing.
- Notes: Transfer smaller/fast variants before huge full models unless a workflow needs them. Large active transfer; copy only when a specific AI-box test is planned.

### `FLUX.2-klein-9B`

- Repo: `black-forest-labs/FLUX.2-klein-9B`
- Location: `Diffusion-Image`
- Capability: Image generation/editing
- Library status: `verified_file_server_copy`
- Transfer priority: `high`
- Keep status: `active`
- AI-box runtime: ComfyUI or diffusers on AI box.
- Size: `49.26 GiB`; payload files: `30`
- Recommended use: Move to AI box for ComfyUI/diffusers image generation and editing.
- Notes: Transfer smaller/fast variants before huge full models unless a workflow needs them.

### `FLUX.2-klein-9b-fp8`

- Repo: `black-forest-labs/FLUX.2-klein-9b-fp8`
- Location: `Diffusion-Image`
- Capability: Image generation/editing
- Library status: `verified_file_server_copy`
- Transfer priority: `high`
- Keep status: `active`
- AI-box runtime: ComfyUI or diffusers on AI box.
- Size: `8.79 GiB`; payload files: `8`
- Recommended use: Move to AI box for ComfyUI/diffusers image generation and editing.
- Notes: Transfer smaller/fast variants before huge full models unless a workflow needs them.

### `stable-diffusion-3-medium`

- Repo: `stabilityai/stable-diffusion-3-medium`
- Location: `Diffusion-Image`
- Capability: Image generation/editing
- Library status: `verified_file_server_copy`
- Transfer priority: `medium`
- Keep status: `active`
- AI-box runtime: ComfyUI or diffusers on AI box.
- Size: `49.66 GiB`; payload files: `29`
- Recommended use: Move to AI box for ComfyUI/diffusers image generation and editing.
- Notes: Transfer smaller/fast variants before huge full models unless a workflow needs them.

### `stable-diffusion-3.5-large`

- Repo: `stabilityai/stable-diffusion-3.5-large`
- Location: `Diffusion-Image`
- Capability: Image generation/editing
- Library status: `verified_file_server_copy`
- Transfer priority: `medium`
- Keep status: `active`
- AI-box runtime: ComfyUI or diffusers on AI box.
- Size: `66.67 GiB`; payload files: `46`
- Recommended use: Move to AI box for ComfyUI/diffusers image generation and editing.
- Notes: Transfer smaller/fast variants before huge full models unless a workflow needs them.

### `all-MiniLM-L12-v2`

- Repo: `sentence-transformers/all-MiniLM-L12-v2`
- Location: `Embeddings`
- Capability: Embeddings / retrieval
- Library status: `verified_file_server_copy`
- Transfer priority: `medium`
- Keep status: `active`
- AI-box runtime: sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants.
- Size: `1.21 GiB`; payload files: `30`
- Recommended use: Move to AI box for semantic search, RAG retrieval, clustering, similarity.
- Notes: Copy small baseline first; benchmark retrieval quality before choosing the default embedding model.

### `all-MiniLM-L6-v2`

- Repo: `sentence-transformers/all-MiniLM-L6-v2`
- Location: `Embeddings`
- Capability: Embeddings / retrieval
- Library status: `verified_file_server_copy`
- Transfer priority: `high`
- Keep status: `active`
- AI-box runtime: sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants.
- Size: `0.83 GiB`; payload files: `30`
- Recommended use: Move to AI box for semantic search, RAG retrieval, clustering, similarity.
- Notes: Copy small baseline first; benchmark retrieval quality before choosing the default embedding model.

### `all-mpnet-base-v2`

- Repo: `sentence-transformers/all-mpnet-base-v2`
- Location: `Embeddings`
- Capability: Embeddings / retrieval
- Library status: `verified_file_server_copy`
- Transfer priority: `high`
- Keep status: `active`
- AI-box runtime: sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants.
- Size: `3.56 GiB`; payload files: `29`
- Recommended use: Move to AI box for semantic search, RAG retrieval, clustering, similarity.
- Notes: Copy small baseline first; benchmark retrieval quality before choosing the default embedding model.

### `embeddinggemma-300m`

- Repo: `google/embeddinggemma-300m`
- Location: `Embeddings`
- Capability: Embeddings / retrieval
- Library status: `verified_file_server_copy`
- Transfer priority: `medium`
- Keep status: `active`
- AI-box runtime: sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants.
- Size: `1.18 GiB`; payload files: `20`
- Recommended use: Move to AI box for semantic search, RAG retrieval, clustering, similarity.
- Notes: Copy small baseline first; benchmark retrieval quality before choosing the default embedding model.

### `paraphrase-multilingual-MiniLM-L12-v2`

- Repo: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- Location: `Embeddings`
- Capability: Embeddings / retrieval
- Library status: `verified_file_server_copy`
- Transfer priority: `medium`
- Keep status: `active`
- AI-box runtime: sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants.
- Size: `3.87 GiB`; payload files: `28`
- Recommended use: Move to AI box for semantic search, RAG retrieval, clustering, similarity.
- Notes: Copy small baseline first; benchmark retrieval quality before choosing the default embedding model.

### `paraphrase-multilingual-mpnet-base-v2`

- Repo: `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`
- Location: `Embeddings`
- Capability: Embeddings / retrieval
- Library status: `verified_file_server_copy`
- Transfer priority: `high`
- Keep status: `active`
- AI-box runtime: sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants.
- Size: `9.07 GiB`; payload files: `27`
- Recommended use: Move to AI box for semantic search, RAG retrieval, clustering, similarity.
- Notes: Copy small baseline first; benchmark retrieval quality before choosing the default embedding model.

### `Qwen3-Embedding-8B-Q4_K_M`

- Repo: `enacimie/Qwen3-Embedding-8B-Q4_K_M-GGUF`
- Location: `Embeddings`
- Capability: Embeddings / retrieval
- Library status: `verified_file_server_copy`
- Transfer priority: `medium`
- Keep status: `active`
- AI-box runtime: sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants.
- Size: `4.36 GiB`; payload files: `2`
- Recommended use: Move to AI box for semantic search, RAG retrieval, clustering, similarity.
- Notes: Copy small baseline first; benchmark retrieval quality before choosing the default embedding model.

### `Qwen3-VL-Embedding-8B`

- Repo: `Qwen/Qwen3-VL-Embedding-8B`
- Location: `Embeddings`
- Capability: Embeddings / retrieval
- Library status: `verified_file_server_copy`
- Transfer priority: `medium`
- Keep status: `active`
- AI-box runtime: sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants.
- Size: `15.19 GiB`; payload files: `23`
- Recommended use: Move to AI box for semantic search, RAG retrieval, clustering, similarity.
- Notes: Copy small baseline first; benchmark retrieval quality before choosing the default embedding model.

### `DeepSeek-R1-Distill-Qwen-32B-Q5_K_M`

- Repo: `roleplaiapp/DeepSeek-R1-Distill-Qwen-32B-Q5_K_M-GGUF`
- Location: `LLM`
- Capability: LLM / reasoning-chat
- Library status: `verified_file_server_copy`
- Transfer priority: `high`
- Keep status: `active`
- AI-box runtime: llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives.
- Size: `21.66 GiB`; payload files: `2`
- Recommended use: Move to AI box for chat, reasoning, drafting, and agent-backend trials.
- Notes: Benchmark tokens/sec and answer quality on the AI box before setting defaults.

### `Gemma-3-27B-QAT-Q4_0`

- Repo: `google/gemma-3-27b-it-qat-q4_0-gguf`
- Location: `LLM`
- Capability: LLM / reasoning-chat
- Library status: `verified_file_server_copy`
- Transfer priority: `medium`
- Keep status: `active`
- AI-box runtime: llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives.
- Size: `16.05 GiB`; payload files: `2`
- Recommended use: Move to AI box for chat, reasoning, drafting, and agent-backend trials.
- Notes: Benchmark tokens/sec and answer quality on the AI box before setting defaults.

### `GLM-4.7-Flash-Q4_K_M`

- Repo: `yybl/Qwen3-30B-A3B-Thinking-2507-GLM-4.7-Flash-High-Reasoning-Q4_K_M-GGUF`
- Location: `LLM`
- Capability: LLM / reasoning-chat
- Library status: `verified_file_server_copy`
- Transfer priority: `high`
- Keep status: `active`
- AI-box runtime: llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives.
- Size: `17.21 GiB`; payload files: `2`
- Recommended use: Move to AI box for chat, reasoning, drafting, and agent-backend trials.
- Notes: Benchmark tokens/sec and answer quality on the AI box before setting defaults.

### `GPT-OSS-20B`

- Repo: `openai/gpt-oss-20b`
- Location: `LLM`
- Capability: LLM / reasoning-chat
- Library status: `verified_file_server_copy`
- Transfer priority: `high`
- Keep status: `active`
- AI-box runtime: llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives.
- Size: `38.47 GiB`; payload files: `19`
- Recommended use: Move to AI box for chat, reasoning, drafting, and agent-backend trials.
- Notes: Benchmark tokens/sec and answer quality on the AI box before setting defaults.

### `Ministral-3-14B-Q5_K_M`

- Repo: `NikolayKozloff/Ministral-3-14B-Reasoning-2512-Q5_K_M-GGUF`
- Location: `LLM`
- Capability: LLM / reasoning-chat
- Library status: `verified_file_server_copy`
- Transfer priority: `high`
- Keep status: `active`
- AI-box runtime: llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives.
- Size: `8.96 GiB`; payload files: `2`
- Recommended use: Move to AI box for chat, reasoning, drafting, and agent-backend trials.
- Notes: Benchmark tokens/sec and answer quality on the AI box before setting defaults.

### `Qwen3-32B-Q5_K_M`

- Repo: `jacobcarajo/Qwen3-32B-Q5_K_M-GGUF`
- Location: `LLM`
- Capability: LLM / reasoning-chat
- Library status: `verified_file_server_copy`
- Transfer priority: `high`
- Keep status: `active`
- AI-box runtime: llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives.
- Size: `21.62 GiB`; payload files: `2`
- Recommended use: Move to AI box for chat, reasoning, drafting, and agent-backend trials.
- Notes: Benchmark tokens/sec and answer quality on the AI box before setting defaults.

### `Qwen3.6-35B-A3B-NVFP4`

- Repo: `nvidia/Qwen3.6-35B-A3B-NVFP4`
- Location: `LLM`
- Capability: LLM / reasoning-chat
- Library status: `verified_file_server_copy`
- Transfer priority: `high`
- Keep status: `active`
- AI-box runtime: llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives.
- Size: `21.85 GiB`; payload files: `18`
- Recommended use: Move to AI box for chat, reasoning, drafting, and agent-backend trials.
- Notes: Benchmark tokens/sec and answer quality on the AI box before setting defaults.

### `Qwen3.6-35B-A3B-UD-Q4_K_M`

- Repo: `juan1995-dev/Qwen3.6-35B-A3B-UD-Q4_K_M_GGUF`
- Location: `LLM`
- Capability: LLM / reasoning-chat
- Library status: `verified_file_server_copy`
- Transfer priority: `high`
- Keep status: `active`
- AI-box runtime: llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives.
- Size: `20.61 GiB`; payload files: `2`
- Recommended use: Move to AI box for chat, reasoning, drafting, and agent-backend trials.
- Notes: Benchmark tokens/sec and answer quality on the AI box before setting defaults.

### `Prompt-Guard-86M`

- Repo: `meta-llama/Prompt-Guard-86M`
- Location: `Safety-Moderation`
- Capability: Prompt safety / moderation
- Library status: `verified_file_server_copy`
- Transfer priority: `high`
- Keep status: `active`
- AI-box runtime: transformers sequence-classification on AI box.
- Size: `1.05 GiB`; payload files: `12`
- Recommended use: Move to AI box for prompt-injection and jailbreak checks in agents/RAG.
- Notes: Strong default safety guardrail candidate; small transfer.

### `nemotron-3.5-asr-streaming-0.6b`

- Repo: `nvidia/nemotron-3.5-asr-streaming-0.6b`
- Location: `Speech-STT`
- Capability: Speech-to-text
- Library status: `verified_file_server_copy`
- Transfer priority: `medium`
- Keep status: `active`
- AI-box runtime: faster-whisper preferred; transformers fallback on AI box.
- Size: `5.27 GiB`; payload files: `23`
- Recommended use: Move to AI box for transcription/STT testing.
- Notes: Transfer v3-turbo first; keep v2 only if AI-box accuracy tests justify it.

### `whisper-large-v2`

- Repo: `openai/whisper-large-v2`
- Location: `Speech-STT`
- Capability: Speech-to-text
- Library status: `verified_file_server_copy`
- Transfer priority: `medium`
- Keep status: `review_after_benchmark`
- AI-box runtime: faster-whisper preferred; transformers fallback on AI box.
- Size: `23.00 GiB`; payload files: `17`
- Recommended use: Move to AI box for transcription/STT testing.
- Notes: Transfer v3-turbo first; keep v2 only if AI-box accuracy tests justify it.

### `whisper-large-v3`

- Repo: `openai/whisper-large-v3`
- Location: `Speech-STT`
- Capability: Speech-to-text
- Library status: `verified_file_server_copy`
- Transfer priority: `medium`
- Keep status: `active`
- AI-box runtime: faster-whisper preferred; transformers fallback on AI box.
- Size: `23.01 GiB`; payload files: `22`
- Recommended use: Move to AI box for transcription/STT testing.
- Notes: Transfer v3-turbo first; keep v2 only if AI-box accuracy tests justify it.

### `whisper-large-v3-turbo`

- Repo: `openai/whisper-large-v3-turbo`
- Location: `Speech-STT`
- Capability: Speech-to-text
- Library status: `verified_file_server_copy`
- Transfer priority: `high`
- Keep status: `active`
- AI-box runtime: faster-whisper preferred; transformers fallback on AI box.
- Size: `1.51 GiB`; payload files: `14`
- Recommended use: Move to AI box for transcription/STT testing.
- Notes: Transfer v3-turbo first; keep v2 only if AI-box accuracy tests justify it.

### `stable-video-diffusion-img2vid-xt-1-1`

- Repo: `stabilityai/stable-video-diffusion-img2vid-xt-1-1`
- Location: `Video`
- Capability: Video generation
- Library status: `verified_file_server_copy`
- Transfer priority: `medium`
- Keep status: `active`
- AI-box runtime: ComfyUI or diffusers Stable Video pipeline on AI box.
- Size: `17.06 GiB`; payload files: `18`
- Recommended use: Move to AI box for image-to-video generation workflows.
- Notes: Structurally verified; transfer only when video pipeline testing is planned.

### `DeepSeek-OCR-2`

- Repo: `deepseek-ai/DeepSeek-OCR-2`
- Location: `Vision-OCR`
- Capability: OCR / document extraction
- Library status: `verified_file_server_copy`
- Transfer priority: `medium`
- Keep status: `active`
- AI-box runtime: transformers/custom model code on AI box.
- Size: `6.32 GiB`; payload files: `17`
- Recommended use: Move to AI box for image/PDF text extraction experiments.
- Notes: Needs sample-image benchmark on the AI box.
