#!/usr/bin/env python3
"""Execute reports/gated-download-plan.json sequentially after user approval."""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "reports" / "gated-download-plan.json"
LOG = ROOT / "reports" / f"gated-download-run-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%SZ')}.log"
MANAGER = ROOT / "scripts" / "hf_model_manager.py"
PYTHON = ROOT / ".venv" / "bin" / "python"


def main() -> int:
    items = json.loads(PLAN.read_text())
    with LOG.open("w", encoding="utf-8") as log:
        def write(msg: str) -> None:
            print(msg, flush=True)
            log.write(msg + "\n")
            log.flush()

        write(f"Gated download run started: {datetime.now(timezone.utc).isoformat()}")
        write(f"Plan: {PLAN}")
        write(f"Items: {len(items)}")
        failures = 0
        for idx, item in enumerate(items, 1):
            repo = item["repo_id"]
            category = item["category"]
            archive = item.get("download_mode") == "archive"
            target = Path(item["suggested_folder"])
            # Recompute target if category override was applied.
            name = repo.split("/", 1)[-1]
            if archive:
                target = Path('/Users/davideddy/mnt/models') / 'Archive-Huge' / category / name
            else:
                target = Path('/Users/davideddy/mnt/models') / category / name
            meta = target / "_hermes_model_metadata.json"
            if meta.exists():
                write(f"[{idx}/{len(items)}] SKIP existing: {repo} -> {target}")
                continue
            cmd = [str(PYTHON), str(MANAGER), "download", repo, "--category", category, "--confirm-gated-access", "--execute", "--resume"]
            if archive:
                cmd.insert(-2, "--archive")
            write(f"[{idx}/{len(items)}] START {'Archive' if archive else 'Download'}: {repo}")
            write("CMD: " + " ".join(cmd))
            proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            write(proc.stdout.rstrip())
            if proc.returncode != 0:
                failures += 1
                write(f"[{idx}/{len(items)}] FAIL rc={proc.returncode}: {repo}")
            else:
                write(f"[{idx}/{len(items)}] OK: {repo}")
        write(f"Gated download run finished: failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
