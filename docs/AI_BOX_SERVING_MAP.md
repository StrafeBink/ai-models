# AI Box Serving Map

Purpose: choose which verified file-server model to manually copy to the AI box for each capability, and what runtime family the AI box should use.

| Capability | Copy first | Alternatives | AI-box runtime family | Status |
|---|---|---|---|---|
| Chat / reasoning | `GPT-OSS-20B` or `Qwen3-32B-Q5_K_M` | `Gemma-3-27B-QAT-Q4_0`, `GLM-4.7-Flash-Q4_K_M`, `Qwen3.6-35B-A3B-NVFP4` | llama.cpp/GGUF or compatible LLM runtime | Needs AI-box benchmark |
| Coding | `Qwen3-Coder-30B-A3B-UD-Q4_K_XL` | `Qwen3-Coder-Next-Q4_K_M` | llama.cpp/GGUF | Needs AI-box benchmark |
| Embeddings | `all-MiniLM-L6-v2` | `all-mpnet-base-v2`, `Qwen3-Embedding-8B-Q4_K_M`, `Qwen3-VL-Embedding-8B` | sentence-transformers/transformers or GGUF embedding runtime | Copy MiniLM first |
| Prompt safety | `Prompt-Guard-86M` | none currently | transformers sequence classification | High-priority small transfer |
| Speech-to-text | `whisper-large-v3-turbo` | `whisper-large-v3`, `nemotron-3.5-asr-streaming-0.6b` | faster-whisper or transformers | Copy turbo first |
| OCR | `DeepSeek-OCR-2` | none currently | transformers/custom model code | Medium priority |
| Image generation/editing | `FLUX.2-klein-9B` or `FLUX.1-schnell` | `FLUX.2-dev`, `stable-diffusion-3.5-large` | ComfyUI or diffusers | Copy smaller/fast model first |
| Video generation | `stable-video-diffusion-img2vid-xt-1-1` | none currently | ComfyUI or diffusers | Transfer only for planned video test |
| Audio generation | `stable-audio-open-1.0`, `stable-audio-3-medium`, `stable-audio-3-small-sfx` | `personaplex-7b-v1` | model-specific audio stack | Transfer only for planned audio test |

## File-server rule

Do not install heavy inference stacks into the file-server project venv just to test models. Keep this repo focused on discovery, downloads, metadata, verification, storage dashboards, and AI-box handoff guidance.