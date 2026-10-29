#!/usr/bin/env bash
# Archive + AI-box batch approved 2026-10-29 (supersedes 2026-10-archives.sh).
# Swaps DeepSeek-V4.1-Flash (Sept) for the 1017 release and adds new picks.
# Resumable: completed files are skipped. A failed model does not stop the batch;
# SIGTERM/SIGINT stops everything.
set -uo pipefail
cd "/Users/davideddy/AI Models"
source .venv/bin/activate

trap 'echo "Stopped by signal $(date -u +%Y-%m-%dT%H:%M:%SZ)"; kill 0; exit 130' TERM INT

FAILED=()
small() {  # staged single-snapshot download for AI-box sized models
  echo "===== $1 ($(date -u +%Y-%m-%dT%H:%M:%SZ)) ====="
  python scripts/hf_model_manager.py download "$1" --category "$2" --execute --resume \
    --staging-dir download-staging --staging-copy-method rsync-inplace --max-workers 2 || FAILED+=("$1")
}
archive() {  # per-file staged download into Archive-Huge/<family>
  echo "===== $1 ($(date -u +%Y-%m-%dT%H:%M:%SZ)) ====="
  python scripts/download_archive_per_file.py "$1" --category "$2" || FAILED+=("$1")
}

echo "Started $(date -u +%Y-%m-%dT%H:%M:%SZ)"
# Quick AI-box picks first
small baidu/Unlimited-OCR-2 Vision-OCR
small Cloudflare/clef-flash Multimodal
small Qwen/Qwen-Image-2.1-Turbo Diffusion-Image
# Archives, smallest first
archive deepseek-ai/DeepSeek-V4-Flash-0731 LLM
archive nvidia/Qwen3.8-Flash-Next-FP4-Local Multimodal
archive MiniMaxAI/MiniMax-M3.1-Flash Multimodal
archive zai-org/GLM-5.3-Flash Multimodal
archive deepseek-ai/DeepSeek-V4.1-Flash-1017 Multimodal
echo "Finished $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Failures: ${#FAILED[@]} ${FAILED[*]:-}"
