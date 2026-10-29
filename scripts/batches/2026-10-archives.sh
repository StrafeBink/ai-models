#!/usr/bin/env bash
# Archive batch approved 2026-10-29. Resumable: completed files are skipped.
# A failed model does not stop the batch, but SIGTERM/SIGINT stops everything
# (so pausing for a server shutdown does not roll on to the next model).
set -uo pipefail
cd "/Users/davideddy/AI Models"
source .venv/bin/activate

trap 'echo "Stopped by signal $(date -u +%Y-%m-%dT%H:%M:%SZ)"; kill 0; exit 130' TERM INT

FAILED=()
run() {
  echo "===== $1 ($(date -u +%Y-%m-%dT%H:%M:%SZ)) ====="
  python scripts/download_archive_per_file.py "$1" --category "$2" || FAILED+=("$1")
}

echo "Started $(date -u +%Y-%m-%dT%H:%M:%SZ)"
run deepseek-ai/DeepSeek-V4-Flash-0731 LLM
run zai-org/GLM-5.3-Flash Multimodal
run deepseek-ai/DeepSeek-V4.1-Flash Multimodal
echo "Finished $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Failures: ${#FAILED[@]} ${FAILED[*]:-}"
