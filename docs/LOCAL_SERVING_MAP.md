# Local Serving Map

Purpose: choose the best local model and runtime path for each capability. This map is operational guidance, not a benchmark result.

| Capability | First candidate | Alternative(s) | Preferred runtime | Status |
|---|---|---|---|---|
| Chat / reasoning | `GPT-OSS-20B` or `Qwen3-32B-Q5_K_M` | `Gemma-3-27B-QAT-Q4_0`, `GLM-4.7-Flash-Q4_K_M` | llama.cpp for GGUF; transformers/vLLM where supported | Needs runtime benchmark |
| Coding | `Qwen3-Coder-30B-A3B-UD-Q4_K_XL` | `Qwen3-Coder-Next-Q4_K_M` | llama.cpp / GGUF | Needs runtime benchmark |
| Embeddings | `all-MiniLM-L6-v2` for fast baseline | `all-mpnet-base-v2`, `Qwen3-Embedding-8B-Q4_K_M`, `Qwen3-VL-Embedding-8B` | sentence-transformers/transformers; GGUF embedding runtime | Needs retrieval benchmark |
| Prompt safety | `Prompt-Guard-86M` | none currently | transformers sequence classification | Ready after runtime install |
| Speech-to-text | `whisper-large-v3-turbo` | `whisper-large-v3`, `nemotron-3.5-asr-streaming-0.6b` | faster-whisper preferred; transformers fallback | Needs audio sample benchmark |
| OCR | `DeepSeek-OCR-2` | none currently | transformers/custom model code | Needs sample image benchmark |
| Image generation/editing | `FLUX.2-dev`, `FLUX.2-klein-9B`, `stable-diffusion-3.5-large` | FLUX.1 family | ComfyUI or diffusers | Needs pipeline benchmark |
| Video generation | `stable-video-diffusion-img2vid-xt-1-1` | none currently | ComfyUI or diffusers | Structurally verified |
| Audio generation | `stable-audio-open-1.0`, `stable-audio-3-medium`, `stable-audio-3-small-sfx` | `personaplex-7b-v1` | model-specific audio/diffusers stack | Needs generation benchmark |

## Runtime installation gaps observed

At the time this map was created, the project venv did not include heavy runtime packages such as `transformers`, `torch`, `sentence_transformers`, `llama_cpp`, `whisper`, or `faster_whisper`. Existing smoke tests therefore validate structure, not full inference.

## Recommended next runtime setup order

1. Install/validate `llama.cpp` or `llama-cpp-python` for GGUF LLM/coding tests.
2. Install `sentence-transformers`/`transformers`/`torch` for embeddings and Prompt Guard.
3. Install `faster-whisper` for STT testing.
4. Add ComfyUI or diffusers runtime validation for image/video/audio models.