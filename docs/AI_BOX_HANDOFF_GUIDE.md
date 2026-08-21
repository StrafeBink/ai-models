# AI Box Handoff Guide

This repo is the model library/file server. Models are manually copied to the AI box for execution. Use this guide to avoid moving giant folders without purpose.

## Recommended handoff workflow

1. Check `docs/AI_BOX_TRANSFER_PRIORITY.md` for copy priority.
2. Check `docs/AI_BOX_SERVING_MAP.md` for the target runtime family.
3. Copy one model family at a time to the AI box.
4. Run a small AI-box benchmark and record the result back in project notes or a future benchmark report.
5. Only then promote a model to default use or mark older models as superseded.

## Suggested first transfers

| Purpose | Model | Why |
|---|---|---|
| Fast embeddings baseline | `Embeddings/all-MiniLM-L6-v2` | Small, verified, useful for RAG/search. |
| Prompt safety | `Safety-Moderation/Prompt-Guard-86M` | Small guardrail model for agent/RAG workflows. |
| Coding model | `Coding/Qwen3-Coder-30B-A3B-UD-Q4_K_XL` | Active GGUF coding candidate. |
| Chat/reasoning | `LLM/Qwen3-32B-Q5_K_M` or `LLM/GPT-OSS-20B` | Active local LLM candidates. |
| STT | `Speech-STT/whisper-large-v3-turbo` | Smallest/fastest Whisper candidate. |
| Image generation | `Diffusion-Image/FLUX.2-klein-9B` or `Diffusion-Image/FLUX.1-schnell` | Prefer smaller/faster image models before huge variants. |

## Avoid routine transfers

- `Archive-Huge/LLM/Kimi-K3`: strategic archive; huge transfer, future-hardware value.
- Full FLUX/SD large models: transfer only when ComfyUI/diffusers workflow is ready.
- Older Llama archive models: transfer only for comparison/regression tests.