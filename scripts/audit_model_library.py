#!/usr/bin/env python3
"""Audit the mounted AI model library for naming, placement, and metadata issues.

This is a structural/inventory audit rather than a full byte-for-byte checksum
of every weight file. It walks model folders, verifies Hermes metadata, checks
category/name placement against the taxonomy, detects duplicate repo IDs and
obvious partial/quarantine folders, and writes JSON/Markdown reports.
"""
from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = REPO_ROOT / "config" / "model_taxonomy.yaml"
DEFAULT_REPORT_DIR = REPO_ROOT / "reports"
METADATA = "_hermes_model_metadata.json"


@dataclass
class ModelAudit:
    path: str
    scope: str
    category: str | None
    archive_family: str | None
    folder_name: str
    status: str
    repo_id: str | None
    metadata_category: str | None
    expected_folder_name: str | None
    expected_path: str | None
    size_gib: float | None
    file_count: int
    payload_file_count: int
    issues: list[str]


def load_config(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def safe_folder_name(repo_id: str) -> str:
    return repo_id.split("/", 1)[-1].replace(" ", "-").replace(":", "-")


def is_mount_like(root: Path) -> bool:
    required = ["LLM", "Archive-Huge", "Embeddings"]
    return root.exists() and all((root / name).is_dir() for name in required)


def iter_model_dirs(root: Path, categories: set[str], archive_families: set[str]) -> list[tuple[Path, str, str | None, str | None]]:
    """Return (path, scope, category, archive_family)."""
    found: list[tuple[Path, str, str | None, str | None]] = []
    for category in sorted(categories):
        cat_dir = root / category
        if not cat_dir.is_dir():
            continue
        if category == "Archive-Huge":
            for family_dir in sorted([p for p in cat_dir.iterdir() if p.is_dir()], key=lambda p: p.name.lower()):
                if family_dir.name not in archive_families:
                    found.append((family_dir, "archive-family-unknown", None, family_dir.name))
                    continue
                for model_dir in sorted([p for p in family_dir.iterdir() if p.is_dir()], key=lambda p: p.name.lower()):
                    found.append((model_dir, "archive", "Archive-Huge", family_dir.name))
        elif category == "RAG":
            # RAG is a workflow area. Audit its immediate subfolders as workflow
            # buckets, not model weights, unless they contain Hermes metadata.
            for child in sorted([p for p in cat_dir.iterdir() if p.is_dir()], key=lambda p: p.name.lower()):
                if (child / METADATA).exists():
                    found.append((child, "active", category, None))
                else:
                    found.append((child, "workflow", category, None))
        else:
            for model_dir in sorted([p for p in cat_dir.iterdir() if p.is_dir()], key=lambda p: p.name.lower()):
                found.append((model_dir, "active", category, None))
    return found


def dir_stats(path: Path) -> tuple[float, int, int]:
    total = 0
    files = 0
    payload = 0
    for current_root, dirs, filenames in os.walk(path):
        parts = Path(current_root).relative_to(path).parts
        in_cache = ".cache" in parts
        # Do not let filesystem noise inside .cache dominate payload counts.
        for name in filenames:
            fp = Path(current_root) / name
            try:
                st = fp.stat()
            except OSError:
                continue
            total += st.st_size
            files += 1
            if not in_cache:
                payload += 1
    return total / 1024**3, files, payload


def expected_path_for(root: Path, repo_id: str, metadata_category: str | None, archive_family: str | None) -> Path | None:
    name = safe_folder_name(repo_id)
    if archive_family:
        return root / "Archive-Huge" / archive_family / name
    if metadata_category:
        return root / metadata_category / name
    return None


def audit_one(root: Path, item: tuple[Path, str, str | None, str | None]) -> ModelAudit:
    path, scope, category, archive_family = item
    issues: list[str] = []
    status = "unknown"
    repo_id = None
    metadata_category = None
    expected_folder = None
    expected_path = None

    lower_name = path.name.lower()
    if any(token in lower_name for token in ["partial", "bad", "tmp", "staged-complete", "incomplete"]):
        issues.append("suspicious_partial_or_quarantine_name")

    metadata: dict[str, Any] = {}
    metadata_path = path / METADATA
    if metadata_path.exists():
        status = "metadata_present"
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            repo_id = metadata.get("repo_id")
            metadata_category = metadata.get("category")
        except Exception as exc:  # noqa: BLE001 - report parse issue explicitly
            issues.append(f"metadata_parse_error:{type(exc).__name__}:{exc}")
            metadata = {}
    else:
        status = "missing_metadata"
        if scope == "workflow":
            status = "workflow_no_metadata"
        else:
            issues.append("missing_hermes_metadata")

    if repo_id:
        # Some curated local folders intentionally include quantisation / format
        # suffixes instead of matching the upstream HF repo slug. Metadata can
        # declare that local folder name explicitly.
        expected_folder = metadata.get("local_folder_name") or safe_folder_name(repo_id)
        expected = expected_path_for(root, repo_id, metadata_category, archive_family)
        if expected and metadata.get("local_folder_name"):
            expected = expected.parent / str(metadata["local_folder_name"])
        expected_path = str(expected) if expected else None
        if expected_folder != path.name:
            issues.append(f"folder_name_mismatch:expected={expected_folder}")
        if expected and path != expected:
            issues.append(f"path_mismatch:expected={expected}")
    elif scope != "workflow":
        issues.append("missing_repo_id")

    if metadata_category and category and category not in {"Archive-Huge", "RAG"} and metadata_category != category:
        issues.append(f"category_mismatch:metadata={metadata_category}:folder={category}")
    if scope == "archive" and metadata_category and archive_family and metadata_category != archive_family:
        issues.append(f"archive_family_mismatch:metadata={metadata_category}:family={archive_family}")

    size_gib, file_count, payload_count = dir_stats(path)
    if file_count == 0 and scope != "workflow":
        issues.append("empty_model_folder")

    return ModelAudit(
        path=str(path),
        scope=scope,
        category=category,
        archive_family=archive_family,
        folder_name=path.name,
        status=status,
        repo_id=repo_id,
        metadata_category=metadata_category,
        expected_folder_name=expected_folder,
        expected_path=expected_path,
        size_gib=round(size_gib, 4),
        file_count=file_count,
        payload_file_count=payload_count,
        issues=issues,
    )


def write_reports(audits: list[ModelAudit], report_dir: Path, label: str) -> tuple[Path, Path]:
    report_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    json_path = report_dir / f"model-library-audit-{label}-{stamp}.json"
    md_path = report_dir / f"model-library-audit-{label}-{stamp}.md"
    data = [asdict(a) for a in audits]
    json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    issue_rows = [a for a in audits if a.issues]
    complete = [a for a in audits if a.status == "metadata_present" and not a.issues]
    missing_metadata = [a for a in audits if "missing_hermes_metadata" in a.issues]
    duplicate_repo_ids: dict[str, list[ModelAudit]] = {}
    for audit in audits:
        if audit.repo_id:
            duplicate_repo_ids.setdefault(audit.repo_id, []).append(audit)
    duplicate_repo_ids = {k: v for k, v in duplicate_repo_ids.items() if len(v) > 1}

    lines = [
        f"# Model Library Audit ({label})",
        "",
        f"Generated: {stamp}",
        "",
        "## Summary",
        "",
        f"- Total audited folders: `{len(audits)}`",
        f"- Clean model folders: `{len(complete)}`",
        f"- Folders with issues: `{len(issue_rows)}`",
        f"- Missing Hermes metadata: `{len(missing_metadata)}`",
        f"- Duplicate repo IDs: `{len(duplicate_repo_ids)}`",
        "",
        "## Issues",
        "",
    ]
    if not issue_rows:
        lines.append("No structural issues found.")
    else:
        for audit in issue_rows:
            lines += [
                f"### `{audit.path}`",
                f"- Repo ID: `{audit.repo_id}`",
                f"- Category: `{audit.category}`; archive family: `{audit.archive_family}`",
                f"- Size GiB: `{audit.size_gib}`; files: `{audit.file_count}`; payload files: `{audit.payload_file_count}`",
                f"- Issues: `{', '.join(audit.issues)}`",
                "",
            ]
    if duplicate_repo_ids:
        lines += ["", "## Duplicate repo IDs", ""]
        for repo_id, rows in sorted(duplicate_repo_ids.items()):
            lines.append(f"### `{repo_id}`")
            for row in rows:
                lines.append(f"- `{row.path}`")
            lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--label", default="manual")
    parser.add_argument("--report-dir", type=Path, default=DEFAULT_REPORT_DIR)
    args = parser.parse_args()

    cfg = load_config(args.config)
    root = Path(cfg["model_root"])
    if not is_mount_like(root):
        raise SystemExit(f"Model root is not mounted/recognisable: {root}")
    categories = set(cfg["categories"])
    archive_families = set(cfg.get("archive_subfolders", []))
    items = iter_model_dirs(root, categories, archive_families)
    print(f"Auditing {len(items)} folders under {root}", flush=True)
    audits: list[ModelAudit] = []
    for index, item in enumerate(items, 1):
        path = item[0]
        print(f"[{index}/{len(items)}] {path}", flush=True)
        audits.append(audit_one(root, item))
    json_path, md_path = write_reports(audits, args.report_dir, args.label)
    issue_count = sum(1 for audit in audits if audit.issues)
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    print(f"Audited folders: {len(audits)}")
    print(f"Folders with issues: {issue_count}")
    return 1 if issue_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
