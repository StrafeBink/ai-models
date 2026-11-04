#!/usr/bin/env bash
# Queue v7 (2026-11-04): v6 + NVIDIA-only pack (after Nemotron) and NVIDIA-only frontier archives (at the end).
# v6 (2026-11-04): v5 + Nemotron 3.5 Super VL (UD-Q4_K_XL GGUF and BF16 archive) after Step-5.
# v5 (2026-11-03): v4 with Step-5-Preview moved ahead of MiMo (David's request).
# v4 notes: (2026-11-02), supersedes v3. Adds the uncensored shortlist and archive-scale
# uncensored models, and a free-space guard (keeps >= RESERVE_GIB free on the share).
# Resumable: completed models/files are skipped. A failed model does not stop the batch;
# SIGTERM/SIGINT stops everything.
set -uo pipefail
cd "/Users/davideddy/AI Models"
source .venv/bin/activate

trap 'echo "Stopped by signal $(date -u +%Y-%m-%dT%H:%M:%SZ)"; kill 0; exit 130' TERM INT

SHARE=/Users/davideddy/mnt/models
RESERVE_GIB=500
FAILED=(); SKIPPED=()
COMMON=(--execute --resume --staging-dir download-staging --staging-copy-method rsync-inplace --max-workers 2)

fits() {  # fits <needed_gib> <label>: true if the share keeps RESERVE_GIB free afterwards
  local free; free=$(df -g "$SHARE" | awk 'NR==2{print $4}')
  if [ "$free" -ge $(( $1 + RESERVE_GIB )) ]; then return 0; fi
  echo "SKIPPED (space): $2 needs ${1} GiB, share has ${free} GiB free (reserve ${RESERVE_GIB})"
  SKIPPED+=("$2"); return 1
}
small() {  # small <repo> <size_gib> <args...>
  local repo=$1 size=$2; shift 2
  echo "===== $repo ($(date -u +%Y-%m-%dT%H:%M:%SZ)) ====="
  fits "$size" "$repo" || return 0
  python scripts/hf_model_manager.py download "$repo" "$@" "${COMMON[@]}" || FAILED+=("$repo")
}
archive() {  # archive <repo> <size_gib> <category> [--target path]
  local repo=$1 size=$2 cat=$3; shift 3
  echo "===== $repo ($(date -u +%Y-%m-%dT%H:%M:%SZ)) ====="
  # Partially downloaded archives only need the remainder; skip the guard when the target exists.
  local name=${repo#*/} existing
  existing=$(ls -d "$SHARE/Archive-Huge/$cat/$name" "$SHARE/$cat/$name" 2>/dev/null | head -1)
  [ -n "$existing" ] || fits "$size" "$repo" || return 0
  python scripts/download_archive_per_file.py "$repo" --category "$cat" "$@" || FAILED+=("$repo")
}

echo "Started $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# --- Already complete (skipped quickly via metadata); kept so this script is the full record
small baidu/Unlimited-OCR-2 7 --category Vision-OCR
small Cloudflare/clef-flash 18 --category Multimodal
small Qwen/Qwen-Image-2.1-Turbo 31 --category Diffusion-Image

# --- Uncensored shortlist (2026-11-02), single quants sized for the AI box
small HauhauCS/Qwen3.8-27B-Uncensored-HauhauCS-Aggressive-MTP-GGUF 19 --category Uncensored/LLM \
  --folder-name Qwen3.8-27B-Uncensored-HauhauCS-Aggressive-Q4_K_P \
  --allow-pattern '*-Aggressive-Q4_K_P.gguf' --allow-pattern '*FastMTP*' --allow-pattern 'mmproj-*' --allow-pattern '*.md' --allow-pattern '*.json'
small DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NEO-CODER-MAX-MTP-GGUF 19 --category Uncensored/Coding \
  --folder-name Qwen3.8-27B-Heretic-Uncensored-NEO-CODER-MTP-Q4_K_M \
  --allow-pattern '*-NEO-CODER-MAX-MTP-Q4_K_M.gguf' --allow-pattern 'mmproj-F16.gguf' --allow-pattern '*.md'
small DavidAU/GLM-4.7-Flash-Uncensored-Heretic-NEO-CODE-Imatrix-MAX-GGUF 18 --category Uncensored/Coding \
  --folder-name GLM-4.7-Flash-Uncensored-Heretic-NEO-CODE-Q4_K_M \
  --allow-pattern '*-D_AU-Q4_K_M.gguf' --allow-pattern '*.md'
small LuffyTheFox/Qwen3.6-35B-A3B-Uncensored-Genesis-Hermes-GGUF 20 --category Uncensored/LLM \
  --folder-name Hermes3.6-35B-A3B-Uncensored-Genesis-APEX-Mini \
  --allow-pattern '*-APEX-Mini.gguf' --allow-pattern 'mmproj-*' --allow-pattern '*.md'
small HauhauCS/Gemma4-12B-QAT-Uncensored-HauhauCS-Balanced 8 --category Uncensored/LLM
small HauhauCS/Gemma-4-E2B-Uncensored-HauhauCS-Aggressive 5 --category Uncensored/LLM \
  --folder-name Gemma-4-E2B-Uncensored-HauhauCS-Aggressive-Q4_K_P \
  --allow-pattern '*-Q4_K_P.gguf' --allow-pattern 'mmproj-*' --allow-pattern '*.md' --allow-pattern '*.json'
small DavidAU/Llama-3.2-8X3B-MOE-Dark-Champion-Instruct-uncensored-abliterated-18.4B-GGUF 11 --category Uncensored/LLM \
  --folder-name Llama-3.2-8X3B-MOE-Dark-Champion-uncensored-Q4_k_m \
  --allow-pattern '*-Q4_k_m.gguf' --allow-pattern '*.md'
small ponpoke/flux2-klein-9b-uncensored-text-encoder 9 --category Uncensored/Diffusion-Image --confirm-gated-access \
  --folder-name flux2-klein-9b-uncensored-text-encoder-q8_0 \
  --allow-pattern 'flux2-klein-9b-uncensored-q8_0.gguf' --allow-pattern '*.md' --allow-pattern 'LICENSE*'
small pottokao/Qwen-Image-2.1-Text-Encoder-Heretic-GGUF 9 --category Uncensored/Diffusion-Image \
  --folder-name Qwen-Image-2.1-Text-Encoder-Heretic-fp8 \
  --allow-pattern 'qwen3vl_8b_fp8_heretic.safetensors' --allow-pattern 'mmproj-*' --allow-pattern '*.md'
small AtomicChat/Qwen-Image-2.1-Turbo-Uncensored-GGUF 10 --category Uncensored/Diffusion-Image \
  --folder-name Qwen-Image-2.1-Turbo-Uncensored-Q8_0 \
  --allow-pattern 'Qwen-Image-2.1-Turbo-Uncensored-Q8_0.gguf' --allow-pattern 'mmproj-Qwen-Image-2.1-Turbo-Uncensored-F16.gguf' --allow-pattern '*.md'
small SexGod1979/PinkCherry_NSFW_LTX23 22 --category Uncensored/Video \
  --folder-name PinkCherry-NSFW-LTX23-v1.8-Q8_0 \
  --allow-pattern 'v1.8/PinkCherry_FineTune_Q8_0_v1_8_LTX23.gguf' --allow-pattern '*.md'

# --- Archive-scale uncensored: Qwen3.8-Flash-Next uncensored, single IQ4_XS quant (staged locally)
small orcarouter/Qwen3.8-Flash-Next-Uncensored-GGUF 96 --category Uncensored/Multimodal --confirm-gated-access \
  --folder-name Qwen3.8-Flash-Next-Uncensored-IQ4_XS \
  --allow-pattern 'Qwen3.8-Flash-Next-Uncensored-IQ4_XS-0000?-of-00003.gguf' \
  --allow-pattern 'Qwen3.8-Flash-Next-Uncensored-MTP-draft.gguf' --allow-pattern '*mmproj*' --allow-pattern '*.md' --allow-pattern '*.json'

# --- Archives (GLM-5.3-Flash resumes where v3 stopped)
archive zai-org/GLM-5.3-Flash 306 Multimodal
archive deepseek-ai/DeepSeek-V4.1-Flash-1017 476 Multimodal
archive stepfun-ai/Step-5-Preview 606 LLM
# Nemotron 3.5 Super VL (daily radar 2026-11-04, approved): GGUF for AI-box testing + BF16 archive
small unsloth/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-GGUF 84 --category Multimodal \
  --folder-name NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-UD-Q4_K_XL \
  --allow-pattern 'UD-Q4_K_XL/*' --allow-pattern 'mmproj-BF16.gguf' --allow-pattern '*.md' --allow-pattern '*.json'
archive nvidia/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-BF16 232 Multimodal
# --- NVIDIA-only pack (2026-11-04): NVFP4 builds for a future RTX 50-series (Blackwell) card; won't run on Arc
archive nvidia/Qwen3.8-27B-NVFP4 21 NVIDIA-Only
archive nvidia/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-NVFP4 70 NVIDIA-Only
archive black-forest-labs/FLUX.2-dev-NVFP4 41 NVIDIA-Only
archive BennyDaBall/Qwen-Image-2.1-NVFP4 12 NVIDIA-Only
archive BennyDaBall/Qwen-Image-2.1-Turbo-NVFP4 15 NVIDIA-Only
archive BennyDaBall/LTX-2.5-22b-distilled-nvfp4-comfy-v2 18 NVIDIA-Only
archive XiaomiMiMo/MiMo-V2.6-Pro-RL 535 LLM
archive reflection/Beam-1.0-501B-A23B 934 LLM
archive tencent/Hy4-preview 1453 LLM
archive meta-models/Muse-Spark-Open-816B-A42B 1532 Multimodal
# Lowest priority: uncensored DeepSeek-1017 (stored in Uncensored/, not Archive-Huge/)
archive dealignai/DeepSeek-V4.1-Flash-1017-UNCENSORED-FP8 476 Uncensored/Multimodal \
  --target "$SHARE/Uncensored/Multimodal/DeepSeek-V4.1-Flash-1017-UNCENSORED-FP8"

# --- NVIDIA-only frontier archives (official NVFP4 of held models); last so the space guard skips them before the expansion
archive nvidia/GLM-5.3-Flash-NVFP4 191 NVIDIA-Only
archive nvidia/DeepSeek-V4-Flash-0731-NVFP4 164 NVIDIA-Only
archive reflection/Beam-1.0-501B-A23B-NVFP4 274 NVIDIA-Only
archive stepfun-ai/Step-5-Preview-NVFP4 368 NVIDIA-Only
archive nvidia/DeepSeek-V4.1-Flash-1017-NVFP4 400 NVIDIA-Only
archive meta-models/Muse-Spark-Open-816B-A42B-NVFP4 497 NVIDIA-Only

echo "Finished $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Failures: ${#FAILED[@]} ${FAILED[*]:-}"
echo "Skipped for space: ${#SKIPPED[@]} ${SKIPPED[*]:-}"
