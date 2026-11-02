#!/usr/bin/env bash
# Civitai starter set (2026-11-02): free uncensored add-ons/checkpoints for bases already in the
# library (LTX-2.3/2.5, Qwen-Image 2.1, FLUX.2-klein-9B). Versions are pinned by base model.
# Safety filter + SHA256 verify in civitai.py. Requires David's VPN (Civitai blocks Australia).
# Resumable; failures don't stop the batch.
set -uo pipefail
cd "/Users/davideddy/AI Models"
source .venv/bin/activate
trap 'echo "Stopped by signal $(date -u +%Y-%m-%dT%H:%M:%SZ)"; kill 0; exit 130' TERM INT
FAILED=()
dl() {  # dl <model_id> <base model> [<base model>...]  (files to Uncensored/Civitai/<base>/<type>/)
  local id=$1; shift 1
  local bases=(); for b in "$@"; do bases+=(--base-model "$b"); done
  echo "===== civitai $id [$*] ($(date -u +%H:%M:%SZ)) ====="
  python scripts/civitai.py download "$id" "${bases[@]}" --execute || FAILED+=("$id")
}

LTX=("LTXV 2.3" "LTXV 2.5" "LTXV2")
QWEN=("Qwen 2.1")
KLEIN=("Flux.2 Klein 9B")

# LTX video
dl 1811313 "${LTX[@]}"            # DR34ML4Y All-In-One NSFW LoRA
dl 1648982 "${LTX[@]}"            # NSFW Posing Nude LoRA
dl 2497207 "${LTX[@]}"            # Video reasoning LoRA (VBVR)
dl 1343431 "${LTX[@]}"            # Bouncing physics LoRA
dl 2447875 "${LTX[@]}"            # LTX 10Eros checkpoint (27 GiB)
# Qwen-Image 2.1
dl 958009 "${QWEN[@]}"   # RedCraft checkpoint
dl 2958918 "${QWEN[@]}"   # NSFW LoRA | Qwen Image 2.1
dl 1662740 "${QWEN[@]}"   # Lenovo UltraReal realism LoRA
dl 2063193 "${QWEN[@]}" "${KLEIN[@]}"   # NSFW UNLOCKED LoRA
# FLUX.2-klein-9B
dl 1972981 "${KLEIN[@]}"  # SNOFS LoRA
dl 2416142 "${KLEIN[@]}"  # SNOFS Merged checkpoint
dl 2382648 "${KLEIN[@]}"  # PornMaster Flux2 Klein checkpoint
dl 2319552 "${KLEIN[@]}"  # 0x7 NSFW Flux Klein LoRA

echo "Finished $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Failures: ${#FAILED[@]} ${FAILED[*]:-}"
