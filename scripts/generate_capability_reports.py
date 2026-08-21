#!/usr/bin/env python3
"""Generate human decision reports for the local model library.

Outputs:
- reports/model-capability-index.md
- reports/model-storage-dashboard.md
- reports/model-replacement-review.md
- docs/LOCAL_SERVING_MAP.md
- reports/runtime-smoke-test-readiness.md
"""
from __future__ import annotations

import json
import shutil
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
    runtime: str
    runnable_status: str
    keep_status: str
    notes: str


def load_models() -> list[dict[str, Any]]:
    rows = json.loads(AUDIT.read_text(encoding="utf-8"))
    return [r for r in rows if r.get("scope") != "workflow"]


def location(row: dict[str, Any]) -> str:
    if row.get("scope") == "archive":
        return f"Archive-Huge/{row.get('archive_family')}"
    return str(row.get("category"))


def has_command(name: str) -> bool:
    return shutil.which(name) is not None


def classify(row: dict[str, Any]) -> ModelCard:
    loc = location(row)
    folder = row["folder_name"]
    repo = row.get("repo_id") or "unknown"
    size = float(row.get("size_gib") or 0)
    scope = row.get("scope") or "active"
    lower = f"{loc} {folder} {repo}".lower()

    capability = "General model"
    use = "Review before use"
    runtime = "Unknown / inspect model card"
    runnable = "unknown"
    keep = "review"
    notes = "Needs capability benchmark before operational use."

    if scope == "archive":
        runnable = "archive_only"
        keep = "strategic_archive"
        notes = "Stored for strategic/future-hardware value rather than current day-to-day use."

    if "embedding" in lower or "minilm" in lower or "mpnet" in lower:
        capability = "Embeddings / retrieval"
        use = "Semantic search, RAG retrieval, clustering, similarity."
        runtime = "sentence-transformers or transformers; GGUF embedding runtime for GGUF quants."
        runnable = "runnable_with_runtime_install" if scope != "archive" else runnable
        keep = "active" if scope != "archive" else keep
        notes = "Benchmark retrieval quality and latency before choosing default RAG embedding."
    elif "prompt-guard" in lower:
        capability = "Prompt safety / moderation"
        use = "Prompt-injection and jailbreak risk classifier for agents/RAG."
        runtime = "transformers sequence-classification."
        runnable = "runnable_with_runtime_install"
        keep = "active"
        notes = "Good candidate for default safety guardrail once transformers/torch runtime is installed."
    elif "whisper" in lower or "asr" in lower:
        capability = "Speech-to-text"
        use = "Transcription and speech recognition."
        runtime = "faster-whisper preferred; transformers fallback."
        runnable = "runnable_with_runtime_install"
        keep = "active" if "v3" in lower or "nemotron" in lower else "review_after_benchmark"
        notes = "Keep v2 only if benchmark shows accuracy/use-case value over v3/v3-turbo."
    elif "ocr" in lower:
        capability = "OCR / document extraction"
        use = "Image/PDF text extraction and document understanding."
        runtime = "transformers/custom model code, likely GPU/accelerator dependent."
        runnable = "runnable_with_runtime_install"
        keep = "active"
        notes = "Needs a known sample-image benchmark."
    elif any(x in lower for x in ["flux", "stable-diffusion"]):
        capability = "Image generation/editing"
        use = "Text-to-image, image editing, diffusion workflows."
        runtime = "ComfyUI or diffusers."
        runnable = "runnable_with_runtime_install"
        keep = "active"
        notes = "Use ComfyUI/diffusers smoke workflow to confirm exact pipeline support."
    elif "stable-video" in lower:
        capability = "Video generation"
        use = "Image-to-video generation."
        runtime = "ComfyUI or diffusers Stable Video pipeline."
        runnable = "runnable_with_runtime_install"
        keep = "active"
        notes = "Verified structurally; runtime test needs diffusion stack."
    elif "audio" in lower or "personaplex" in lower:
        capability = "Audio generation / audio model"
        use = "Audio/music/SFX generation or audio-specific workflows."
        runtime = "Model-specific audio/diffusers stack."
        runnable = "runnable_with_runtime_install"
        keep = "active"
        notes = "Needs model-specific generation smoke test."
    elif "coder" in lower or loc.endswith("Coding"):
        capability = "Coding LLM"
        use = "Local coding assistant, code generation, code review."
        runtime = "llama.cpp for GGUF; transformers/vLLM for safetensors archive."
        runnable = "runnable_with_runtime_install" if scope != "archive" else runnable
        keep = "active" if scope != "archive" else keep
        notes = "GGUF quants are the most likely current runnable path."
    elif any(x in lower for x in ["qwen", "llama", "gemma", "glm", "gpt-oss", "deepseek", "ministral", "kimi"]):
        capability = "LLM / reasoning-chat"
        use = "Local chat, reasoning, drafting, agent backend."
        runtime = "llama.cpp for GGUF; transformers/vLLM for safetensors archives."
        runnable = "runnable_with_runtime_install" if scope != "archive" else runnable
        keep = "active" if scope != "archive" else keep
        notes = "Benchmark tokens/sec and answer quality before choosing default."
    elif "vl" in lower or "multimodal" in lower or "agentworld" in lower:
        capability = "Multimodal / vision-language"
        use = "Vision-language reasoning, image understanding, multimodal agents."
        runtime = "transformers/vLLM/custom multimodal runtime."
        runnable = "archive_only" if scope == "archive" else "runnable_with_runtime_install"
        keep = keep if scope == "archive" else "active"
        notes = "Requires multimodal runtime compatibility test."

    if size > 120 and scope != "archive":
        notes += " Large active model; confirm storage/runtime value periodically."
    return ModelCard(loc, folder, repo, size, int(row.get("payload_file_count") or 0), scope, capability, use, runtime, runnable, keep, notes)


def write_capability_index(cards: list[ModelCard]) -> None:
    out = REPORTS / "model-capability-index.md"
    lines = [
        "# Model Capability Index",
        "",
        "Generated from the latest clean local-library audit. This is a human decision layer over the verified model folders.",
        "",
        "## Status meanings",
        "",
        "| Status | Meaning |",
        "|---|---|",
        "| `runnable_with_runtime_install` | Files are present; install/use the named runtime stack before running. |",
        "| `archive_only` | Strategic/future-hardware store, not expected to run today. |",
        "| `unknown` | Needs manual runtime/capability review. |",
        "",
        "## Capability cards",
        "",
        "| Location | Model | Capability | Runnable status | Keep status | Runtime | Size | Use |",
        "|---|---|---|---|---|---|---:|---|",
    ]
    for c in sorted(cards, key=lambda x: (x.location, x.folder.lower())):
        lines.append(f"| {c.location} | `{c.folder}` | {c.capability} | `{c.runnable_status}` | `{c.keep_status}` | {c.runtime} | {c.size_gib:.2f} GiB | {c.recommended_use} |")
    lines += ["", "## Notes by model", ""]
    for c in sorted(cards, key=lambda x: (x.location, x.folder.lower())):
        lines += [
            f"### `{c.folder}`",
            "",
            f"- Repo: `{c.repo_id}`",
            f"- Location: `{c.location}`",
            f"- Capability: {c.capability}",
            f"- Runtime: {c.runtime}",
            f"- Runnable status: `{c.runnable_status}`",
            f"- Keep status: `{c.keep_status}`",
            f"- Size: `{c.size_gib:.2f} GiB`; payload files: `{c.payload_files}`",
            f"- Recommended use: {c.recommended_use}",
            f"- Notes: {c.notes}",
            "",
        ]
    out.write_text("\n".join(lines), encoding="utf-8")


def write_storage_dashboard(cards: list[ModelCard]) -> None:
    out = REPORTS / "model-storage-dashboard.md"
    total = sum(c.size_gib for c in cards)
    by_loc: dict[str, float] = defaultdict(float)
    by_cap: dict[str, float] = defaultdict(float)
    for c in cards:
        by_loc[c.location] += c.size_gib
        by_cap[c.capability] += c.size_gib
    lines = [
        "# Model Storage Dashboard",
        "",
        f"- Total downloaded model folders: `{len(cards)}`",
        f"- Total measured size: `{total:.2f} GiB` (`{total/1024:.2f} TiB`)",
        "",
        "## Size by location",
        "",
        "| Location | Size | Share |",
        "|---|---:|---:|",
    ]
    for loc, size in sorted(by_loc.items(), key=lambda kv: kv[1], reverse=True):
        lines.append(f"| {loc} | {size:.2f} GiB | {size/total*100:.1f}% |")
    lines += ["", "## Size by capability", "", "| Capability | Size | Share |", "|---|---:|---:|"]
    for cap, size in sorted(by_cap.items(), key=lambda kv: kv[1], reverse=True):
        lines.append(f"| {cap} | {size:.2f} GiB | {size/total*100:.1f}% |")
    lines += ["", "## Top 15 largest folders", "", "| Rank | Model | Location | Size | Keep status |", "|---:|---|---|---:|---|"]
    for i, c in enumerate(sorted(cards, key=lambda x: x.size_gib, reverse=True)[:15], 1):
        lines.append(f"| {i} | `{c.folder}` | {c.location} | {c.size_gib:.2f} GiB | `{c.keep_status}` |")
    out.write_text("\n".join(lines), encoding="utf-8")


def write_replacement_review(cards: list[ModelCard]) -> None:
    out = REPORTS / "model-replacement-review.md"
    by_folder = {c.folder: c for c in cards}
    candidates: list[tuple[str, str, str]] = []
    def add(model: str, action: str, rationale: str) -> None:
        if model in by_folder:
            candidates.append((model, action, rationale))
    add("whisper-large-v2", "Benchmark then likely archive", "`whisper-large-v3` and `whisper-large-v3-turbo` are present; keep v2 only if accuracy/regression tests justify it.")
    add("Llama-2-7b-chat-hf", "Archive only", "Older Llama 2 chat model is strategically useful but not a default active local LLM.")
    add("Meta-Llama-3-8B", "Archive only / compare against newer local LLMs", "Newer Qwen/GPT-OSS/Gemma local candidates are present.")
    add("Llama-3.1-8B-Instruct", "Archive only / benchmark if needed", "Useful baseline but likely superseded by newer local active models.")
    add("all-MiniLM-L12-v2", "Benchmark before default use", "`all-MiniLM-L6-v2` is smaller/faster; `all-mpnet-base-v2` may be higher quality.")
    add("paraphrase-multilingual-MiniLM-L12-v2", "Keep only for multilingual benchmark value", "May be superseded by multilingual mpnet or Qwen embedding depending quality/latency.")
    add("stable-diffusion-3-medium", "Review against SD3.5/FLUX", "Newer SD3.5/FLUX families are present; keep if workflow compatibility or speed matters.")
    add("FLUX.1-schnell", "Keep as fast image-generation baseline", "May remain useful despite FLUX.2 presence because it is faster/simpler.")
    add("Kimi-K3", "Strategic archive", "Very large model; keep for future hardware/significance, not current runnable default.")
    lines = [
        "# Model Replacement / Deprecation Review",
        "",
        "No deletion is recommended automatically. This report identifies candidates for benchmark-driven keep/archive/delete decisions.",
        "",
        "## Review candidates",
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
        "- Do not delete a model until a replacement has passed a capability benchmark for the actual use case.",
        "- Prefer archiving over deleting gated or hard-to-redownload models.",
        "- Keep one fast/small baseline per capability even when a larger higher-quality model exists.",
        "- Review `Archive-Huge/` quarterly for storage pressure, not weekly.",
    ]
    out.write_text("\n".join(lines), encoding="utf-8")


def write_serving_map(cards: list[ModelCard]) -> None:
    out = DOCS / "LOCAL_SERVING_MAP.md"
    DOCS.mkdir(exist_ok=True)
    lines = [
        "# Local Serving Map",
        "",
        "Purpose: choose the best local model and runtime path for each capability. This map is operational guidance, not a benchmark result.",
        "",
        "| Capability | First candidate | Alternative(s) | Preferred runtime | Status |",
        "|---|---|---|---|---|",
        "| Chat / reasoning | `GPT-OSS-20B` or `Qwen3-32B-Q5_K_M` | `Gemma-3-27B-QAT-Q4_0`, `GLM-4.7-Flash-Q4_K_M` | llama.cpp for GGUF; transformers/vLLM where supported | Needs runtime benchmark |",
        "| Coding | `Qwen3-Coder-30B-A3B-UD-Q4_K_XL` | `Qwen3-Coder-Next-Q4_K_M` | llama.cpp / GGUF | Needs runtime benchmark |",
        "| Embeddings | `all-MiniLM-L6-v2` for fast baseline | `all-mpnet-base-v2`, `Qwen3-Embedding-8B-Q4_K_M`, `Qwen3-VL-Embedding-8B` | sentence-transformers/transformers; GGUF embedding runtime | Needs retrieval benchmark |",
        "| Prompt safety | `Prompt-Guard-86M` | none currently | transformers sequence classification | Ready after runtime install |",
        "| Speech-to-text | `whisper-large-v3-turbo` | `whisper-large-v3`, `nemotron-3.5-asr-streaming-0.6b` | faster-whisper preferred; transformers fallback | Needs audio sample benchmark |",
        "| OCR | `DeepSeek-OCR-2` | none currently | transformers/custom model code | Needs sample image benchmark |",
        "| Image generation/editing | `FLUX.2-dev`, `FLUX.2-klein-9B`, `stable-diffusion-3.5-large` | FLUX.1 family | ComfyUI or diffusers | Needs pipeline benchmark |",
        "| Video generation | `stable-video-diffusion-img2vid-xt-1-1` | none currently | ComfyUI or diffusers | Structurally verified |",
        "| Audio generation | `stable-audio-open-1.0`, `stable-audio-3-medium`, `stable-audio-3-small-sfx` | `personaplex-7b-v1` | model-specific audio/diffusers stack | Needs generation benchmark |",
        "",
        "## Runtime installation gaps observed",
        "",
        "At the time this map was created, the project venv did not include heavy runtime packages such as `transformers`, `torch`, `sentence_transformers`, `llama_cpp`, `whisper`, or `faster_whisper`. Existing smoke tests therefore validate structure, not full inference.",
        "",
        "## Recommended next runtime setup order",
        "",
        "1. Install/validate `llama.cpp` or `llama-cpp-python` for GGUF LLM/coding tests.",
        "2. Install `sentence-transformers`/`transformers`/`torch` for embeddings and Prompt Guard.",
        "3. Install `faster-whisper` for STT testing.",
        "4. Add ComfyUI or diffusers runtime validation for image/video/audio models.",
    ]
    out.write_text("\n".join(lines), encoding="utf-8")


def write_runtime_readiness() -> None:
    out = REPORTS / "runtime-smoke-test-readiness.md"
    deps = {
        "llama.cpp CLI (`llama-cli` or `main`)": has_command("llama-cli") or has_command("main"),
        "ollama CLI": has_command("ollama"),
        "comfy CLI": has_command("comfy"),
    }
    lines = [
        "# Runtime Smoke Test Readiness",
        "",
        "The current repository smoke tests are structural. Full inference tests require runtime packages/tools.",
        "",
        "## CLI/runtime availability",
        "",
        "| Runtime | Available |",
        "|---|---:|",
    ]
    for dep, ok in deps.items():
        lines.append(f"| {dep} | {'✅' if ok else '❌'} |")
    lines += [
        "",
        "## Proposed full runtime tests",
        "",
        "| Capability | Test | Dependency |",
        "|---|---|---|",
        "| Embeddings | Embed five sentences and check cosine similarity ordering | `sentence-transformers`, `torch` |",
        "| Prompt Guard | Classify benign, injection, and jailbreak prompts | `transformers`, `torch` |",
        "| Whisper | Transcribe a short known audio sample | `faster-whisper` or `transformers`, `torch` |",
        "| GGUF LLM | Generate a 20-token response and record tokens/sec | `llama.cpp` or `llama-cpp-python` |",
        "| OCR | Extract text from a known sample image | `transformers`, `torch`, model custom code |",
        "| Diffusion/video/audio | Generate a tiny/sample output | ComfyUI or diffusers stack |",
        "",
        "## Recommendation",
        "",
        "Install runtime stacks deliberately, one family at a time, so the project can record exact working commands and avoid turning the manager venv into an unstable heavy ML environment.",
    ]
    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    cards = [classify(r) for r in load_models()]
    write_capability_index(cards)
    write_storage_dashboard(cards)
    write_replacement_review(cards)
    write_serving_map(cards)
    write_runtime_readiness()
    print("Wrote reports/model-capability-index.md")
    print("Wrote reports/model-storage-dashboard.md")
    print("Wrote reports/model-replacement-review.md")
    print("Wrote docs/LOCAL_SERVING_MAP.md")
    print("Wrote reports/runtime-smoke-test-readiness.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
