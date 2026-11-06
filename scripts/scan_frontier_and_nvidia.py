#!/usr/bin/env python3
"""New-frontier-release scan plus NVIDIA-only (NVFP4/FP4) build scan.

Frontier: HF repos created in the last N days with >= MIN_LIKES across generation tasks.
NVIDIA-only: NVFP4/FP4 builds of (a) frontier finds and (b) models already held.
Writes reports/frontier-nvidia-scan-<stamp>.json/.md. Read-only; never downloads.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

from huggingface_hub import HfApi, model_info

REPO = Path(__file__).resolve().parents[1]
REPORTS = REPO / "reports"
MODEL_ROOT = Path("/Users/davideddy/mnt/models")
TASKS = ["text-generation", "image-text-to-text", "any-to-any", "text-to-image", "text-to-video", "image-to-video",
         "text-to-speech", "automatic-speech-recognition"]
QUANT = re.compile(r"gguf|awq|gptq|mlx|4bit|8bit|exl[23]?|nvfp4|fp4|fp8|int4|int8|bnb", re.I)
NV = re.compile(r"nvfp4|fp4-local|(?<![a-z])fp4(?![a-z])|tensorrt|trtllm", re.I)
UNC = re.compile(r"uncensored|abliterat|heretic|nsfw|decensor|unfiltered", re.I)


def held() -> tuple[set[str], set[str]]:
    """Repo ids (from metadata on the share) and folder names currently held."""
    ids, names = set(), set()
    for pat in ("*/*/_hermes_model_metadata.json", "*/*/*/_hermes_model_metadata.json",
                "Uncensored/Civitai/*/*/*/_hermes_model_metadata.json"):
        for m in MODEL_ROOT.glob(pat):
            names.add(m.parent.name.lower())
            try:
                rid = json.loads(m.read_text()).get("repo_id")
                if rid:
                    ids.add(str(rid).lower())
            except Exception:  # noqa: BLE001
                pass
    return ids, names


def queued() -> set[str]:
    out = set()
    for f in (REPO / "scripts" / "batches").glob("2026-11-queue-v7.sh"):
        out |= {m.lower() for m in re.findall(r"^(?:archive|small) (\S+/\S+)", f.read_text(), re.M)}
    return out


def size_info(rid: str) -> dict:
    try:
        i = model_info(rid, files_metadata=True)
    except Exception as e:  # noqa: BLE001
        return {"error": type(e).__name__}
    lic = next((t.split(":", 1)[1] for t in (i.tags or []) if t.startswith("license:")), None)
    return {"gib": round(sum(s.size or 0 for s in i.siblings or []) / 1024**3, 1), "license": lic,
            "gated": str(i.gated), "created": str(i.created_at)[:10]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=21)
    ap.add_argument("--min-likes", type=int, default=100)
    args = ap.parse_args()
    api = HfApi()
    now = datetime.now(timezone.utc)
    cut = now - timedelta(days=args.days)
    ids, names = held()
    q = queued()

    def status(rid: str) -> str:
        r = rid.lower()
        if r in ids or r.split("/", 1)[1] in names:
            return "held"
        return "queued" if r in q else "new"

    frontier: dict[str, dict] = {}
    for task in TASKS:
        for sort in ("trending_score", "likes"):
            for m in api.list_models(pipeline_tag=task, sort=sort, limit=150, full=False):
                if not m.created_at or m.created_at < cut or (m.likes or 0) < args.min_likes:
                    continue
                if QUANT.search(m.id) or UNC.search(m.id) or m.id in frontier:
                    continue
                frontier[m.id] = {"id": m.id, "task": task, "likes": m.likes, "downloads": m.downloads,
                                  "status": status(m.id)}
    for rec in frontier.values():
        if rec["status"] == "new":
            rec.update(size_info(rec["id"]))

    # NVIDIA-only builds: of frontier finds and of held families
    fams = {r["id"].split("/", 1)[1] for r in frontier.values()}
    fams |= {n for n in (p.name for p in (MODEL_ROOT / "Archive-Huge").glob("*/*")) if not NV.search(n)}
    nvidia: dict[str, dict] = {}
    for fam in sorted(fams):
        base = re.sub(r"-(UD-)?(Q\d.*|BF16|FP8.*|GGUF.*)$", "", fam)
        try:
            hits = list(api.list_models(search=base, sort="downloads", limit=25))
        except Exception:  # noqa: BLE001
            continue
        for m in hits:
            if not NV.search(m.id) or "gguf" in m.id.lower() or m.id in nvidia or (m.downloads or 0) < 100:
                continue
            if m.created_at and m.created_at < cut and status(m.id) == "new":
                # only report older NVIDIA builds if nothing for that family is held/queued yet
                pass
            nvidia[m.id] = {"id": m.id, "family": base, "downloads": m.downloads, "status": status(m.id),
                            "official": m.id.split("/")[0].lower() in {"nvidia", base.split("-")[0].lower()}
                            or m.id.split("/")[0].lower() in {"black-forest-labs", "stepfun-ai", "reflection",
                                                              "meta-models", "deepseek-ai", "zai-org", "qwen",
                                                              "minimaxai", "xiaomimimo", "tencent", "moonshotai"}}
    # keep the best (official first, then downloads) 2 per family that are not held/queued
    best: dict[str, list] = {}
    for r in sorted(nvidia.values(), key=lambda r: (not r["official"], -(r["downloads"] or 0))):
        fam = best.setdefault(r["family"], [])
        if r["status"] == "new" and len(fam) < 2:
            fam.append(r)
    picks = [r for v in best.values() for r in v]
    for r in picks:
        r.update(size_info(r["id"]))

    stamp = now.strftime("%Y%m%d-%H%M%SZ")
    out = {"generated_at": now.isoformat(), "days": args.days, "frontier": sorted(frontier.values(), key=lambda r: -(r["likes"] or 0)),
           "nvidia_only_new": picks}
    REPORTS.mkdir(exist_ok=True)
    (REPORTS / f"frontier-nvidia-scan-{stamp}.json").write_text(json.dumps(out, indent=2))
    lines = [f"# Frontier + NVIDIA-only scan {stamp} (last {args.days} days)", "", "## Frontier (new = not held/queued)"]
    for r in out["frontier"]:
        extra = f" · {r.get('gib')} GiB · {r.get('license')} · gated={r.get('gated')}" if r["status"] == "new" else ""
        lines.append(f"- [{r['status']}] `{r['id']}` ({r['task']}, {r['likes']} likes){extra}")
    lines += ["", "## NVIDIA-only builds not held/queued"]
    for r in picks:
        lines.append(f"- `{r['id']}` ({r['family']}{', official' if r['official'] else ''}) · {r.get('gib')} GiB · {r.get('license')} · dl {r['downloads']}")
    (REPORTS / f"frontier-nvidia-scan-{stamp}.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
