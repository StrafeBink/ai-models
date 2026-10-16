#!/usr/bin/env bash
# Voice pack + AI-box gap models approved 2026-10-16.
# Sequential, staged locally, SMB-safe copy. One failure does not stop the batch.
set -uo pipefail
cd "/Users/davideddy/AI Models"
source .venv/bin/activate

COMMON=(--execute --resume --staging-dir download-staging --staging-copy-method rsync-inplace --max-workers 2)
FAILED=()

dl() {
  echo
  echo "===== $1 ($(date -u +%H:%M:%SZ)) ====="
  if ! python scripts/hf_model_manager.py download "$@" "${COMMON[@]}"; then
    FAILED+=("$1")
    echo "FAILED: $1"
  fi
}

# Text-to-speech
dl hexgrad/Kokoro-82M --category Speech-TTS
dl Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice --category Speech-TTS
dl Qwen/Qwen3-TTS-12Hz-1.7B-Base --category Speech-TTS
dl ResembleAI/chatterbox --category Speech-TTS
dl microsoft/VibeVoice-1.5B --category Speech-TTS
dl openbmb/VoxCPM2 --category Speech-TTS

# Speech-to-text, diarisation, voice activity detection
dl nvidia/parakeet-tdt-0.6b-v3 --category Speech-STT
dl Qwen/Qwen3-ASR-1.7B --category Speech-STT
dl nvidia/Nemotron-3-Diarization --category Speech-STT
dl onnx-community/silero-vad --category Speech-STT

# AI-box gaps
dl Qwen/Qwen3-VL-Reranker-2B --category Rerankers
dl google/embeddinggemma-2 --category Embeddings
dl unsloth/Qwen3.8-27B-GGUF --category LLM --folder-name Qwen3.8-27B-UD-Q4_K_XL \
  --allow-pattern 'Qwen3.8-27B-UD-Q4_K_XL.gguf' --allow-pattern 'mmproj-F16.gguf' --allow-pattern '*.md' --allow-pattern '*.json'
dl unsloth/gemma-4-26B-A4B-it-GGUF --category LLM --folder-name gemma-4-26B-A4B-it-UD-Q4_K_XL \
  --allow-pattern 'gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf' --allow-pattern 'mmproj-F16.gguf' --allow-pattern '*.md' --allow-pattern '*.json'
dl Qwen/Qwen-Image-2.1 --category Diffusion-Image

echo
echo "===== Batch finished $(date -u +%Y-%m-%dT%H:%M:%SZ) ====="
echo "Failures: ${#FAILED[@]} ${FAILED[*]:-}"
