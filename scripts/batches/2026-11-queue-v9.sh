#!/usr/bin/env bash
# Queue v9 (2026-11-06): v8 + popular-model archive wishlist at the end (behind the space guard).
# v8 (2026-11-06): v7 + rescan picks (AI-box models, MiniMax-H3/Krea-2/MOSS-Image, uncensored, Civitai, NVIDIA-only)
#   ahead of the archives; Hy4-preview + its NVFP4 removed until Hy4 final; Kimi-K3.1-Pro replaces Kimi-K3 NVFP4.
# v7 (2026-11-04): v6 + NVIDIA-only pack (after Nemotron) and NVIDIA-only frontier archives (at the end).
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

fits() {  # fits <needed_gib> <label>: wait (re-checking every 30 min) until the share keeps RESERVE_GIB free afterwards.
  # David is adding ~20 TB (2026-11-07): items no longer skip for space; the queue pauses and resumes by itself.
  local free announced=0
  while :; do
    free=$(df -g "$SHARE" 2>/dev/null | awk 'NR==2{print $4}')
    if [ -n "$free" ] && [ "$free" -ge $(( $1 + RESERVE_GIB )) ]; then
      [ "$announced" = 1 ] && echo "SPACE OK $(date -u +%Y-%m-%dT%H:%M:%SZ): ${free} GiB free, continuing with $2"
      return 0
    fi
    if [ "$announced" = 0 ]; then
      echo "WAITING (space) $(date -u +%Y-%m-%dT%H:%M:%SZ): $2 needs ${1} GiB, share has ${free:-?} GiB free (reserve ${RESERVE_GIB})"
      announced=1
    fi
    sleep 1800
  done
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

civ() {  # civ <civitai model id> <base model> [...]  -> Uncensored/Civitai/<base>/<type>/
  local id=$1; shift; local bases=(); for b in "$@"; do bases+=(--base-model "$b"); done
  echo "===== civitai $id [$*] ($(date -u +%Y-%m-%dT%H:%M:%SZ)) ====="
  python scripts/civitai.py download "$id" "${bases[@]}" --execute || FAILED+=("civitai:$id")
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

# --- 2026-11-06 rescan picks (David: "yes to all"), sized for the AI box; run before the archives
small unsloth/flint-GGUF 24 --category LLM --folder-name flint-UD-Q4_K_XL \
  --allow-pattern 'flint-UD-Q4_K_XL.gguf' --allow-pattern '*.md'
small bartowski/Nanbeige_Nanbeige4.3-33B-GGUF 20 --category LLM --folder-name Nanbeige4.3-33B-Q4_K_M \
  --allow-pattern 'Nanbeige_Nanbeige4.3-33B-Q4_K_M.gguf' --allow-pattern '*.md'
small Diffuspace/Clover-35B-A3B-Preview-GGUF 22 --category LLM --folder-name Clover-35B-A3B-Preview-Q4_K_M \
  --allow-pattern 'Clover-35B-A3B-Preview-Q4_K_M.gguf' --allow-pattern '*.md'
# Single 70.6 GiB GGUF exceeds the HF regular-download limit: use the per-file downloader
archive ornith-ai/Ornith-1.5-122B-GGUF 72 Multimodal --target "$SHARE/Multimodal/Ornith-1.5-122B-Q4_K_M" \
  --allow-pattern 'Ornith-1.5-122B-Q4_K_M.gguf' --allow-pattern 'mmproj-Ornith-1.5-122B-BF16.gguf' --allow-pattern '*.md'
small openbmb/MiniCPM-OCR-1.0 3 --category Vision-OCR
small LiquidAI/LFM3-Omni-2B 5 --category Multimodal
small maya-research/maya2-native 5 --category Speech-TTS
small gradium/phonon-31m-en 1 --category Speech-TTS
# New image/video bases (one ComfyUI variant each: fp8/bf16 weights that also load on Arc)
# 48 GiB text encoder exceeds the HF regular-download limit: per-file downloader
archive Comfy-Org/MiniMax-H3 80 Video --target "$SHARE/Video/MiniMax-H3-fl2va-pruned-fp8" \
  --allow-pattern 'diffusion_models/minimax_h3_fl2va_pruned_fp8_scaled.safetensors' \
  --allow-pattern 'text_encoders/qwen3vl_32b_minimax_h3_bf16.safetensors' \
  --allow-pattern 'vae/minimax_h3_audio_vae_fp32.safetensors' --allow-pattern 'vae/minimax_h3_sol_vae_fp16.safetensors' \
  --allow-pattern 'vae/minimax_h3_video_vae_fp16.safetensors' --allow-pattern 'loras/minimax_h3_fl2v_turbo_*' \
  --allow-pattern 'embeddings/*' --allow-pattern '*.md'
small Comfy-Org/Krea-2 39 --category Diffusion-Image --folder-name Krea-2-fp8 \
  --allow-pattern 'diffusion_models/krea2_turbo_fp8_scaled.safetensors' --allow-pattern 'diffusion_models/krea2_raw_fp8_scaled.safetensors' \
  --allow-pattern 'text_encoders/qwen3vl_4b_bf16.safetensors' --allow-pattern 'vae/*' --allow-pattern 'loras/*' \
  --allow-pattern '*.md' --allow-pattern 'LICENSE*'
small Comfy-Org/MOSS-Image 29 --category Diffusion-Image --folder-name MOSS-Image-SFT-bf16 \
  --allow-pattern 'diffusion_models/moss_image_sft_bf16.safetensors' --allow-pattern 'text_encoders/qwen3.5_9b_bf16.safetensors' \
  --allow-pattern 'vae/*' --allow-pattern 'loras/*' --allow-pattern '*.md'
# Uncensored additions
small HauhauCS/Gemma4-31B-QAT-Uncensored-HauhauCS-Balanced-MTP 19 --category Uncensored/LLM \
  --folder-name Gemma4-31B-QAT-Uncensored-HauhauCS-Balanced-Q4_K_M \
  --allow-pattern '*-Balanced-Q4_K_M.gguf' --allow-pattern 'mmproj-*' --allow-pattern '*.md'
small HauhauCS/Gemma4-26B-A4B-Uncensored-HauhauCS-Balanced 17 --category Uncensored/LLM \
  --folder-name Gemma4-26B-A4B-Uncensored-HauhauCS-Balanced-Q4_K_P \
  --allow-pattern '*-Balanced-Q4_K_P.gguf' --allow-pattern 'mmproj-*' --allow-pattern '*.md'
small orcarouter/Qwen3.8-27B-Uncensored-GGUF 17 --category Uncensored/Multimodal --confirm-gated-access \
  --folder-name Qwen3.8-27B-Uncensored-orcarouter-Q4_K_M \
  --allow-pattern 'Qwen3.8-27B-Uncensored-Q4_K_M.gguf' --allow-pattern 'mmproj-Qwen3.8-27B-Uncensored-f16.gguf' --allow-pattern '*.md'
# Civitai add-ons for held bases (free, SHA256-verified)
civ 2734359 'LTXV 2.5'
civ 2925394 'LTXV 2.5'
civ 1862761 'Qwen 2.1'
civ 2436859 'Qwen 2.1'
civ 2985682 'Qwen 2.1'
civ 3012015 'Qwen 2.1'
civ 2067704 'Flux.2 Klein 9B'
civ 2168120 'Flux.2 Klein 9B'
civ 2709984 'Flux.2 Klein 9B'
# NVIDIA-only additions
archive ornith-ai/Ornith-1.5-122B-NVFP4 73 NVIDIA-Only
archive unsloth/Qwen3.6-35B-A3B-NVFP4-Fast 23 NVIDIA-Only
archive axteam/Nanbeige4.3-33B-NVFP4 21 NVIDIA-Only

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
# removed 2026-11-06 (waiting for Hy4 final): archive tencent/Hy4-preview 1453 LLM
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
# Added 2026-11-04 at David's request (evaluate removals later): community NVFP4 where no official build exists, plus Kimi-K3
archive shanjiaz/gpt-oss-120b-nvfp4-modelopt 63 NVIDIA-Only
archive AMAImedia/MiniMax-M3.1-Flash-NVFP4-GGUF 233 NVIDIA-Only --exclude-prefix GGUF/ --exclude-prefix dspark/ --target "$SHARE/Archive-Huge/NVIDIA-Only/MiniMax-M3.1-Flash-NVFP4"
# removed 2026-11-06 (waiting for Hy4 final): archive Oxmiq/Hy4-preview-NVFP4-W4A16 457 NVIDIA-Only
archive com-kotobalabs/MiMo-V2.6-Pro-MOPD-Uncensored-NVFP4 600 NVIDIA-Only  # gated: needs David's click on HF
# replaced 2026-11-06 by Kimi-K3.1-Pro: archive nvidia/Kimi-K3-NVFP4 1500 NVIDIA-Only
archive moonshotai/Kimi-K3.1-Pro 1455 Multimodal

# --- Popular-model archive wishlist (2026-11-06, David: archive all popular models whether or not they run on the B70).
# Latest release per family; superseded versions skipped (GLM-5.2, DeepSeek-V4-Pro, Kimi-K2.6, Llama-2/3).
# Ordered smallest/most-used first; the space guard skips whatever does not fit until more disks are added.
# Full-precision references (< 150 GiB, active categories)
small Qwen/Qwen3.8-27B 52 --category Multimodal
small google/gemma-4-31B-it 59 --category Multimodal
small google/gemma-4-26B-A4B-it 49 --category Multimodal
small Qwen/Qwen3.6-35B-A3B 67 --category Multimodal
small nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16 62 --category Multimodal
small RecursiveSI/flint 75 --category LLM
small Nanbeige/Nanbeige4.3-33B 62 --category LLM
small Diffuspace/Clover-35B-A3B-Preview 65 --category LLM
small lodestones/Kromoss 61 --category Diffusion-Image
small PrunaAI/P-H3-Image 93 --category Diffusion-Image
small OpenMOSS-Team/MOSS-Image-SFT 26 --category Diffusion-Image
small OpenMOSS-Team/MOSS-Image-Base 26 --category Diffusion-Image
small krea/Krea-2-Turbo 58 --category Diffusion-Image --confirm-gated-access   # gated=auto: David accepts terms on HF
small krea/Krea-2-Raw 58 --category Diffusion-Image --confirm-gated-access     # gated=auto: David accepts terms on HF
# Archive-scale, most popular first
archive XiaomiMiMo/MiMo-V2.6-Flash-RL 166 LLM
archive Pika-Labs/Pika-H3-Flex 205 Video
archive ornith-ai/Ornith-1.5-122B 233 Multimodal
archive baidu/ERNIE-5.5-Flash-Base 269 LLM
archive Qwen/Qwen3.8-Flash-Next 336 Multimodal
archive MiniMaxAI/MiniMax-H3 465 Video
archive tencent/Hy3 557 LLM
archive deepseek-ai/DeepSeek-V3.2 643 LLM
archive zai-org/GLM-5.3 704 Multimodal
archive MiniMaxAI/MiniMax-M3 796 LLM
archive deepseek-ai/DeepSeek-V4-Pro-0813 832 LLM
archive mistralai/Mistral-Large-4-1T-A52B 988 Multimodal
archive nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16 1045 LLM
archive deep-principle/Hydrogen-1.0 1404 LLM   # gated=auto: David accepts terms on HF

echo "Finished $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Failures: ${#FAILED[@]} ${FAILED[*]:-}"
echo "Skipped for space: ${#SKIPPED[@]} ${SKIPPED[*]:-}"
