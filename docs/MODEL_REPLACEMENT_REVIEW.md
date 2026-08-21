# Model Replacement / Deprecation Review

No deletion is recommended automatically. This report identifies benchmark-driven keep/archive/delete decisions for the file-server library and AI-box transfer workflow.

| Model | Suggested action | Rationale |
|---|---|---|
| `whisper-large-v2` | Copy only for comparison; likely archive | `whisper-large-v3` and `whisper-large-v3-turbo` are present; keep v2 only if AI-box accuracy tests justify it. Size: `23.00 GiB`. |
| `Llama-2-7b-chat-hf` | Archive only | Older Llama 2 chat model is strategically useful but not a default AI-box transfer candidate. Size: `25.11 GiB`. |
| `Meta-Llama-3-8B` | Archive / compare only if needed | Newer Qwen/GPT-OSS/Gemma local candidates are present. Size: `29.93 GiB`. |
| `Llama-3.1-8B-Instruct` | Archive / compare only if needed | Useful baseline but likely superseded by newer active AI-box candidates. Size: `29.93 GiB`. |
| `all-MiniLM-L12-v2` | Benchmark before copying routinely | `all-MiniLM-L6-v2` is smaller/faster; `all-mpnet-base-v2` may be higher quality. Size: `1.21 GiB`. |
| `paraphrase-multilingual-MiniLM-L12-v2` | Copy only for multilingual benchmark | May be superseded by multilingual mpnet or Qwen embedding depending AI-box quality/latency. Size: `3.87 GiB`. |
| `stable-diffusion-3-medium` | Review against SD3.5/FLUX | Newer SD3.5/FLUX families are present; copy only if AI-box workflow compatibility or speed matters. Size: `49.66 GiB`. |
| `FLUX.1-schnell` | Good fast baseline transfer | May remain useful despite FLUX.2 because it is faster/simpler. Size: `53.87 GiB`. |
| `Kimi-K3` | Strategic archive | Very large model; keep on file server for future hardware/significance, not routine transfer. Size: `1453.79 GiB`. |

## General rules

- Do not delete a model until a replacement has passed an AI-box benchmark for the actual use case.
- Prefer archiving over deleting gated or hard-to-redownload models.
- Keep one fast/small baseline per capability even when a larger higher-quality model exists.
- Review `Archive-Huge/` quarterly for storage pressure, not weekly.