#!/usr/bin/env python3
"""Generate AI-box transfer and decision reports for the model file-server library.

This Mac/repo is the verified model library and file server. The AI box is the
execution host. These reports therefore focus on curation, transfer priority,
AI-box runtime hints, storage, and benchmark-before-delete decisions rather
than installing inference runtimes on the file server.

Outputs committed under docs/:
- MODEL_CAPABILITY_INDEX.md
- AI_BOX_TRANSFER_PRIORITY.md
- MODEL_STORAGE_DASHBOARD.md
- MODEL_REPLACEMENT_REVIEW.md
- AI_BOX_SERVING_MAP.md
- AI_BOX_HANDOFF_GUIDE.md
"""
from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT = REPO_ROOT / "reports" / "model-library-audit-post-cleanup-20260821-133801Z.json"
REPORTS = REPO_ROOT / "reports"
DOCS = REPO_ROOT / "docs"


@dataclass
class ModelCard:
    location: str
    folder: str
    repo_id: str
    size_gib: float
    payload_files: int
    scope: str
    capability: str
    recommended_use: str
    ai_box_runtime: str
    transfer_priority: str
    library_status: str
    keep_status: str
    notes: str


def load_models() -> list[dict[str, Any]]:
    rows = json.loads(AUDIT.read_text(encoding="utf-8"))
    return [r for r in rows if r.get("scope") != "workflow"]


def location(row: dict[str, Any]) -> str:
    if row.get("scope") == "archive":
        return f"Archive-Huge/{row.get('archive_family')}"
    return str(row.get("category"))


def classify(row: dict[str, Any]) -> ModelCard:
    loc = location(row)
    folder = row["folder_name"]
    repo = row.get("repo_id") or "unknown"
    size = float(row.get("size_gib") or 0)
    scope = row.get("scope") or "active"
    lower = f"{loc} {folder} {repo}".lower()

    capability = "General model"
    use = "Review before moving to AI box."
    runtime = "Unknown; inspect upstream model card."
    priority = "review"
    library_status = "verified_file_server_copy"
    keep = "review"
    notes = "Files are verified in the library; AI-box run suitability needs review."

    if scope == "archive":
        priority = "archive_only"
        keep = "strategic_archive"
        notes = "Strategic archive/future-hardware store. Do not transfer routinely unless specifically needed."

    if "embedding" in lower or "minilm" in lower or "mpnet" in lower:
        capability = "Embeddings / retrieval"
        use = "Move to AI box for semantic search, RAG retrieval, clustering, similarity."
        runtime = "sentence-transformers/transformers on AI box; GGUF embedding runtime for GGUF quants."
        priority = "high" if scope != "archive" and ("all-minilm-l6" in lower or "mpnet" in lower) else ("medium" if scope != "archive" else priority)
        keep = "active" if scope != "archive" else keep
        notes = "Copy small baseline first; benchmark retrieval quality before choosing the default embedding model."
    elif "prompt-guard" in lower:
        capability = "Prompt safety / moderation"
        use = "Move to AI box for prompt-injection and jailbreak checks in agents/RAG."
        runtime = "transformers sequence-classification on AI box."
        priority = "high"
        keep = "active"
        notes = "Strong default safety guardrail candidate; small transfer."
    elif "whisper" in lower or "asr" in lower:
        capability = "Speech-to-text"
        use = "Move to AI box for transcription/STT testing."
        runtime = "faster-whisper preferred; transformers fallback on AI box."
        priority = "high" if "v3-turbo" in lower else "medium"
        keep = "active" if "v3" in lower or "nemotron" in lower else "review_after_benchmark"
        notes = "Transfer v3-turbo first; keep v2 only if AI-box accuracy tests justify it."
    elif "ocr" in lower:
        capability = "OCR / document extraction"
        use = "Move to AI box for image/PDF text extraction experiments."
        runtime = "transformers/custom model code on AI box."
        priority = "medium"
        keep = "active"
        notes = "Needs sample-image benchmark on the AI box."
    elif "stable-video" in lower:
        capability = "Video generation"
        use = "Move to AI box for image-to-video generation workflows."
        runtime = "ComfyUI or diffusers Stable Video pipeline on AI box."
        priority = "medium"
        keep = "active"
        notes = "Structurally verified; transfer only when video pipeline testing is planned."
    elif any(x in lower for x in ["flux", "stable-diffusion"]):
        capability = "Image generation/editing"
        use = "Move to AI box for ComfyUI/diffusers image generation and editing."
        runtime = "ComfyUI or diffusers on AI box."
        priority = "high" if any(x in lower for x in ["flux.2-klein", "flux.1-schnell"]) else "medium"
        keep = "active"
        notes = "Transfer smaller/fast variants before huge full models unless a workflow needs them."
    elif "audio" in lower or "personaplex" in lower:
        capability = "Audio generation / audio model"
        use = "Move to AI box for audio/music/SFX model-specific workflows."
        runtime = "Model-specific audio/diffusers stack on AI box."
        priority = "medium"
        keep = "active"
        notes = "Needs model-specific AI-box generation smoke test."
    elif "coder" in lower or loc.endswith("Coding"):
        capability = "Coding LLM"
        use = "Move to AI box for local coding assistant/code generation tests."
        runtime = "llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archive."
        priority = "high" if scope != "archive" else priority
        keep = "active" if scope != "archive" else keep
        notes = "GGUF quants are likely the most useful current AI-box transfer candidates."
    elif "vl" in lower or "multimodal" in lower or "agentworld" in lower:
        capability = "Multimodal / vision-language"
        use = "Move to AI box for image-understanding/multimodal agent tests."
        runtime = "transformers/vLLM/custom multimodal runtime on AI box."
        priority = "medium" if scope != "archive" else priority
        keep = keep if scope == "archive" else "active"
        notes = "Requires AI-box multimodal runtime compatibility test."
    elif any(x in lower for x in ["qwen", "llama", "gemma", "glm", "gpt-oss", "deepseek", "ministral", "kimi"]):
        capability = "LLM / reasoning-chat"
        use = "Move to AI box for chat, reasoning, drafting, and agent-backend trials."
        runtime = "llama.cpp/GGUF on AI box for quant folders; transformers/vLLM for safetensors archives."
        priority = "high" if scope != "archive" and any(x in lower for x in ["q5_k_m", "q4_k_m", "gpt-oss", "nvfp4"]) else ("medium" if scope != "archive" else priority)
        keep = "active" if scope != "archive" else keep
        notes = "Benchmark tokens/sec and answer quality on the AI box before setting defaults."

    if size > 120 and scope != "archive":
        priority = "medium"
        notes += " Large active transfer; copy only when a specific AI-box test is planned."

    if scope == "archive":
        priority = "archive_only"
        keep = "strategic_archive"
        notes = "Strategic archive/future-hardware store. Keep on file server; transfer only for a specific AI-box comparison or future-hardware test. " + notes

    return ModelCard(
        loc,
        folder,
        repo,
        size,
        int(row.get("payload_file_count") or 0),
        scope,
        capability,
        use,
        runtime,
        priority,
        library_status,
        keep,
        notes,
    )


def write_both(name: str, text: str) -> None:
    REPORTS.mkdir(exist_ok=True)
    DOCS.mkdir(exist_ok=True)
    (REPORTS / name.lower().replace("_", "-")).write_text(text, encoding="utf-8")
    (DOCS / name).write_text(text, encoding="utf-8")


def write_capability_index(cards: list[ModelCard]) -> None:
    lines = [
        "# Model Capability Index",
        "",
        "This is a decision layer for the model file server. It describes what each verified library folder is for, how valuable it is to transfer to the separate AI box, and what runtime the AI box is likely to need.",
        "",
        "## Status meanings",
        "",
        "| Status | Meaning |",
        "|---|---|",
        "| `verified_file_server_copy` | The model folder is present, named, categorized, metadata-complete, and structurally verified on the file server. |",
        "| `high` | Strong candidate to copy to the AI box soon. |",
        "| `medium` | Useful, but copy when a specific test/workflow needs it. |",
        "| `archive_only` | Keep on file server; do not routinely transfer to AI box. |",
        "| `review` | Needs manual purpose/runtime review first. |",
        "",
        "## Capability cards",
        "",
        "| Location | Model | Capability | Transfer priority | Keep status | AI-box runtime | Size | Use |",
        "|---|---|---|---|---|---|---:|---|",
    ]
    for c in sorted(cards, key=lambda x: (x.location, x.folder.lower())):
        lines.append(f"| {c.location} | `{c.folder}` | {c.capability} | `{c.transfer_priority}` | `{c.keep_status}` | {c.ai_box_runtime} | {c.size_gib:.2f} GiB | {c.recommended_use} |")
    lines += ["", "## Notes by model", ""]
    for c in sorted(cards, key=lambda x: (x.location, x.folder.lower())):
        lines += [
            f"### `{c.folder}`",
            "",
            f"- Repo: `{c.repo_id}`",
            f"- Location: `{c.location}`",
            f"- Capability: {c.capability}",
            f"- Library status: `{c.library_status}`",
            f"- Transfer priority: `{c.transfer_priority}`",
            f"- Keep status: `{c.keep_status}`",
            f"- AI-box runtime: {c.ai_box_runtime}",
            f"- Size: `{c.size_gib:.2f} GiB`; payload files: `{c.payload_files}`",
            f"- Recommended use: {c.recommended_use}",
            f"- Notes: {c.notes}",
            "",
        ]
    write_both("MODEL_CAPABILITY_INDEX.md", "\n".join(lines))


def write_transfer_priority(cards: list[ModelCard]) -> None:
    lines = [
        "# AI Box Transfer Priority",
        "",
        "Use this when deciding what to manually copy from the file-server library to the AI box.",
        "",
    ]
    for priority in ["high", "medium", "review", "archive_only"]:
        subset = sorted([c for c in cards if c.transfer_priority == priority], key=lambda x: (x.size_gib, x.folder.lower()))
        lines += [f"## `{priority}`", "", "| Model | Capability | Size | AI-box runtime | Why copy / why keep |", "|---|---|---:|---|---|"]
        for c in subset:
            lines.append(f"| `{c.folder}` | {c.capability} | {c.size_gib:.2f} GiB | {c.ai_box_runtime} | {c.notes} |")
        lines.append("")
    write_both("AI_BOX_TRANSFER_PRIORITY.md", "\n".join(lines))


def write_storage_dashboard(cards: list[ModelCard]) -> None:
    total = sum(c.size_gib for c in cards)
    by_loc: dict[str, float] = defaultdict(float)
    by_cap: dict[str, float] = defaultdict(float)
    by_priority: dict[str, float] = defaultdict(float)
    for c in cards:
        by_loc[c.location] += c.size_gib
        by_cap[c.capability] += c.size_gib
        by_priority[c.transfer_priority] += c.size_gib
    lines = [
        "# Model Storage Dashboard",
        "",
        f"- Total downloaded model folders: `{len(cards)}`",
        f"- Total measured size: `{total:.2f} GiB` (`{total/1024:.2f} TiB`)",
        "- Role: file-server storage for models that are manually copied to the AI box as needed.",
        "",
        "## Size by transfer priority",
        "",
        "| Transfer priority | Size | Share |",
        "|---|---:|---:|",
    ]
    for key in ["high", "medium", "review", "archive_only"]:
        size = by_priority.get(key, 0)
        lines.append(f"| `{key}` | {size:.2f} GiB | {size/total*100:.1f}% |")
    lines += ["", "## Size by location", "", "| Location | Size | Share |", "|---|---:|---:|"]
    for loc, size in sorted(by_loc.items(), key=lambda kv: kv[1], reverse=True):
        lines.append(f"| {loc} | {size:.2f} GiB | {size/total*100:.1f}% |")
    lines += ["", "## Size by capability", "", "| Capability | Size | Share |", "|---|---:|---:|"]
    for cap, size in sorted(by_cap.items(), key=lambda kv: kv[1], reverse=True):
        lines.append(f"| {cap} | {size:.2f} GiB | {size/total*100:.1f}% |")
    lines += ["", "## Top 15 largest folders", "", "| Rank | Model | Location | Size | Transfer priority |", "|---:|---|---|---:|---|"]
    for i, c in enumerate(sorted(cards, key=lambda x: x.size_gib, reverse=True)[:15], 1):
        lines.append(f"| {i} | `{c.folder}` | {c.location} | {c.size_gib:.2f} GiB | `{c.transfer_priority}` |")
    write_both("MODEL_STORAGE_DASHBOARD.md", "\n".join(lines))


def write_replacement_review(cards: list[ModelCard]) -> None:
    by_folder = {c.folder: c for c in cards}
    candidates: list[tuple[str, str, str]] = []

    def add(model: str, action: str, rationale: str) -> None:
        if model in by_folder:
            candidates.append((model, action, rationale))

    add("whisper-large-v2", "Copy only for comparison; likely archive", "`whisper-large-v3` and `whisper-large-v3-turbo` are present; keep v2 only if AI-box accuracy tests justify it.")
    add("Llama-2-7b-chat-hf", "Archive only", "Older Llama 2 chat model is strategically useful but not a default AI-box transfer candidate.")
    add("Meta-Llama-3-8B", "Archive / compare only if needed", "Newer Qwen/GPT-OSS/Gemma local candidates are present.")
    add("Llama-3.1-8B-Instruct", "Archive / compare only if needed", "Useful baseline but likely superseded by newer active AI-box candidates.")
    add("all-MiniLM-L12-v2", "Benchmark before copying routinely", "`all-MiniLM-L6-v2` is smaller/faster; `all-mpnet-base-v2` may be higher quality.")
    add("paraphrase-multilingual-MiniLM-L12-v2", "Copy only for multilingual benchmark", "May be superseded by multilingual mpnet or Qwen embedding depending AI-box quality/latency.")
    add("stable-diffusion-3-medium", "Review against SD3.5/FLUX", "Newer SD3.5/FLUX families are present; copy only if AI-box workflow compatibility or speed matters.")
    add("FLUX.1-schnell", "Good fast baseline transfer", "May remain useful despite FLUX.2 because it is faster/simpler.")
    add("Kimi-K3", "Strategic archive", "Very large model; keep on file server for future hardware/significance, not routine transfer.")

    lines = [
        "# Model Replacement / Deprecation Review",
        "",
        "No deletion is recommended automatically. This report identifies benchmark-driven keep/archive/delete decisions for the file-server library and AI-box transfer workflow.",
        "",
        "| Model | Suggested action | Rationale |",
        "|---|---|---|",
    ]
    for model, action, rationale in candidates:
        c = by_folder[model]
        lines.append(f"| `{model}` | {action} | {rationale} Size: `{c.size_gib:.2f} GiB`. |")
    lines += [
        "",
        "## General rules",
        "",
        "- Do not delete a model until a replacement has passed an AI-box benchmark for the actual use case.",
        "- Prefer archiving over deleting gated or hard-to-redownload models.",
        "- Keep one fast/small baseline per capability even when a larger higher-quality model exists.",
        "- Review `Archive-Huge/` quarterly for storage pressure, not weekly.",
    ]
    write_both("MODEL_REPLACEMENT_REVIEW.md", "\n".join(lines))


def write_ai_box_serving_map() -> None:
    lines = [
        "# AI Box Serving Map",
        "",
        "Purpose: choose which verified file-server model to manually copy to the AI box for each capability, and what runtime family the AI box should use.",
        "",
        "| Capability | Copy first | Alternatives | AI-box runtime family | Status |",
        "|---|---|---|---|---|",
        "| Chat / reasoning | `GPT-OSS-20B` or `Qwen3-32B-Q5_K_M` | `Gemma-3-27B-QAT-Q4_0`, `GLM-4.7-Flash-Q4_K_M`, `Qwen3.6-35B-A3B-NVFP4` | llama.cpp/GGUF or compatible LLM runtime | Needs AI-box benchmark |",
        "| Coding | `Qwen3-Coder-30B-A3B-UD-Q4_K_XL` | `Qwen3-Coder-Next-Q4_K_M` | llama.cpp/GGUF | Needs AI-box benchmark |",
        "| Embeddings | `all-MiniLM-L6-v2` | `all-mpnet-base-v2`, `Qwen3-Embedding-8B-Q4_K_M`, `Qwen3-VL-Embedding-8B` | sentence-transformers/transformers or GGUF embedding runtime | Copy MiniLM first |",
        "| Prompt safety | `Prompt-Guard-86M` | none currently | transformers sequence classification | High-priority small transfer |",
        "| Speech-to-text | `whisper-large-v3-turbo` | `whisper-large-v3`, `nemotron-3.5-asr-streaming-0.6b` | faster-whisper or transformers | Copy turbo first |",
        "| OCR | `DeepSeek-OCR-2` | none currently | transformers/custom model code | Medium priority |",
        "| Image generation/editing | `FLUX.2-klein-9B` or `FLUX.1-schnell` | `FLUX.2-dev`, `stable-diffusion-3.5-large` | ComfyUI or diffusers | Copy smaller/fast model first |",
        "| Video generation | `stable-video-diffusion-img2vid-xt-1-1` | none currently | ComfyUI or diffusers | Transfer only for planned video test |",
        "| Audio generation | `stable-audio-open-1.0`, `stable-audio-3-medium`, `stable-audio-3-small-sfx` | `personaplex-7b-v1` | model-specific audio stack | Transfer only for planned audio test |",
        "",
        "## File-server rule",
        "",
        "Do not install heavy inference stacks into the file-server project venv just to test models. Keep this repo focused on discovery, downloads, metadata, verification, storage dashboards, and AI-box handoff guidance.",
    ]
    (DOCS / "AI_BOX_SERVING_MAP.md").write_text("\n".join(lines), encoding="utf-8")


def write_ai_box_handoff_guide() -> None:
    lines = [
        "# AI Box Handoff Guide",
        "",
        "This repo is the model library/file server. Models are manually copied to the AI box for execution. Use this guide to avoid moving giant folders without purpose.",
        "",
        "## Recommended handoff workflow",
        "",
        "1. Check `docs/AI_BOX_TRANSFER_PRIORITY.md` for copy priority.",
        "2. Check `docs/AI_BOX_SERVING_MAP.md` for the target runtime family.",
        "3. Copy one model family at a time to the AI box.",
        "4. Run a small AI-box benchmark and record the result back in project notes or a future benchmark report.",
        "5. Only then promote a model to default use or mark older models as superseded.",
        "",
        "## Suggested first transfers",
        "",
        "| Purpose | Model | Why |",
        "|---|---|---|",
        "| Fast embeddings baseline | `Embeddings/all-MiniLM-L6-v2` | Small, verified, useful for RAG/search. |",
        "| Prompt safety | `Safety-Moderation/Prompt-Guard-86M` | Small guardrail model for agent/RAG workflows. |",
        "| Coding model | `Coding/Qwen3-Coder-30B-A3B-UD-Q4_K_XL` | Active GGUF coding candidate. |",
        "| Chat/reasoning | `LLM/Qwen3-32B-Q5_K_M` or `LLM/GPT-OSS-20B` | Active local LLM candidates. |",
        "| STT | `Speech-STT/whisper-large-v3-turbo` | Smallest/fastest Whisper candidate. |",
        "| Image generation | `Diffusion-Image/FLUX.2-klein-9B` or `Diffusion-Image/FLUX.1-schnell` | Prefer smaller/faster image models before huge variants. |",
        "",
        "## Avoid routine transfers",
        "",
        "- `Archive-Huge/LLM/Kimi-K3`: strategic archive; huge transfer, future-hardware value.",
        "- Full FLUX/SD large models: transfer only when ComfyUI/diffusers workflow is ready.",
        "- Older Llama archive models: transfer only for comparison/regression tests.",
    ]
    (DOCS / "AI_BOX_HANDOFF_GUIDE.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    cards = [classify(r) for r in load_models()]
    DOCS.mkdir(exist_ok=True)
    write_capability_index(cards)
    write_transfer_priority(cards)
    write_storage_dashboard(cards)
    write_replacement_review(cards)
    write_ai_box_serving_map()
    write_ai_box_handoff_guide()
    for name in [
        "MODEL_CAPABILITY_INDEX.md",
        "AI_BOX_TRANSFER_PRIORITY.md",
        "MODEL_STORAGE_DASHBOARD.md",
        "MODEL_REPLACEMENT_REVIEW.md",
        "AI_BOX_SERVING_MAP.md",
        "AI_BOX_HANDOFF_GUIDE.md",
    ]:
        print(f"Wrote docs/{name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
