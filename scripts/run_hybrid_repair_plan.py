#!/usr/bin/env python3
"""Run the combined hybrid repair plan.

Policy:
- Use the final mounted target directly for partial repair (`--repair-direct-to-target`).
- Use local staging for clean models that fit the threshold.
- Copy completed staging downloads to SMB with the reusable `rsync --inplace`
  workflow built into `hf_model_manager.py`.
- Use low concurrency and retry transient failures.
"""
from __future__ import annotations

import json
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "reports" / "hybrid-repair-plan.json"
LOG = ROOT / "reports" / f"hybrid-repair-run-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%SZ')}.log"
PYTHON = ROOT / ".venv" / "bin" / "python"
MANAGER = ROOT / "scripts" / "hf_model_manager.py"
STAGING = ROOT / "download-staging"
MAX_ATTEMPTS = 5
RETRY_SLEEP_SECONDS = 180


def is_archive(item: dict) -> bool:
    return item.get("download_mode") == "archive" or item.get("recommendation") == "Archive"


def main() -> int:
    items = json.loads(PLAN.read_text())
    env = os.environ.copy()
    env.setdefault("HF_HUB_DISABLE_XET", "1")
    env.setdefault("HF_HUB_ENABLE_HF_TRANSFER", "1")
    with LOG.open("w", encoding="utf-8") as log:
        def write(msg: str) -> None:
            print(msg, flush=True)
            log.write(msg + "\n")
            log.flush()

        write(f"Hybrid repair run started: {datetime.now(timezone.utc).isoformat()}")
        write(f"Plan: {PLAN}")
        write(f"Items: {len(items)}")
        failures = []
        for idx, item in enumerate(items, 1):
            repo = item["repo_id"]
            category = item["category"]
            archive = is_archive(item)
            cmd = [
                str(PYTHON), str(MANAGER), "download", repo,
                "--category", category,
                "--execute", "--resume",
                "--staging-dir", str(STAGING),
                "--local-staging-threshold-gib", "120",
                "--repair-direct-to-target",
                "--staging-copy-method", "rsync-inplace",
                "--max-workers", "1",
            ]
            if archive:
                cmd.append("--archive")
            if str(item.get("gated")) not in {"False", "false", "None", "none", ""}:
                cmd.append("--confirm-gated-access")
            ok = False
            for attempt in range(1, MAX_ATTEMPTS + 1):
                write(f"[{idx}/{len(items)}] START attempt {attempt}/{MAX_ATTEMPTS}: {repo}")
                write("CMD: " + " ".join(cmd))
                proc = subprocess.run(cmd, cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                write(proc.stdout.rstrip())
                if proc.returncode == 0:
                    write(f"[{idx}/{len(items)}] OK: {repo}")
                    ok = True
                    break
                write(f"[{idx}/{len(items)}] FAIL attempt {attempt}/{MAX_ATTEMPTS} rc={proc.returncode}: {repo}")
                if attempt < MAX_ATTEMPTS:
                    write(f"Sleeping {RETRY_SLEEP_SECONDS}s before retry...")
                    time.sleep(RETRY_SLEEP_SECONDS)
            if not ok:
                failures.append(repo)
                write(f"[{idx}/{len(items)}] GIVE UP after {MAX_ATTEMPTS} attempts: {repo}")
        write(f"Hybrid repair run finished: failures={len(failures)}")
        for repo in failures:
            write(f"FAILED: {repo}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
