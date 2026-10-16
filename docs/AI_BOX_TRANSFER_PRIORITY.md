# AI Box Transfer Priority

Use this when deciding what to manually copy from the file-server library to the AI box.

## `high`

| Model | Capability | Size | AI-box runtime | Why copy / why keep |
|---|---|---:|---|---|
| `Kokoro-82M` | Text-to-speech / voice | 0.34 GiB | Model-specific PyTorch package (kokoro, chatterbox, qwen-tts, vibevoice, voxcpm) on AI box; Kokoro also runs on CPU/ONNX. | Start with Kokoro (tiny, fast) as the default voice; use Qwen3-TTS or Chatterbox for cloning. |
| `all-MiniLM-L6-v2` | Embeddings / retrieval | 0.91 GiB | sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants. | Copy small baseline first; benchmark retrieval quality before choosing the default embedding model. |
| `Prompt-Guard-86M` | Prompt safety / moderation | 1.05 GiB | transformers sequence-classification on AI box. | Strong default safety guardrail candidate; small transfer. |
| `whisper-large-v3-turbo` | Speech-to-text | 1.51 GiB | faster-whisper preferred; transformers fallback on AI box. | Transfer v3-turbo first; keep v2 only if AI-box accuracy tests justify it. |
| `all-mpnet-base-v2` | Embeddings / retrieval | 3.56 GiB | sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants. | Copy small baseline first; benchmark retrieval quality before choosing the default embedding model. |
| `Qwen3-TTS-12Hz-1.7B-CustomVoice` | Text-to-speech / voice | 4.21 GiB | Model-specific PyTorch package (kokoro, chatterbox, qwen-tts, vibevoice, voxcpm) on AI box; Kokoro also runs on CPU/ONNX. | Start with Kokoro (tiny, fast) as the default voice; use Qwen3-TTS or Chatterbox for cloning. |
| `Qwen3-TTS-12Hz-1.7B-Base` | Text-to-speech / voice | 4.23 GiB | Model-specific PyTorch package (kokoro, chatterbox, qwen-tts, vibevoice, voxcpm) on AI box; Kokoro also runs on CPU/ONNX. | Start with Kokoro (tiny, fast) as the default voice; use Qwen3-TTS or Chatterbox for cloning. |
| `parakeet-tdt-0.6b-v3` | Speech-to-text | 5.34 GiB | NeMo (parakeet/nemotron) or transformers (Qwen3-ASR) on AI box. | Benchmark against whisper-large-v3-turbo for speed and accuracy. |
| `FLUX.2-klein-9b-fp8` | Image generation/editing | 8.79 GiB | ComfyUI or diffusers on AI box. | Transfer smaller/fast variants before huge full models unless a workflow needs them. |
| `Ministral-3-14B-Q5_K_M` | LLM / reasoning-chat | 8.96 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | Benchmark tokens/sec and answer quality on the AI box before setting defaults. |
| `paraphrase-multilingual-mpnet-base-v2` | Embeddings / retrieval | 9.07 GiB | sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants. | Copy small baseline first; benchmark retrieval quality before choosing the default embedding model. |
| `Qwen2.5-Coder-14B-Instruct-AWQ` | Coding LLM | 9.31 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archive. | GGUF quants are likely the most useful current AI-box transfer candidates. |
| `chatterbox` | Text-to-speech / voice | 12.91 GiB | Model-specific PyTorch package (kokoro, chatterbox, qwen-tts, vibevoice, voxcpm) on AI box; Kokoro also runs on CPU/ONNX. | Start with Kokoro (tiny, fast) as the default voice; use Qwen3-TTS or Chatterbox for cloning. |
| `Qwen3-Coder-30B-A3B-UD-Q4_K_XL` | Coding LLM | 16.45 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archive. | GGUF quants are likely the most useful current AI-box transfer candidates. |
| `GLM-4.7-Flash-Q4_K_M` | LLM / reasoning-chat | 17.21 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | Benchmark tokens/sec and answer quality on the AI box before setting defaults. |
| `Qwen2.5-Coder-32B-Instruct-AWQ` | Coding LLM | 18.01 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archive. | GGUF quants are likely the most useful current AI-box transfer candidates. |
| `Qwen3.6-35B-A3B-UD-Q4_K_M` | LLM / reasoning-chat | 20.61 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | Benchmark tokens/sec and answer quality on the AI box before setting defaults. |
| `Qwen3-32B-Q5_K_M` | LLM / reasoning-chat | 21.62 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | Benchmark tokens/sec and answer quality on the AI box before setting defaults. |
| `DeepSeek-R1-Distill-Qwen-32B-Q5_K_M` | LLM / reasoning-chat | 21.66 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | Benchmark tokens/sec and answer quality on the AI box before setting defaults. |
| `Qwen3.6-35B-A3B-NVFP4` | LLM / reasoning-chat | 21.85 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | Benchmark tokens/sec and answer quality on the AI box before setting defaults. |
| `GPT-OSS-20B` | LLM / reasoning-chat | 38.47 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | Benchmark tokens/sec and answer quality on the AI box before setting defaults. |
| `Qwen3-Coder-Next-Q4_K_M` | Coding LLM | 45.09 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archive. | GGUF quants are likely the most useful current AI-box transfer candidates. |
| `FLUX.2-klein-9B` | Image generation/editing | 49.26 GiB | ComfyUI or diffusers on AI box. | Transfer smaller/fast variants before huge full models unless a workflow needs them. |
| `FLUX.1-schnell` | Image generation/editing | 53.87 GiB | ComfyUI or diffusers on AI box. | Transfer smaller/fast variants before huge full models unless a workflow needs them. |

## `medium`

| Model | Capability | Size | AI-box runtime | Why copy / why keep |
|---|---|---:|---|---|
| `silero-vad` | Speaker diarisation / voice activity | 0.01 GiB | NeMo / ONNX runtime on AI box (very small; CPU is fine). | Small helper models for transcription pipelines. |
| `Nemotron-3-Diarization` | Speaker diarisation / voice activity | 0.66 GiB | NeMo / ONNX runtime on AI box (very small; CPU is fine). | Small helper models for transcription pipelines. |
| `embeddinggemma-300m` | Embeddings / retrieval | 1.18 GiB | sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants. | Copy small baseline first; benchmark retrieval quality before choosing the default embedding model. |
| `all-MiniLM-L12-v2` | Embeddings / retrieval | 1.21 GiB | sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants. | Copy small baseline first; benchmark retrieval quality before choosing the default embedding model. |
| `Qwen3-0.6B` | LLM / reasoning-chat | 1.41 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | Benchmark tokens/sec and answer quality on the AI box before setting defaults. |
| `embeddinggemma-2` | Embeddings / retrieval | 1.42 GiB | sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants. | Copy small baseline first; benchmark retrieval quality before choosing the default embedding model. |
| `stable-audio-3-small-sfx` | Audio generation / audio model | 3.25 GiB | Model-specific audio/diffusers stack on AI box. | Needs model-specific AI-box generation smoke test. |
| `paraphrase-multilingual-MiniLM-L12-v2` | Embeddings / retrieval | 3.87 GiB | sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants. | Copy small baseline first; benchmark retrieval quality before choosing the default embedding model. |
| `Qwen3-VL-Reranker-2B` | Reranking / retrieval | 3.98 GiB | transformers/sentence-transformers cross-encoder on AI box. | Pair with an embedding model; benchmark retrieval quality with and without reranking. |
| `Qwen3-Embedding-8B-Q4_K_M` | Embeddings / retrieval | 4.36 GiB | sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants. | Copy small baseline first; benchmark retrieval quality before choosing the default embedding model. |
| `Qwen3-ASR-1.7B` | Speech-to-text | 4.38 GiB | NeMo (parakeet/nemotron) or transformers (Qwen3-ASR) on AI box. | Benchmark against whisper-large-v3-turbo for speed and accuracy. |
| `VoxCPM2` | Text-to-speech / voice | 4.62 GiB | Model-specific PyTorch package (kokoro, chatterbox, qwen-tts, vibevoice, voxcpm) on AI box; Kokoro also runs on CPU/ONNX. | Start with Kokoro (tiny, fast) as the default voice; use Qwen3-TTS or Chatterbox for cloning. |
| `VibeVoice-1.5B` | Text-to-speech / voice | 5.04 GiB | Model-specific PyTorch package (kokoro, chatterbox, qwen-tts, vibevoice, voxcpm) on AI box; Kokoro also runs on CPU/ONNX. | Start with Kokoro (tiny, fast) as the default voice; use Qwen3-TTS or Chatterbox for cloning. |
| `nemotron-3.5-asr-streaming-0.6b` | Speech-to-text | 5.27 GiB | NeMo (parakeet/nemotron) or transformers (Qwen3-ASR) on AI box. | Benchmark against whisper-large-v3-turbo for speed and accuracy. |
| `DeepSeek-OCR-2` | OCR / document extraction | 6.32 GiB | transformers/custom model code on AI box. | Needs sample-image benchmark on the AI box. |
| `stable-audio-3-medium` | Audio generation / audio model | 9.73 GiB | Model-specific audio/diffusers stack on AI box. | Needs model-specific AI-box generation smoke test. |
| `stable-audio-open-1.0` | Audio generation / audio model | 14.60 GiB | Model-specific audio/diffusers stack on AI box. | Needs model-specific AI-box generation smoke test. |
| `Qwen3-VL-Embedding-8B` | Embeddings / retrieval | 15.19 GiB | sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants. | Copy small baseline first; benchmark retrieval quality before choosing the default embedding model. |
| `Qwen3-8B` | LLM / reasoning-chat | 15.27 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | Benchmark tokens/sec and answer quality on the AI box before setting defaults. |
| `personaplex-7b-v1` | Audio generation / audio model | 15.96 GiB | Model-specific audio/diffusers stack on AI box. | Needs model-specific AI-box generation smoke test. |
| `Gemma-3-27B-QAT-Q4_0` | LLM / reasoning-chat | 16.05 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | Benchmark tokens/sec and answer quality on the AI box before setting defaults. |
| `gemma-4-26B-A4B-it-UD-Q4_K_XL` | LLM / reasoning-chat | 16.95 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | Benchmark tokens/sec and answer quality on the AI box before setting defaults. |
| `stable-video-diffusion-img2vid-xt-1-1` | Video generation | 17.06 GiB | ComfyUI or diffusers Stable Video pipeline on AI box. | Structurally verified; transfer only when video pipeline testing is planned. |
| `Qwen3.8-27B-UD-Q4_K_XL` | LLM / reasoning-chat | 17.22 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | Benchmark tokens/sec and answer quality on the AI box before setting defaults. |
| `whisper-large-v2` | Speech-to-text | 23.00 GiB | faster-whisper preferred; transformers fallback on AI box. | Transfer v3-turbo first; keep v2 only if AI-box accuracy tests justify it. |
| `whisper-large-v3` | Speech-to-text | 23.01 GiB | faster-whisper preferred; transformers fallback on AI box. | Transfer v3-turbo first; keep v2 only if AI-box accuracy tests justify it. |
| `Qwen3.6-27B-FP8` | Multimodal / vision-language | 28.77 GiB | transformers/vLLM/custom multimodal runtime on AI box. | Requires AI-box multimodal runtime compatibility test. |
| `Qwen-Image-2.1` | Image generation/editing | 30.86 GiB | ComfyUI or diffusers on AI box. | Large DiT model; needs CPU offload on small-VRAM GPUs. |
| `stable-diffusion-3-medium` | Image generation/editing | 49.66 GiB | ComfyUI or diffusers on AI box. | Transfer smaller/fast variants before huge full models unless a workflow needs them. |
| `FLUX.1-Kontext-dev` | Image generation/editing | 53.92 GiB | ComfyUI or diffusers on AI box. | Transfer smaller/fast variants before huge full models unless a workflow needs them. |
| `FLUX.1-Fill-dev` | Image generation/editing | 54.07 GiB | ComfyUI or diffusers on AI box. | Transfer smaller/fast variants before huge full models unless a workflow needs them. |
| `FLUX.1-dev` | Image generation/editing | 60.59 GiB | ComfyUI or diffusers on AI box. | Transfer smaller/fast variants before huge full models unless a workflow needs them. |
| `stable-diffusion-3.5-large` | Image generation/editing | 66.67 GiB | ComfyUI or diffusers on AI box. | Transfer smaller/fast variants before huge full models unless a workflow needs them. |
| `FLUX.2-dev` | Image generation/editing | 165.44 GiB | ComfyUI or diffusers on AI box. | Transfer smaller/fast variants before huge full models unless a workflow needs them. Large active transfer; copy only when a specific AI-box test is planned. |

## `review`

| Model | Capability | Size | AI-box runtime | Why copy / why keep |
|---|---|---:|---|---|

## `archive_only`

| Model | Capability | Size | AI-box runtime | Why copy / why keep |
|---|---|---:|---|---|
| `Llama-3.2-1B-Instruct` | LLM / reasoning-chat | 4.61 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. Benchmark tokens/sec and answer quality on the AI box before setting defaults. |
| `Qwen2.5-VL-3B-Instruct` | Multimodal / vision-language | 7.00 GiB | transformers/vLLM/custom multimodal runtime on AI box. | Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. Requires AI-box multimodal runtime compatibility test. |
| `Qwen2.5-VL-7B-Instruct` | Multimodal / vision-language | 15.46 GiB | transformers/vLLM/custom multimodal runtime on AI box. | Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. Requires AI-box multimodal runtime compatibility test. |
| `Llama-2-7b-chat-hf` | LLM / reasoning-chat | 25.11 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. Benchmark tokens/sec and answer quality on the AI box before setting defaults. |
| `Qwen3-Coder-30B-A3B-Instruct-FP8` | Coding LLM | 29.05 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archive. | Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. GGUF quants are likely the most useful current AI-box transfer candidates. |
| `Llama-3.1-8B-Instruct` | LLM / reasoning-chat | 29.93 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. Benchmark tokens/sec and answer quality on the AI box before setting defaults. |
| `Meta-Llama-3-8B` | LLM / reasoning-chat | 29.93 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. Benchmark tokens/sec and answer quality on the AI box before setting defaults. |
| `Qwen3.6-35B-A3B-FP8` | Multimodal / vision-language | 33.45 GiB | transformers/vLLM/custom multimodal runtime on AI box. | Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. Requires AI-box multimodal runtime compatibility test. |
| `Qwen3-Coder-30B-A3B-Instruct` | Coding LLM | 57.17 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archive. | Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. GGUF quants are likely the most useful current AI-box transfer candidates. |
| `Qwen-AgentWorld-35B-A3B` | Multimodal / vision-language | 64.58 GiB | transformers/vLLM/custom multimodal runtime on AI box. | Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. Requires AI-box multimodal runtime compatibility test. |
| `gpt-oss-120b` | LLM / reasoning-chat | 182.55 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. Benchmark tokens/sec and answer quality on the AI box before setting defaults. |
| `DeepSeek-R1` | LLM / reasoning-chat | 641.31 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. Benchmark tokens/sec and answer quality on the AI box before setting defaults. |
| `Kimi-K3` | LLM / reasoning-chat | 1453.79 GiB | llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives. | Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. Benchmark tokens/sec and answer quality on the AI box before setting defaults. |
