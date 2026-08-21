#!/usr/bin/env python3
"""Verify selected high-value local model folders against Hugging Face manifests.

This deliberately avoids hashing every large file. It verifies the practical
integrity signals that are cheap and useful on an SMB model share:
- target metadata exists and has repo_id/category;
- every Hugging Face sibling file exists locally, unless ignored;
- local file sizes match Hugging Face file sizes exactly;
- unexpected local payload files are reported, excluding Hermes metadata.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from huggingface_hub import model_info

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = REPO_ROOT / "config" / "model_taxonomy.yaml"
DEFAULT_AUDIT = REPO_ROOT / "reports" / "model-library-audit-post-cleanup-20260821-133801Z.json"
DEFAULT_REPORT_DIR = REPO_ROOT / "reports"
HERMES_METADATA = "_hermes_model_metadata.json"
IGNORE_SUFFIXES = {".lock", ".metadata"}
IGNORE_NAMES = {HERMES_METADATA}
DEFAULT_REPOS = [
    "sentence-transformers/all-MiniLM-L6-v2",
    "meta-llama/Prompt-Guard-86M",
    "openai/whisper-large-v3-turbo",
    "deepseek-ai/DeepSeek-OCR-2",
    "stabilityai/stable-video-diffusion-img2vid-xt-1-1",
    "openai/gpt-oss-20b",
    "moonshotai/Kimi-K3",
]


@dataclass
class IntegrityResult:
    repo_id: str
    path: str
    status: str
    hf_file_count: int | None
    matched_files: int
    missing_files: list[str]
    size_mismatches: list[dict[str, Any]]
    extra_payload_files: list[str]
    notes: list[str]


def load_config() -> dict[str, Any]:
    return yaml.safe_load(DEFAULT_CONFIG.read_text(encoding="utf-8"))


def load_inventory(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def payload_files(root: Path) -> dict[str, int]:
    files: dict[str, int] = {}
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if ".cache" in rel.parts:
            continue
        if rel.name in IGNORE_NAMES:
            continue
        if rel.suffix in IGNORE_SUFFIXES:
            continue
        try:
            files[str(rel)] = p.stat().st_size
        except OSError:
            continue
    return files


def verify_one(row: dict[str, Any]) -> IntegrityResult:
    repo_id = row["repo_id"]
    path = Path(row["path"])
    notes: list[str] = []
    if not (path / HERMES_METADATA).exists():
        return IntegrityResult(repo_id, str(path), "missing_metadata", None, 0, [], [], [], notes)
    local = payload_files(path)
    try:
        info = model_info(repo_id, files_metadata=True)
    except Exception as exc:  # noqa: BLE001 - report exact API problem
        return IntegrityResult(repo_id, str(path), f"hf_error:{type(exc).__name__}", None, 0, [], [], [], [str(exc)])
    siblings = getattr(info, "siblings", None) or []
    hf_files: dict[str, int] = {}
    unknown_size: list[str] = []
    for s in siblings:
        name = getattr(s, "rfilename", None)
        if not name or name in IGNORE_NAMES:
            continue
        size = getattr(s, "size", None)
        if size is None:
            unknown_size.append(name)
            continue
        hf_files[name] = int(size)
    if unknown_size:
        notes.append(f"hf_unknown_size_count={len(unknown_size)}")

    missing = sorted([name for name in hf_files if name not in local])
    mismatches = []
    matched = 0
    for name, hf_size in hf_files.items():
        if name not in local:
            continue
        if local[name] != hf_size:
            mismatches.append({"file": name, "local": local[name], "hf": hf_size})
        else:
            matched += 1
    extra = sorted([name for name in local if name not in hf_files])
    status = "ok" if not missing and not mismatches else "issues"
    # Selected GGUF/curated folders are intentionally partial local selections.
    metadata = json.loads((path / HERMES_METADATA).read_text(encoding="utf-8"))
    if metadata.get("selected_file") and metadata["selected_file"] in local:
        status = "selected_file_ok" if local[metadata["selected_file"]] > 0 else "selected_file_empty"
        notes.append("curated_selected_file; full HF manifest not expected to match")
    return IntegrityResult(repo_id, str(path), status, len(hf_files), matched, missing[:50], mismatches[:50], extra[:50], notes)


def write_reports(results: list[IntegrityResult], report_dir: Path, label: str) -> tuple[Path, Path]:
    report_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    json_path = report_dir / f"model-integrity-{label}-{stamp}.json"
    md_path = report_dir / f"model-integrity-{label}-{stamp}.md"
    json_path.write_text(json.dumps([asdict(r) for r in results], indent=2), encoding="utf-8")
    issue_results = [r for r in results if r.status not in {"ok", "selected_file_ok"}]
    lines = [
        f"# Model Integrity Check ({label})",
        "",
        f"Generated: {stamp}",
        "",
        f"- Checked models: `{len(results)}`",
        f"- Issues: `{len(issue_results)}`",
        "",
    ]
    for r in results:
        lines += [
            f"## `{r.repo_id}`",
            f"- Status: `{r.status}`",
            f"- Path: `{r.path}`",
            f"- HF files: `{r.hf_file_count}`; matched files: `{r.matched_files}`",
            f"- Missing files: `{len(r.missing_files)}`",
            f"- Size mismatches: `{len(r.size_mismatches)}`",
            f"- Extra local payload files: `{len(r.extra_payload_files)}`",
        ]
        if r.notes:
            lines.append(f"- Notes: `{'; '.join(r.notes)}`")
        if r.missing_files[:10]:
            lines.append("- Missing sample: " + ", ".join(f"`{x}`" for x in r.missing_files[:10]))
        if r.size_mismatches[:5]:
            lines.append("- Mismatch sample: " + json.dumps(r.size_mismatches[:5]))
        lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", type=Path, default=DEFAULT_AUDIT)
    parser.add_argument("--repo", action="append", help="Repo ID to check; repeatable. Defaults to curated high-value set.")
    parser.add_argument("--label", default="high-value")
    parser.add_argument("--report-dir", type=Path, default=DEFAULT_REPORT_DIR)
    args = parser.parse_args()
    wanted = set(args.repo or DEFAULT_REPOS)
    inventory = load_inventory(args.audit)
    by_repo = {row.get("repo_id"): row for row in inventory if row.get("repo_id")}
    missing_inventory = sorted(wanted - set(by_repo))
    if missing_inventory:
        raise SystemExit(f"Repos not found in inventory: {missing_inventory}")
    results = []
    for repo_id in sorted(wanted):
        print(f"Verifying {repo_id}", flush=True)
        results.append(verify_one(by_repo[repo_id]))
    json_path, md_path = write_reports(results, args.report_dir, args.label)
    issues = [r for r in results if r.status not in {"ok", "selected_file_ok"}]
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    print(f"Checked models: {len(results)}")
    print(f"Issues: {len(issues)}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
