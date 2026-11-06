#!/usr/bin/env python3
"""Write `_HOW_TO_USE.md` into model folders that need a base model or companion files,
and mark Uncensored/Civitai models as protected (never a cleanup candidate).

Covers every folder under `Uncensored/`, plus mainstream add-on folders (GGUF transformer-only
quants and LoRA folders) listed in ADDON_FOLDERS. Idempotent: re-run after each batch.

    python scripts/write_how_to_use.py            # write/refresh all
    python scripts/write_how_to_use.py --dry-run  # print what would be written
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path("/Users/davideddy/mnt/models")
META = "_hermes_model_metadata.json"
OUT = "_HOW_TO_USE.md"

# Civitai baseModel -> (friendly name, library folder(s) to load, note)
BASES = {
    "qwen 2.1": ("Qwen-Image 2.1", ["Diffusion-Image/Qwen-Image-2.1"],
                 "Also works with `Diffusion-Image/Qwen-Image-2.1-Turbo` (fewer steps)."),
    "qwen 2": ("Qwen-Image 2", ["Diffusion-Image/Qwen-Image-2.1"], "Built for Qwen-Image 2; usually works on 2.1, test first."),
    "flux.2 klein 9b": ("FLUX.2 [klein] 9B", ["Diffusion-Image/FLUX.2-klein-9b-fp8", "Diffusion-Image/FLUX.2-klein-9B"],
                        "Use the fp8 folder on the AI box; the full folder is the reference copy."),
    "ltxv 2.3": ("LTX-2.3 (video)", ["Uncensored/Video/LTX-2.3-uncensored-v1.4-fp8mixed"],
                 "That folder has the LTX-2.3 diffusion model plus the text encoder, VAEs, upscaler and example ComfyUI workflows."),
    "ltxv 2.5": ("LTX-2.5 (video)", ["Uncensored/Video/LTX-2.5-uncensored-v1.1-fp8_scaled"],
                 "That folder has the LTX-2.5 diffusion model plus text encoder, VAEs, upscalers and workflows."),
    "ltxv2": ("LTX-2 family (video)", ["Uncensored/Video/LTX-2.3-uncensored-v1.4-fp8mixed"], "Built for LTX-2; use with LTX-2.3."),
    "krea 2": ("Krea 2 (image)", ["Diffusion-Image/Krea-2-fp8"], "Use `krea2_raw_fp8_scaled` with the Qwen3-VL 4B text encoder and VAE in that folder."),
    "krea 2 turbo": ("Krea 2 Turbo (image)", ["Diffusion-Image/Krea-2-fp8"], "Use `krea2_turbo_fp8_scaled` (fewer steps) from that folder."),
    "minimax h3": ("MiniMax-H3 (video)", ["Video/MiniMax-H3-fl2va-pruned-fp8"],
                   "That folder has the pruned fp8 video model, Qwen3-VL 32B text encoder, VAEs and turbo LoRAs."),
    "moss image": ("MOSS-Image", ["Diffusion-Image/MOSS-Image-SFT-bf16"], "That folder has the SFT model, Qwen3.5 9B text encoder and VAE."),
}

# Curated guidance for specific folders (path relative to ROOT).
CURATED: dict[str, dict] = {
    "Uncensored/Video/LTX-2.3-uncensored-v1.4-fp8mixed": {
        "kind": "Complete LTX-2.3 video model bundle (uncensored fine-tune)",
        "base": "None needed: this IS a base model. LTX-2.3 LoRAs in `Uncensored/Video/` load on top of it.",
        "load": ["`split/diffusion_models/ltxv23_uncensored_v1.4_fp8mixed.safetensors` → ComfyUI `models/diffusion_models/`",
                 "`split/text_encoders/*` (abliterated Gemma-3-12B Q4_K_M + projections) → `models/text_encoders/` (GGUF needs ComfyUI-GGUF)",
                 "`split/vae/*` (video + audio VAE) → `models/vae/`",
                 "`split/latent_upscale_models/*` → `models/latent_upscale_models/` (optional 2× upscale)",
                 "Start from `workflow_examples/*.json` (T2AV / I2AV / A2AV)."],
        "hw": "B70 (32 GB): fp8 fits. A380 (6 GB): needs heavy offload; very slow.",
    },
    "Uncensored/Video/LTX-2.5-uncensored-v1.1-fp8_scaled": {
        "kind": "Complete LTX-2.5 video model bundle (uncensored fine-tune)",
        "base": "None needed: this IS a base model. LTX-2.5 LoRAs load on top of it.",
        "load": ["`split/diffusion_models/ltx25_uncensored_v1.1-fp8_scaled.safetensors` → `models/diffusion_models/`",
                 "`split/text_encoders/gemma4_12b_ltx25_uncensored-int8.safetensors` → `models/text_encoders/`",
                 "`split/vae/*` → `models/vae/`; `split/latent_upscale_models/*` (spatial + temporal 2×) → `models/latent_upscale_models/`",
                 "Start from `workflow_examples/*.json` (T2V / I2V)."],
        "hw": "B70: fits. A380: offload, very slow.",
    },
    "Uncensored/Video/PinkCherry-NSFW-LTX23-v1.8-Q8_0": {
        "kind": "LTX-2.3 full fine-tune (diffusion model only, GGUF Q8_0)",
        "base": "Replaces the LTX-2.3 diffusion model. Take the text encoder, VAEs and upscaler from `Uncensored/Video/LTX-2.3-uncensored-v1.4-fp8mixed/split/`.",
        "load": ["`v1.8/PinkCherry_FineTune_Q8_0_v1_8_LTX23.gguf` → `models/unet/` via ComfyUI-GGUF *Unet Loader (GGUF)*",
                 "Use the LTX-2.3 workflows from the LTX-2.3 folder, swapping the model loader."],
    },
    "Uncensored/Diffusion-Image/Qwen-Image-2.1-Uncensored-Q8_0": {
        "kind": "Complete uncensored Qwen-Image 2.1 set (GGUF transformer + uncensored text encoder + VAE)",
        "base": "None needed: standalone. (Original Qwen-Image 2.1 is `Diffusion-Image/Qwen-Image-2.1`.)",
        "load": ["`qwen-image-2.1-UC-Q8_0.gguf` → `models/unet/` (ComfyUI-GGUF Unet Loader)",
                 "`text_encoders/qwen3vl_8b_int8_convrot.safetensors` → `models/text_encoders/`",
                 "`vae/*` → `models/vae/`"],
        "hw": "B70: fits comfortably. A380: Q8 needs offload; slow.",
    },
    "Uncensored/Diffusion-Image/Noct-Q-Uncensored-Qwen-Image-2.1-V4": {
        "kind": "Qwen-Image 2.1 fine-tune checkpoint (diffusion model only, int8)",
        "base": "Replaces the Qwen-Image 2.1 diffusion model. Text encoder + VAE: from `Diffusion-Image/Qwen-Image-2.1`, or the uncensored encoder in `Uncensored/Diffusion-Image/Qwen-Image-2.1-Uncensored-Q8_0` / `Qwen-Image-2.1-Text-Encoder-Heretic-fp8`.",
        "load": ["`NoctQ_V4_int8_convrot.safetensors` → `models/diffusion_models/`", "Start from `NoctQ_V4_workflow.json`."],
    },
    "Uncensored/Diffusion-Image/qwen-image-edit-plus-nsfw-lora": {
        "kind": "LoRA (image editing)",
        "base": "Qwen-Image-Edit-2511: `Diffusion-Image/Qwen-Image-Edit-2511` (full) or `Qwen-Image-Edit-2511-GGUF-Q8_0` / `-Q4_K_M` (+ text encoder/VAE from the full folder).",
        "load": ["`qwen-image-edit-plus-nsfw-lora.safetensors` → `models/loras/`, load with *LoraLoaderModelOnly* after the Edit model.",
                 "Optional speed-up: also add `Diffusion-Image/Qwen-Image-Edit-2511-Lightning-LoRAs` (4 or 8 steps)."],
    },
    "Uncensored/Diffusion-Image/Qwen-Image-2.1-Text-Encoder-Heretic-fp8": {
        "kind": "Uncensored (heretic) text encoder for Qwen-Image 2.1",
        "base": "Swap in for the normal text encoder of `Diffusion-Image/Qwen-Image-2.1` (also Noct-Q / RedCraft Qwen-Image checkpoints).",
        "load": ["`qwen3vl_8b_fp8_heretic.safetensors` → `models/text_encoders/`, select it in the CLIP/text-encoder loader instead of the stock one."],
    },
    "Uncensored/Diffusion-Image/Qwen-Image-2.1-Turbo-Uncensored-Q8_0": {
        "kind": "Uncensored text encoder for Qwen-Image 2.1 Turbo (GGUF, Qwen3-VL-8B based)",
        "base": "Use with `Diffusion-Image/Qwen-Image-2.1-Turbo` in place of its stock text encoder.",
        "load": ["`Qwen-Image-2.1-Turbo-Uncensored-Q8_0.gguf` (+ `mmproj-*-F16.gguf`) → `models/text_encoders/` via ComfyUI-GGUF CLIP loader."],
    },
    "Uncensored/Diffusion-Image/flux2-klein-9b-uncensored-text-encoder-q8_0": {
        "kind": "Uncensored text encoder for FLUX.2 [klein] 9B (GGUF)",
        "base": "Use with `Diffusion-Image/FLUX.2-klein-9b-fp8` (or `FLUX.2-klein-9B`) in place of its stock text encoder.",
        "load": ["`flux2-klein-9b-uncensored-q8_0.gguf` → `models/text_encoders/` via ComfyUI-GGUF CLIP loader."],
    },
    "Uncensored/Multimodal/Qwen3.8-Flash-Next-Uncensored-IQ4_XS": {
        "kind": "Standalone uncensored chat/vision model (GGUF, split in 3 parts)",
        "base": "None needed.",
        "load": ["Point llama.cpp / LM Studio at `...-IQ4_XS-00001-of-00003.gguf` (it loads the other parts).",
                 "Vision: add `mmproj-*.gguf`. Faster decoding: `...-MTP-draft.gguf` as the draft model."],
        "hw": "~91 GiB: needs ~96 GB+ RAM+VRAM combined (MoE offload). Not practical on a single B70 alone.",
    },
    "Uncensored/Multimodal/DeepSeek-V4.1-Flash-1017-UNCENSORED-FP8": {
        "kind": "Archive-scale uncensored DeepSeek-V4.1-Flash-1017 (FP8 safetensors)",
        "base": "None needed.",
        "load": ["Serve with vLLM / SGLang on a multi-GPU server. Keep on the file server; not runnable on the AI box."],
    },
    # Mainstream add-on folders
    "Diffusion-Image/Qwen-Image-Edit-2511-GGUF-Q8_0": {
        "kind": "Qwen-Image-Edit-2511 diffusion model only (GGUF Q8_0)",
        "base": "Text encoder + VAE come from `Diffusion-Image/Qwen-Image-Edit-2511` (`text_encoder/`, `vae/`).",
        "load": ["`qwen-image-edit-2511-Q8_0.gguf` → `models/unet/` (ComfyUI-GGUF Unet Loader)."],
        "hw": "B70: best quality/size balance.",
    },
    "Diffusion-Image/Qwen-Image-Edit-2511-GGUF-Q4_K_M": {
        "kind": "Qwen-Image-Edit-2511 diffusion model only (GGUF Q4_K_M)",
        "base": "Text encoder + VAE come from `Diffusion-Image/Qwen-Image-Edit-2511`.",
        "load": ["`qwen-image-edit-2511-Q4_K_M.gguf` → `models/unet/` (ComfyUI-GGUF Unet Loader)."],
        "hw": "B70: fast. A380: works with CPU/RAM offload; pair with the Lightning 4-step LoRA.",
    },
    "Diffusion-Image/Qwen-Image-Edit-2511-Lightning-LoRAs": {
        "kind": "Speed LoRAs (4-step and 8-step)",
        "base": "Qwen-Image-Edit-2511 (full or either GGUF folder).",
        "load": ["`*-4steps-*.safetensors` or `*-8steps-*.safetensors` → `models/loras/`; set steps to 4/8 and CFG ≈ 1."],
    },
}


def hf_base(repo_id: str | None) -> str | None:
    """Original (non-quantised) base model from the Hugging Face card, for the readme."""
    if not repo_id or ":" in repo_id:
        return None
    try:
        from huggingface_hub import model_info
        tags = model_info(repo_id).tags or []
    except Exception:  # noqa: BLE001 - informational only
        return None
    bases = [t.split(":", 1)[1] for t in tags if t.startswith("base_model:") and t.count(":") == 1]
    return bases[0] if bases else None


def gguf_llm_guide(md: dict, files: list[str]) -> dict:
    ggufs = [f for f in files if f.endswith(".gguf") and "mmproj" not in f.lower() and "mtp" not in f.lower()]
    mmproj = [f for f in files if "mmproj" in f.lower()]
    mtp = [f for f in files if "mtp" in f.lower() and f.endswith(".gguf")]
    load = [f"Load `{ggufs[0]}` in llama.cpp / LM Studio / Ollama / koboldcpp." if ggufs else "Load the .gguf file."]
    if mmproj:
        load.append(f"Image input: also load `{mmproj[0]}` (llama.cpp `--mmproj`).")
    if mtp:
        load.append(f"Optional faster decoding: `{mtp[0]}` as the draft / MTP model (llama.cpp `--model-draft` or MTP support).")
    base = hf_base(md.get("repo_id"))
    return {"kind": "Standalone uncensored chat model (GGUF)",
            "base": "None needed: runs on its own." + (f" Built from `{base}` (via `{md.get('repo_id')}`)." if base else f" Source repo `{md.get('repo_id')}`."),
            "load": load}


def size_gib(folder: Path) -> float:
    return sum(p.stat().st_size for p in folder.rglob("*") if p.is_file()) / 1024**3


def guide_for(rel: str, folder: Path, md: dict) -> dict | None:
    if rel in CURATED:
        return CURATED[rel]
    files = sorted(str(p.relative_to(folder)) for p in folder.rglob("*") if p.is_file() and not p.name.startswith("_"))
    if md.get("source") == "civitai":
        base_key = str(md.get("base_model") or "").lower()
        name, paths, note = BASES.get(base_key, (md.get("base_model"), [], "That base model is NOT in the library yet."))
        typ = md.get("model_type")
        kind = {"LORA": "LoRA", "Checkpoint": "Checkpoint (full fine-tune)", "LoCon": "LoRA (LoCon)"}.get(typ, typ)
        load = []
        if typ in ("LORA", "LoCon"):
            load.append(f"`{files[0] if files else 'the .safetensors'}` → ComfyUI `models/loras/`; apply with *LoraLoaderModelOnly* (start at strength 0.7–1.0).")
        else:
            load.append(f"`{next((f for f in files if f != 'civitai_model.json'), 'the model file')}` → `models/diffusion_models/` (or `checkpoints/` if it bundles the text encoder/VAE); "
                        "it replaces the base diffusion model, keep the base's text encoder and VAE.")
        if md.get("trained_words"):
            load.append("Trigger words: " + ", ".join(f"`{w}`" for w in md["trained_words"][:12]))
        load.append("Full model card and settings: `civitai_model.json`.")
        base = f"{name}: " + (" or ".join(f"`{p}`" for p in paths) if paths else "(not in library)") + (f". {note}" if note else "")
        return {"kind": f"{kind} from Civitai", "base": base, "load": load}
    if any(f.endswith(".gguf") for f in files) and rel.split("/")[1] in {"LLM", "Coding", "Multimodal"}:
        return gguf_llm_guide(md, files)
    return None


def render(rel: str, folder: Path, md: dict, g: dict) -> str:
    src = md.get("url") or (f"https://huggingface.co/{md['repo_id']}" if md.get("repo_id") else "")
    lines = [f"# How to use: {folder.name}", "",
             f"- **What it is:** {g['kind']}",
             f"- **Base model to use:** {g['base']}",
             f"- **Library path:** `{rel}` ({size_gib(folder):.1f} GiB)",
             f"- **Source:** {src}"]
    if g.get("hw"):
        lines.append(f"- **AI box:** {g['hw']}")
    lines += ["", "## Files to load", ""] + [f"- {x}" for x in g["load"]]
    if rel.startswith("Uncensored/"):
        lines += ["", "Protected: kept by request. Never a cleanup or replacement candidate."]
    lines += ["", "_Generated by `scripts/write_how_to_use.py`._", ""]
    return "\n".join(lines)


def write_one(folder: Path) -> bool:
    """Write the readme (and protected flag) for one folder; used by the downloaders after a
    verified download. Returns True if a readme was written."""
    try:
        rel = str(folder.relative_to(ROOT))
        md = json.loads((folder / META).read_text())
    except Exception:  # noqa: BLE001 - never fail a download over the readme
        return False
    if not (rel.startswith("Uncensored/") or rel in CURATED):
        return False
    g = guide_for(rel, folder, md)
    if not g:
        return False
    (folder / OUT).write_text(render(rel, folder, md, g), encoding="utf-8")
    if rel.startswith("Uncensored/") and not md.get("protected"):
        md["protected"] = True
        md["protected_reason"] = "Kept by David's request; never a cleanup or replacement candidate."
        (folder / META).write_text(json.dumps(md, indent=2), encoding="utf-8")
    print(f"Wrote {rel}/{OUT}")
    return True


def folders() -> list[Path]:
    out = sorted(p.parent for p in (ROOT / "Uncensored").glob("*/*/" + META))
    out += sorted(p.parent for p in (ROOT / "Uncensored" / "Civitai").glob("*/*/*/" + META))
    out += [ROOT / rel for rel in CURATED if not rel.startswith("Uncensored/") and (ROOT / rel / META).exists()]
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    written = skipped = 0
    for folder in folders():
        rel = str(folder.relative_to(ROOT))
        md = json.loads((folder / META).read_text())
        g = guide_for(rel, folder, md)
        if not g:
            print(f"skip (no guidance rule): {rel}")
            skipped += 1
            continue
        text = render(rel, folder, md, g)
        if args.dry_run:
            print(f"----- {rel}/{OUT}\n{text}")
            continue
        (folder / OUT).write_text(text, encoding="utf-8")
        if rel.startswith("Uncensored/") and not md.get("protected"):
            md["protected"] = True
            md["protected_reason"] = "Kept by David's request; never a cleanup or replacement candidate."
            (folder / META).write_text(json.dumps(md, indent=2), encoding="utf-8")
        written += 1
        print(f"wrote {rel}/{OUT}")
    print(f"Done: {written} written, {skipped} skipped")


if __name__ == "__main__":
    main()
