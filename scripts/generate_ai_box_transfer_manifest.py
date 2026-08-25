#!/usr/bin/env python3
"""Generate an AI-box transfer manifest from the verified model library.

The Mac/model share is the source of truth. This script does not copy anything;
it creates a checklist for manual transfer to the separate AI box.

Examples:
  python scripts/generate_ai_box_transfer_manifest.py --bundle minimal-rag
  python scripts/generate_ai_box_transfer_manifest.py --model LLM/Qwen3-32B-Q5_K_M --model Safety-Moderation/Prompt-Guard-86M
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT = REPO_ROOT / "reports" / "model-library-audit-post-cleanup-20260821-133801Z.json"
OUT_DIR = REPO_ROOT / "transfer-manifests"

BUNDLES: dict[str, list[str]] = {
    "minimal-rag": [
        "Embeddings/all-MiniLM-L6-v2",
        "Safety-Moderation/Prompt-Guard-86M",
        "LLM/Qwen3-32B-Q5_K_M",
    ],
    "coding-assistant": [
        "Coding/Qwen3-Coder-30B-A3B-UD-Q4_K_XL",
        "LLM/GPT-OSS-20B",
        "Safety-Moderation/Prompt-Guard-86M",
    ],
    "speech-and-docs": [
        "Speech-STT/whisper-large-v3-turbo",
        "Vision-OCR/DeepSeek-OCR-2",
        "Embeddings/all-MiniLM-L6-v2",
    ],
    "image-generation-small-first": [
        "Diffusion-Image/FLUX.2-klein-9b-fp8",
        "Diffusion-Image/FLUX.1-schnell",
    ],
    "llm-comparison": [
        "LLM/Qwen3-32B-Q5_K_M",
        "LLM/GPT-OSS-20B",
        "LLM/Ministral-3-14B-Q5_K_M",
        "LLM/Gemma-3-27B-QAT-Q4_0",
    ],
}


@dataclass
class ManifestItem:
    selector: str
    repo_id: str
    source_path: str
    size_gib: float
    payload_files: int
    ai_box_runtime_hint: str
    verification_command_hint: str


def location(row: dict[str, Any]) -> str:
    if row.get("scope") == "archive":
        return f"Archive-Huge/{row.get('archive_family')}"
    return str(row.get("category"))


def runtime_hint(selector: str, repo_id: str) -> str:
    text = f"{selector} {repo_id}".lower()
    if "embedding" in text or "minilm" in text or "mpnet" in text:
        return "sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants"
    if "prompt-guard" in text:
        return "transformers sequence-classification on AI box"
    if "whisper" in text or "asr" in text:
        return "faster-whisper preferred; transformers fallback"
    if "ocr" in text:
        return "transformers/custom model code on AI box"
    if "flux" in text or "stable-diffusion" in text or "stable-video" in text:
        return "ComfyUI or diffusers on AI box"
    if "audio" in text or "personaplex" in text:
        return "model-specific audio/diffusers stack on AI box"
    if "gguf" in text or "q4_" in text or "q5_" in text or "coder" in text:
        return "llama.cpp/GGUF-compatible runtime on AI box"
    return "inspect upstream model card and local metadata before transfer"


def load_inventory() -> dict[str, dict[str, Any]]:
    rows = json.loads(AUDIT.read_text(encoding="utf-8"))
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        if row.get("scope") == "workflow":
            continue
        sel = f"{location(row)}/{row['folder_name']}"
        out[sel] = row
        out[row["folder_name"]] = row
        if row.get("repo_id"):
            out[row["repo_id"]] = row
    return out


def make_item(selector: str, row: dict[str, Any]) -> ManifestItem:
    src = row["path"]
    return ManifestItem(
        selector=selector,
        repo_id=row.get("repo_id") or "unknown",
        source_path=src,
        size_gib=float(row.get("size_gib") or 0),
        payload_files=int(row.get("payload_file_count") or 0),
        ai_box_runtime_hint=runtime_hint(selector, row.get("repo_id") or ""),
        verification_command_hint=f"Compare source and AI-box copy: size ≈ {float(row.get('size_gib') or 0):.2f} GiB, payload files = {int(row.get('payload_file_count') or 0)}, metadata file present",
    )


def write_manifest(items: list[ManifestItem], label: str, dest_root: str) -> Path:
    OUT_DIR.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    path = OUT_DIR / f"ai-box-transfer-{label}-{stamp}.md"
    total = sum(i.size_gib for i in items)
    lines = [
        f"# AI Box Transfer Manifest: {label}",
        "",
        f"Generated: {stamp}",
        f"Destination root placeholder: `{dest_root}`",
        f"Models: `{len(items)}`",
        f"Total estimated transfer size: `{total:.2f} GiB`",
        "",
        "## Transfer checklist",
        "",
        "- [ ] Confirm available free space on the AI box.",
        "- [ ] Copy one model at a time or one bundle at a time.",
        "- [ ] Preserve directory structure under the AI-box model root.",
        "- [ ] Verify `_hermes_model_metadata.json` exists after copy.",
        "- [ ] Verify approximate size and payload file count after copy.",
        "- [ ] Run the AI-box runtime benchmark/smoke test.",
        "- [ ] Record result back into this repo.",
        "",
        "## Models",
        "",
        "| Model | Repo | Size | Payload files | AI-box runtime hint | Source | Suggested destination |",
        "|---|---|---:|---:|---|---|---|",
    ]
    for item in items:
        rel = "/".join(Path(item.source_path).parts[-2:])
        dest = f"{dest_root.rstrip('/')}/{rel}"
        lines.append(f"| `{item.selector}` | `{item.repo_id}` | {item.size_gib:.2f} GiB | {item.payload_files} | {item.ai_box_runtime_hint} | `{item.source_path}` | `{dest}` |")
    lines += ["", "## Per-model verification notes", ""]
    for item in items:
        lines += [
            f"### `{item.selector}`",
            "",
            f"- Source: `{item.source_path}`",
            f"- Repo: `{item.repo_id}`",
            f"- Expected size: `{item.size_gib:.2f} GiB`",
            f"- Expected payload files excluding `.cache`: `{item.payload_files}`",
            f"- Metadata: `_hermes_model_metadata.json` should exist in the destination folder.",
            f"- Runtime hint: {item.ai_box_runtime_hint}",
            f"- Verification: {item.verification_command_hint}",
            "",
        ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", choices=sorted(BUNDLES), help="Predefined transfer bundle")
    parser.add_argument("--model", action="append", help="Model selector: repo_id, folder name, or Location/folder. Repeatable.")
    parser.add_argument("--label", help="Manifest label; defaults to bundle or custom")
    parser.add_argument("--dest-root", default="/path/on/ai-box/models", help="AI-box destination root placeholder")
    parser.add_argument("--list-bundles", action="store_true")
    args = parser.parse_args()

    if args.list_bundles:
        for name, selectors in BUNDLES.items():
            print(f"{name}: {', '.join(selectors)}")
        return 0

    selectors: list[str] = []
    if args.bundle:
        selectors.extend(BUNDLES[args.bundle])
    if args.model:
        selectors.extend(args.model)
    if not selectors:
        raise SystemExit("Pass --bundle, --model, or --list-bundles")

    inventory = load_inventory()
    missing = [s for s in selectors if s not in inventory]
    if missing:
        raise SystemExit(f"Selectors not found in verified inventory: {missing}")
    items = [make_item(s, inventory[s]) for s in selectors]
    label = args.label or args.bundle or "custom"
    path = write_manifest(items, label, args.dest_root)
    print(f"Wrote {path}")
    print(f"Models: {len(items)}")
    print(f"Total GiB: {sum(i.size_gib for i in items):.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
