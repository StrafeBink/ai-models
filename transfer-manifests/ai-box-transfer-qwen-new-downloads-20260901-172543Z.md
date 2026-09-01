# AI Box Transfer Manifest: qwen-new-downloads

Generated: 20260901-172543Z
Destination root placeholder: `/mnt/ai-box/models`
Models: `2`
Total estimated transfer size: `10.72 GiB`

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
| `LLM/Qwen3-0.6B` | `Qwen/Qwen3-0.6B` | 1.41 GiB | 11 | transformers/vLLM-compatible runtime on AI box | `/Users/davideddy/mnt/models/LLM/Qwen3-0.6B` | `/mnt/ai-box/models/LLM/Qwen3-0.6B` |
| `Coding/Qwen2.5-Coder-14B-Instruct-AWQ` | `Qwen/Qwen2.5-Coder-14B-Instruct-AWQ` | 9.31 GiB | 14 | llama.cpp/GGUF/AWQ-compatible runtime on AI box | `/Users/davideddy/mnt/models/Coding/Qwen2.5-Coder-14B-Instruct-AWQ` | `/mnt/ai-box/models/Coding/Qwen2.5-Coder-14B-Instruct-AWQ` |

## Per-model verification notes

### `LLM/Qwen3-0.6B`

- Source: `/Users/davideddy/mnt/models/LLM/Qwen3-0.6B`
- Repo: `Qwen/Qwen3-0.6B`
- Expected size: `1.41 GiB`
- Expected payload files excluding `.cache`: `11`
- Metadata: `_hermes_model_metadata.json` should exist in the destination folder.
- Runtime hint: transformers/vLLM-compatible runtime on AI box
- Verification: Compare source and AI-box copy: size ≈ 1.41 GiB, payload files = 11, metadata file present

### `Coding/Qwen2.5-Coder-14B-Instruct-AWQ`

- Source: `/Users/davideddy/mnt/models/Coding/Qwen2.5-Coder-14B-Instruct-AWQ`
- Repo: `Qwen/Qwen2.5-Coder-14B-Instruct-AWQ`
- Expected size: `9.31 GiB`
- Expected payload files excluding `.cache`: `14`
- Metadata: `_hermes_model_metadata.json` should exist in the destination folder.
- Runtime hint: llama.cpp/GGUF/AWQ-compatible runtime on AI box
- Verification: Compare source and AI-box copy: size ≈ 9.31 GiB, payload files = 14, metadata file present
