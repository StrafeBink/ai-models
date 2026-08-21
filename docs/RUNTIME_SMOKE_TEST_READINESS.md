# Runtime Smoke Test Readiness

The current repository smoke tests are structural. Full inference tests require runtime packages/tools.

## CLI/runtime availability

| Runtime | Available |
|---|---:|
| llama.cpp CLI (`llama-cli` or `main`) | ❌ |
| ollama CLI | ❌ |
| comfy CLI | ❌ |

## Proposed full runtime tests

| Capability | Test | Dependency |
|---|---|---|
| Embeddings | Embed five sentences and check cosine similarity ordering | `sentence-transformers`, `torch` |
| Prompt Guard | Classify benign, injection, and jailbreak prompts | `transformers`, `torch` |
| Whisper | Transcribe a short known audio sample | `faster-whisper` or `transformers`, `torch` |
| GGUF LLM | Generate a 20-token response and record tokens/sec | `llama.cpp` or `llama-cpp-python` |
| OCR | Extract text from a known sample image | `transformers`, `torch`, model custom code |
| Diffusion/video/audio | Generate a tiny/sample output | ComfyUI or diffusers stack |

## Recommendation

Install runtime stacks deliberately, one family at a time, so the project can record exact working commands and avoid turning the manager venv into an unstable heavy ML environment.