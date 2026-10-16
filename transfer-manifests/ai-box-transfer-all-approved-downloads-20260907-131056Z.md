# AI Box Transfer Manifest: all-approved-downloads

Generated: 20260907-131056Z
Destination root placeholder: `/mnt/ai-box/models`
Models: `5`
Total estimated transfer size: `885.92 GiB`

## Transfer checklist

- [ ] Confirm available free space on the AI box.
- [ ] Copy one model at a time or one bundle at a time.
- [ ] Preserve directory structure under the AI-box model root.
- [ ] Verify `_hermes_model_metadata.json` exists after copy.
- [ ] Verify approximate size and payload file count after copy.
- [ ] Run the AI-box runtime benchmark/smoke test.
- [ ] Record result back into this repo.

## Models

| Model | Repo | Size | Payload files | AI-box runtime hint | Source | Suggested destination |
|---|---|---:|---:|---|---|---|
| `LLM/Qwen3-8B` | `Qwen/Qwen3-8B` | 15.27 GiB | 16 | transformers/vLLM-compatible runtime on AI box | `/Users/davideddy/mnt/models/LLM/Qwen3-8B` | `/mnt/ai-box/models/LLM/Qwen3-8B` |
| `Coding/Qwen2.5-Coder-32B-Instruct-AWQ` | `Qwen/Qwen2.5-Coder-32B-Instruct-AWQ` | 18.01 GiB | 16 | llama.cpp/GGUF/AWQ-compatible runtime on AI box | `/Users/davideddy/mnt/models/Coding/Qwen2.5-Coder-32B-Instruct-AWQ` | `/mnt/ai-box/models/Coding/Qwen2.5-Coder-32B-Instruct-AWQ` |
| `Multimodal/Qwen3.6-27B-FP8` | `Qwen/Qwen3.6-27B-FP8` | 28.77 GiB | 81 | transformers/vLLM-compatible runtime on AI box | `/Users/davideddy/mnt/models/Multimodal/Qwen3.6-27B-FP8` | `/mnt/ai-box/models/Multimodal/Qwen3.6-27B-FP8` |
| `Archive-Huge/LLM/gpt-oss-120b` | `openai/gpt-oss-120b` | 182.55 GiB | 38 | transformers/vLLM-compatible runtime on AI box | `/Users/davideddy/mnt/models/Archive-Huge/LLM/gpt-oss-120b` | `/mnt/ai-box/models/LLM/gpt-oss-120b` |
| `Archive-Huge/LLM/DeepSeek-R1` | `deepseek-ai/DeepSeek-R1` | 641.31 GiB | 175 | transformers/vLLM-compatible runtime on AI box | `/Users/davideddy/mnt/models/Archive-Huge/LLM/DeepSeek-R1` | `/mnt/ai-box/models/LLM/DeepSeek-R1` |

## Per-model verification notes

### `LLM/Qwen3-8B`

- Source: `/Users/davideddy/mnt/models/LLM/Qwen3-8B`
- Repo: `Qwen/Qwen3-8B`
- Expected size: `15.27 GiB`
- Expected payload files excluding `.cache`: `16`
- Metadata: `_hermes_model_metadata.json` should exist in the destination folder.
- Runtime hint: transformers/vLLM-compatible runtime on AI box
- Verification: Compare source and AI-box copy: size ≈ 15.27 GiB, payload files = 16, metadata file present

### `Coding/Qwen2.5-Coder-32B-Instruct-AWQ`

- Source: `/Users/davideddy/mnt/models/Coding/Qwen2.5-Coder-32B-Instruct-AWQ`
- Repo: `Qwen/Qwen2.5-Coder-32B-Instruct-AWQ`
- Expected size: `18.01 GiB`
- Expected payload files excluding `.cache`: `16`
- Metadata: `_hermes_model_metadata.json` should exist in the destination folder.
- Runtime hint: llama.cpp/GGUF/AWQ-compatible runtime on AI box
- Verification: Compare source and AI-box copy: size ≈ 18.01 GiB, payload files = 16, metadata file present

### `Multimodal/Qwen3.6-27B-FP8`

- Source: `/Users/davideddy/mnt/models/Multimodal/Qwen3.6-27B-FP8`
- Repo: `Qwen/Qwen3.6-27B-FP8`
- Expected size: `28.77 GiB`
- Expected payload files excluding `.cache`: `81`
- Metadata: `_hermes_model_metadata.json` should exist in the destination folder.
- Runtime hint: transformers/vLLM-compatible runtime on AI box
- Verification: Compare source and AI-box copy: size ≈ 28.77 GiB, payload files = 81, metadata file present

### `Archive-Huge/LLM/gpt-oss-120b`

- Source: `/Users/davideddy/mnt/models/Archive-Huge/LLM/gpt-oss-120b`
- Repo: `openai/gpt-oss-120b`
- Expected size: `182.55 GiB`
- Expected payload files excluding `.cache`: `38`
- Metadata: `_hermes_model_metadata.json` should exist in the destination folder.
- Runtime hint: transformers/vLLM-compatible runtime on AI box
- Verification: Compare source and AI-box copy: size ≈ 182.55 GiB, payload files = 38, metadata file present

### `Archive-Huge/LLM/DeepSeek-R1`

- Source: `/Users/davideddy/mnt/models/Archive-Huge/LLM/DeepSeek-R1`
- Repo: `deepseek-ai/DeepSeek-R1`
- Expected size: `641.31 GiB`
- Expected payload files excluding `.cache`: `175`
- Metadata: `_hermes_model_metadata.json` should exist in the destination folder.
- Runtime hint: transformers/vLLM-compatible runtime on AI box
- Verification: Compare source and AI-box copy: size ≈ 641.31 GiB, payload files = 175, metadata file present
