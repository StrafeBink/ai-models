#!/usr/bin/env bash
# Combined queue approved 2026-10-29 (supersedes 2026-10-archives-v2.sh).
# Order: remaining AI-box picks -> Uncensored starter catalogue -> archives (smallest first,
# gated Muse-Spark last). Resumable: completed files/models are skipped. A failed model
# does not stop the batch; SIGTERM/SIGINT stops everything.
set -uo pipefail
cd "/Users/davideddy/AI Models"
source .venv/bin/activate

trap 'echo "Stopped by signal $(date -u +%Y-%m-%dT%H:%M:%SZ)"; kill 0; exit 130' TERM INT

FAILED=()
COMMON=(--execute --resume --staging-dir download-staging --staging-copy-method rsync-inplace --max-workers 2)
small() {  # staged download for AI-box sized models; extra args pass through
  echo "===== $1 ($(date -u +%Y-%m-%dT%H:%M:%SZ)) ====="
  python scripts/hf_model_manager.py download "$@" "${COMMON[@]}" || FAILED+=("$1")
}
archive() {  # per-file staged download into Archive-Huge/<family>
  echo "===== $1 ($(date -u +%Y-%m-%dT%H:%M:%SZ)) ====="
  python scripts/download_archive_per_file.py "$1" --category "$2" || FAILED+=("$1")
}

echo "Started $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# --- Remaining AI-box picks
small baidu/Unlimited-OCR-2 --category Vision-OCR
small Cloudflare/clef-flash --category Multimodal
small Qwen/Qwen-Image-2.1-Turbo --category Diffusion-Image

# --- Uncensored starter catalogue (single quants sized for the AI box)
small huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF --category Uncensored/LLM \
  --folder-name Huihui-Qwen3.8-27B-abliterated-Q4_K \
  --allow-pattern 'Huihui-Qwen3.8-27B-abliterated-Q4_K.gguf' --allow-pattern '*mmproj*' --allow-pattern '*.md' --allow-pattern '*.json'
small HauhauCS/Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive --category Uncensored/LLM \
  --folder-name Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive-Q4_K_M \
  --allow-pattern '*-Q4_K_M.gguf' --allow-pattern 'mmproj-*' --allow-pattern '*.md' --allow-pattern '*.json'
small HauhauCS/Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced-MTP --category Uncensored/LLM
small HauhauCS/Gemma-4-E4B-Uncensored-HauhauCS-Aggressive --category Uncensored/LLM \
  --folder-name Gemma-4-E4B-Uncensored-HauhauCS-Aggressive-Q4_K_M \
  --allow-pattern '*-Q4_K_M.gguf' --allow-pattern 'mmproj-*' --allow-pattern '*.md' --allow-pattern '*.json'
small HauhauCS/Qwen3.5-9B-Uncensored-HauhauCS-Aggressive --category Uncensored/LLM \
  --folder-name Qwen3.5-9B-Uncensored-HauhauCS-Aggressive-Q4_K_M \
  --allow-pattern '*-Q4_K_M.gguf' --allow-pattern 'mmproj-*' --allow-pattern '*.md' --allow-pattern '*.json'
small DavidAU/OpenAi-GPT-oss-20b-abliterated-uncensored-NEO-Imatrix-gguf --category Uncensored/LLM \
  --folder-name GPT-oss-20b-abliterated-NEO-Uncensored2-IQ4_NL \
  --allow-pattern 'OpenAI-20B-NEO-Uncensored2-IQ4_NL.gguf' --allow-pattern '*.md' --allow-pattern '*.json'
small abenzerps/Qwen-Image-2.1-Uncensored-Quantized --category Uncensored/Diffusion-Image \
  --folder-name Qwen-Image-2.1-Uncensored-Q8_0 \
  --allow-pattern 'qwen-image-2.1-UC-Q8_0.gguf' --allow-pattern 'text_encoders/qwen3vl_8b_int8_convrot.safetensors' \
  --allow-pattern 'vae/*' --allow-pattern '*.md' --allow-pattern '*.json'

# --- Qwen-Image-Edit-2511 (base for the edit LoRA below): full model + homelab-sized variants
small Qwen/Qwen-Image-Edit-2511 --category Diffusion-Image
small unsloth/Qwen-Image-Edit-2511-GGUF --category Diffusion-Image \
  --folder-name Qwen-Image-Edit-2511-GGUF-Q8_0 \
  --allow-pattern 'qwen-image-edit-2511-Q8_0.gguf' --allow-pattern '*.md' --allow-pattern '*.json'
small unsloth/Qwen-Image-Edit-2511-GGUF --category Diffusion-Image \
  --folder-name Qwen-Image-Edit-2511-GGUF-Q4_K_M \
  --allow-pattern 'qwen-image-edit-2511-Q4_K_M.gguf' --allow-pattern '*.md' --allow-pattern '*.json'
small lightx2v/Qwen-Image-Edit-2511-Lightning --category Diffusion-Image \
  --folder-name Qwen-Image-Edit-2511-Lightning-LoRAs \
  --allow-pattern 'Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors' \
  --allow-pattern 'Qwen-Image-Edit-2511-Lightning-8steps-V1.0-bf16.safetensors' --allow-pattern '*.md'

# --- Uncensored image/video additions (approved 2026-10-29). One variant each.
small Noctaluna/Noct-Q-Uncensored-Qwen-Image-2.1 --category Uncensored/Diffusion-Image \
  --folder-name Noct-Q-Uncensored-Qwen-Image-2.1-V4 \
  --allow-pattern 'NoctQ_V4*' --allow-pattern 'LICENSE' --allow-pattern 'NOTICE' --allow-pattern '*.md' --allow-pattern 'images/*'
small ScottzillaSystems/qwen-image-edit-plus-nsfw-lora --category Uncensored/Diffusion-Image
small ChrisColeTech/LTX-2.3-uncensored-v1.4-FP8 --category Uncensored/Video \
  --folder-name LTX-2.3-uncensored-v1.4-fp8mixed \
  --allow-pattern 'split/diffusion_models/ltxv23_uncensored_v1.4_fp8mixed.safetensors' \
  --allow-pattern 'split/text_encoders/*' --allow-pattern 'split/vae/*' \
  --allow-pattern 'split/latent_upscale_models/ltx-2.3-spatial-upscaler-x2-1.1.safetensors' \
  --allow-pattern 'workflow_examples/*' --allow-pattern '*.md'
small ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8 --category Uncensored/Video \
  --folder-name LTX-2.5-uncensored-v1.1-fp8_scaled \
  --allow-pattern 'split/diffusion_models/ltx25_uncensored_v1.1-fp8_scaled.safetensors' \
  --allow-pattern 'split/text_encoders/gemma4_12b_ltx25_uncensored-int8.safetensors' \
  --allow-pattern 'split/vae/*' --allow-pattern 'split/latent_upscale_models/*' \
  --allow-pattern 'workflow_examples/*' --allow-pattern '*.md'

# --- Archives, smallest first (DeepSeek-V4-Flash resumes at file 26/74)
archive deepseek-ai/DeepSeek-V4-Flash-0731 LLM
archive nvidia/Qwen3.8-Flash-Next-FP4-Local Multimodal
archive MiniMaxAI/MiniMax-M3.1-Flash Multimodal
archive zai-org/GLM-5.3-Flash Multimodal
archive deepseek-ai/DeepSeek-V4.1-Flash-1017 Multimodal
archive XiaomiMiMo/MiMo-V2.6-Pro-RL LLM
archive stepfun-ai/Step-5-Preview LLM
archive reflection/Beam-1.0-501B-A23B LLM
archive tencent/Hy4-preview LLM
# Gated (manual approval on Hugging Face); last so David has time to get access.
archive meta-models/Muse-Spark-Open-816B-A42B Multimodal

echo "Finished $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Failures: ${#FAILED[@]} ${FAILED[*]:-}"
