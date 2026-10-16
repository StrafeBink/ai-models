#!/usr/bin/env python3
"""Resumable per-file archive downloader for very large Hugging Face repos.

This is for cases where snapshot_download directly to the SMB model share is too
fragile or refuses very large LFS files. It downloads one file at a time to local
staging, verifies the size, rsyncs the completed file to the mounted model share,
verifies destination size, then removes the local staging copy.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from huggingface_hub import hf_hub_url, model_info
from huggingface_hub.utils import build_hf_headers

REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = Path("/Users/davideddy/mnt/models")
DEFAULT_STAGING = REPO_ROOT / "download-staging" / "archive-per-file"


def safe_folder_name(repo_id: str) -> str:
    return repo_id.split("/", 1)[-1]


def wanted_files(repo_id: str, ignore_suffixes: tuple[str, ...]) -> dict[str, int]:
    info = model_info(repo_id, files_metadata=True)
    out: dict[str, int] = {}
    for sibling in info.siblings or []:
        rel = sibling.rfilename
        if rel.endswith(ignore_suffixes):
            continue
        size = getattr(sibling, "size", None)
        if size is None:
            continue
        out[rel] = int(size)
    return out


def classify_files(target: Path, expected: dict[str, int]) -> tuple[list[str], list[str], list[str]]:
    complete: list[str] = []
    missing: list[str] = []
    mismatched: list[str] = []
    for rel, size in expected.items():
        p = target / rel
        if not p.exists():
            missing.append(rel)
        elif p.stat().st_size != size:
            mismatched.append(rel)
        else:
            complete.append(rel)
    return complete, missing, mismatched


def redacted_cmd(cmd: list[str]) -> str:
    safe: list[str] = []
    redact_next = False
    for part in cmd:
        if redact_next:
            safe.append("Authorization: Bearer [REDACTED]")
            redact_next = False
            continue
        safe.append(part)
        if part == "-H":
            redact_next = True
    return " ".join(safe)


def run(cmd: list[str], *, env: dict[str, str] | None = None) -> None:
    print("CMD:", redacted_cmd(cmd), flush=True)
    subprocess.run(cmd, check=True, env=env)


def download_with_curl(repo_id: str, revision: str, rel: str, dest: Path, token: str | None) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = hf_hub_url(repo_id, rel, revision=revision)
    cmd = [
        "curl",
        "-L",
        "--fail",
        "--retry",
        "20",
        "--retry-delay",
        "30",
        "--retry-all-errors",
        "--continue-at",
        "-",
        "--output",
        str(dest),
    ]
    if token:
        cmd.extend(["-H", f"Authorization: Bearer {token}"])
    cmd.append(url)
    run(cmd)


def copy_file_to_target(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["COPYFILE_DISABLE"] = "1"
    run(["rsync", "-t", "--inplace", "--progress", str(src), str(dst)], env=env)


def write_metadata(repo_id: str, category: str, target: Path, expected: dict[str, int]) -> None:
    info = model_info(repo_id, files_metadata=True)
    license_tag = None
    for tag in info.tags or []:
        if tag.startswith("license:"):
            license_tag = tag.split(":", 1)[1]
            break
    metadata = {
        "repo_id": repo_id,
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "category": category,
        "archive": True,
        "gated": str(info.gated),
        "license": license_tag,
        "url": f"https://huggingface.co/{repo_id}",
        "ignore_patterns": ["*.msgpack", "*.h5"],
        "estimated_size_gib": sum(expected.values()) / 1024**3,
        "used_local_staging": True,
        "download_dir": str(target),
        "target": str(target),
        "per_file_local_staging": True,
    }
    (target / "_hermes_model_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("repo_id")
    p.add_argument("--category", default="LLM")
    p.add_argument("--target", type=Path)
    p.add_argument("--staging-root", type=Path, default=DEFAULT_STAGING)
    p.add_argument("--revision", default="main")
    p.add_argument("--keep-staging", action="store_true")
    p.add_argument("--max-files", type=int, default=0, help="Optional limit for testing/resume batches")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    target = args.target or MODEL_ROOT / "Archive-Huge" / args.category / safe_folder_name(args.repo_id)
    target.mkdir(parents=True, exist_ok=True)
    staging = args.staging_root / safe_folder_name(args.repo_id)
    staging.mkdir(parents=True, exist_ok=True)

    info = model_info(args.repo_id, files_metadata=True)
    revision = info.sha or args.revision
    expected = wanted_files(args.repo_id, (".msgpack", ".h5"))
    complete, missing, mismatched = classify_files(target, expected)
    todo = missing + mismatched
    if args.max_files:
        todo = todo[: args.max_files]

    print(f"Repo: {args.repo_id}")
    print(f"Target: {target}")
    print(f"Staging: {staging}")
    print(f"Expected files: {len(expected)}")
    print(f"Already complete: {len(complete)}")
    print(f"Missing: {len(missing)}")
    print(f"Mismatched: {len(mismatched)}")
    print(f"This run todo: {len(todo)}")

    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    if not token:
        try:
            from huggingface_hub import get_token
            token = get_token()
        except Exception:
            token = None

    for idx, rel in enumerate(todo, 1):
        expected_size = expected[rel]
        local = staging / rel
        dest = target / rel
        print(f"\n[{idx}/{len(todo)}] {rel} expected={expected_size / 1024**3:.2f} GiB", flush=True)
        if local.exists() and local.stat().st_size == expected_size:
            print("Local staged file already complete")
        else:
            download_with_curl(args.repo_id, revision, rel, local, token)
        actual = local.stat().st_size
        if actual != expected_size:
            raise SystemExit(f"Local size mismatch for {rel}: got {actual}, expected {expected_size}")
        copy_file_to_target(local, dest)
        dest_size = dest.stat().st_size
        if dest_size != expected_size:
            raise SystemExit(f"Destination size mismatch for {rel}: got {dest_size}, expected {expected_size}")
        if not args.keep_staging:
            local.unlink()
            # Remove empty parent dirs under staging.
            parent = local.parent
            while parent != staging and parent.exists():
                try:
                    parent.rmdir()
                except OSError:
                    break
                parent = parent.parent

    complete, missing, mismatched = classify_files(target, expected)
    print(f"\nFinal complete: {len(complete)} / {len(expected)}")
    print(f"Final missing: {len(missing)}")
    print(f"Final mismatched: {len(mismatched)}")
    if missing or mismatched:
        raise SystemExit(1)
    write_metadata(args.repo_id, args.category, target, expected)
    print(f"Metadata written: {target / '_hermes_model_metadata.json'}")
    if not args.keep_staging:
        shutil.rmtree(staging, ignore_errors=True)
        print(f"Removed staging: {staging}")


if __name__ == "__main__":
    main()
