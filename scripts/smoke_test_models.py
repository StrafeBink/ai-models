#!/usr/bin/env python3
"""Light functional smoke tests for representative local models.

These tests avoid loading huge tensors into memory. They check that representative
model artifacts are present and structurally readable: JSON configs/tokenizers,
GGUF magic headers, and safetensors headers.
"""
from __future__ import annotations

import argparse
import json
import struct
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT_DIR = REPO_ROOT / "reports"
ROOT = Path("/Users/davideddy/mnt/models")


@dataclass
class SmokeResult:
    name: str
    path: str
    status: str
    checks: list[str]
    errors: list[str]


def read_json(path: Path) -> dict | list:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def check_exists(path: Path, checks: list[str]) -> None:
    if not path.exists():
        raise AssertionError(f"missing: {path}")
    checks.append(f"exists:{path.name}")


def check_json(path: Path, checks: list[str], required_keys: list[str] | None = None) -> None:
    check_exists(path, checks)
    data = read_json(path)
    if required_keys and isinstance(data, dict):
        missing = [k for k in required_keys if k not in data]
        if missing:
            raise AssertionError(f"{path} missing keys {missing}")
    checks.append(f"json_ok:{path.name}")


def check_safetensors(path: Path, checks: list[str]) -> None:
    check_exists(path, checks)
    with path.open("rb") as f:
        header_len = struct.unpack("<Q", f.read(8))[0]
        if header_len <= 2 or header_len > 100_000_000:
            raise AssertionError(f"invalid safetensors header length {header_len}: {path}")
        header = json.loads(f.read(header_len).decode("utf-8"))
    tensors = [k for k in header if k != "__metadata__"]
    if not tensors:
        raise AssertionError(f"no tensors in safetensors header: {path}")
    checks.append(f"safetensors_header_ok:{path.name}:tensors={len(tensors)}")


def check_gguf(path: Path, checks: list[str]) -> None:
    check_exists(path, checks)
    with path.open("rb") as f:
        magic = f.read(4)
    if magic != b"GGUF":
        raise AssertionError(f"bad GGUF magic {magic!r}: {path}")
    checks.append(f"gguf_magic_ok:{path.name}")


def smoke_embedding_minilm(checks: list[str]) -> None:
    p = ROOT / "Embeddings" / "all-MiniLM-L6-v2"
    check_json(p / "config.json", checks, ["model_type"])
    check_json(p / "tokenizer.json", checks)
    check_safetensors(p / "model.safetensors", checks)


def smoke_prompt_guard(checks: list[str]) -> None:
    p = ROOT / "Safety-Moderation" / "Prompt-Guard-86M"
    check_json(p / "config.json", checks, ["id2label", "model_type"])
    check_json(p / "tokenizer.json", checks)
    check_safetensors(p / "model.safetensors", checks)


def smoke_whisper_turbo(checks: list[str]) -> None:
    p = ROOT / "Speech-STT" / "whisper-large-v3-turbo"
    check_json(p / "config.json", checks, ["model_type"])
    check_json(p / "preprocessor_config.json", checks)
    check_safetensors(p / "model.safetensors", checks)


def smoke_gguf_llm(checks: list[str]) -> None:
    p = ROOT / "LLM" / "Qwen3-32B-Q5_K_M"
    check_gguf(p / "Qwen3-32B-Q5_K_M.gguf", checks)


def smoke_gguf_coding(checks: list[str]) -> None:
    p = ROOT / "Coding" / "Qwen3-Coder-30B-A3B-UD-Q4_K_XL"
    check_gguf(p / "Qwen3-Coder-30B-A3B-Instruct-UD-Q4_K_XL.gguf", checks)


def smoke_deepseek_ocr(checks: list[str]) -> None:
    p = ROOT / "Vision-OCR" / "DeepSeek-OCR-2"
    check_json(p / "config.json", checks, ["model_type"])
    check_json(p / "processor_config.json", checks)
    check_safetensors(p / "model-00001-of-000001.safetensors", checks)


def smoke_stable_video(checks: list[str]) -> None:
    p = ROOT / "Video" / "stable-video-diffusion-img2vid-xt-1-1"
    check_json(p / "model_index.json", checks)
    check_json(p / "scheduler" / "scheduler_config.json", checks)
    check_safetensors(p / "svd_xt_1_1.safetensors", checks)


TESTS: dict[str, tuple[Path, Callable[[list[str]], None]]] = {
    "embedding_minilm_l6": (ROOT / "Embeddings" / "all-MiniLM-L6-v2", smoke_embedding_minilm),
    "prompt_guard": (ROOT / "Safety-Moderation" / "Prompt-Guard-86M", smoke_prompt_guard),
    "whisper_large_v3_turbo": (ROOT / "Speech-STT" / "whisper-large-v3-turbo", smoke_whisper_turbo),
    "gguf_llm_qwen3_32b": (ROOT / "LLM" / "Qwen3-32B-Q5_K_M", smoke_gguf_llm),
    "gguf_coding_qwen3_coder": (ROOT / "Coding" / "Qwen3-Coder-30B-A3B-UD-Q4_K_XL", smoke_gguf_coding),
    "deepseek_ocr": (ROOT / "Vision-OCR" / "DeepSeek-OCR-2", smoke_deepseek_ocr),
    "stable_video_diffusion": (ROOT / "Video" / "stable-video-diffusion-img2vid-xt-1-1", smoke_stable_video),
}


def write_reports(results: list[SmokeResult], report_dir: Path, label: str) -> tuple[Path, Path]:
    report_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    json_path = report_dir / f"model-smoke-tests-{label}-{stamp}.json"
    md_path = report_dir / f"model-smoke-tests-{label}-{stamp}.md"
    json_path.write_text(json.dumps([asdict(r) for r in results], indent=2), encoding="utf-8")
    failures = [r for r in results if r.status != "ok"]
    lines = [
        f"# Model Smoke Tests ({label})",
        "",
        f"Generated: {stamp}",
        "",
        f"- Tests: `{len(results)}`",
        f"- Failures: `{len(failures)}`",
        "",
    ]
    for r in results:
        lines += [
            f"## `{r.name}`",
            f"- Status: `{r.status}`",
            f"- Path: `{r.path}`",
            f"- Checks: `{'; '.join(r.checks)}`",
        ]
        if r.errors:
            lines.append(f"- Errors: `{'; '.join(r.errors)}`")
        lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--label", default="representative")
    parser.add_argument("--report-dir", type=Path, default=DEFAULT_REPORT_DIR)
    args = parser.parse_args()
    results: list[SmokeResult] = []
    for name, (path, func) in TESTS.items():
        checks: list[str] = []
        errors: list[str] = []
        print(f"Smoke testing {name}", flush=True)
        try:
            func(checks)
            status = "ok"
        except Exception as exc:  # noqa: BLE001 - capture smoke failure
            status = "failed"
            errors.append(f"{type(exc).__name__}: {exc}")
        results.append(SmokeResult(name, str(path), status, checks, errors))
    json_path, md_path = write_reports(results, args.report_dir, args.label)
    failures = [r for r in results if r.status != "ok"]
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    print(f"Tests: {len(results)}")
    print(f"Failures: {len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
