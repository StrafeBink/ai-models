#!/usr/bin/env python3
"""Collect OpenRouter usage statistics as a real-world adoption signal.

Sources:
- Official API: https://openrouter.ai/api/v1/models
  (model list, pricing, context length, and `hugging_face_id` for open weights)
- Public pages (undocumented, page-embedded data; may change without notice):
  - https://openrouter.ai/rankings        -> top models by weekly tokens
  - https://openrouter.ai/<author>/<slug> -> ~30 days of daily token usage

Only open-weight models (those with a `hugging_face_id`) get per-model page
fetches by default, because those are the ones this library can download.

Outputs:
- reports/openrouter-usage-<stamp>.json / .md
- reports/openrouter-usage-latest.json   (read by hf_model_manager.py research)

Read-only: nothing is downloaded.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
REPORTS = REPO_ROOT / "reports"
LATEST = REPORTS / "openrouter-usage-latest.json"

MODELS_URL = "https://openrouter.ai/api/v1/models"
RANKINGS_URL = "https://openrouter.ai/rankings"
MODEL_PAGE_URL = "https://openrouter.ai/{slug}"
USER_AGENT = "Mozilla/5.0 (Macintosh) ai-models-library-research/1.0"

NEXT_CHUNK_RE = re.compile(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)</script>', re.S)


def fetch(url: str, timeout: int = 60, retries: int = 3) -> str:
    last: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except (urllib.error.URLError, TimeoutError) as e:
            last = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"fetch failed for {url}: {last}")


def next_payload(html: str) -> str:
    """Join the Next.js flight-data chunks embedded in a page."""
    out = []
    for chunk in NEXT_CHUNK_RE.findall(html):
        try:
            out.append(json.loads('"' + chunk + '"'))
        except json.JSONDecodeError:
            continue
    return "".join(out)


def query_data(payload: str, key_prefix: str) -> Any | None:
    """Return state.data for the first dehydrated react-query whose queryKey starts with key_prefix."""
    marker = '"queryKey":' + key_prefix
    idx = payload.find(marker)
    if idx < 0:
        return None
    start = payload.rfind('{"dehydratedAt"', 0, idx)
    if start < 0:
        return None
    try:
        obj, _ = json.JSONDecoder().raw_decode(payload[start:])
    except json.JSONDecodeError:
        return None
    return (obj.get("state") or {}).get("data")


def tokens(row: dict[str, Any]) -> int:
    return int(row.get("total_prompt_tokens") or 0) + int(row.get("total_completion_tokens") or 0)


def base_slug(model_id: str) -> str:
    return model_id.split(":", 1)[0]


def load_local_inventory() -> dict[str, Any]:
    """Use the newest structural audit (avoids rescanning the SMB share)."""
    audits = sorted(REPORTS.glob("model-library-audit-*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    repo_ids: set[str] = set()
    folders: list[str] = []
    source = None
    if audits:
        source = str(audits[0])
        for row in json.loads(audits[0].read_text(encoding="utf-8")):
            if row.get("scope") == "workflow":
                continue
            if row.get("repo_id"):
                repo_ids.add(row["repo_id"].lower())
            if row.get("folder_name"):
                folders.append(row["folder_name"].lower())
    return {"repo_ids": repo_ids, "folders": folders, "source": source}


def local_status(hf_id: str, inv: dict[str, Any]) -> str:
    hid = hf_id.lower()
    if hid in inv["repo_ids"]:
        return "installed"
    name = hid.split("/", 1)[-1]
    if any(name == f or f.startswith(name + "-") or f.startswith(name + "_") for f in inv["folders"]):
        return "variant_installed"
    return "missing"


def collect_rankings() -> list[dict[str, Any]]:
    payload = next_payload(fetch(RANKINGS_URL))
    rows = query_data(payload, '["rankings","models"') or []
    out = []
    for rank, r in enumerate(sorted(rows, key=tokens, reverse=True), 1):
        out.append(
            {
                "rank": rank,
                "permaslug": r.get("model_permaslug"),
                "week_tokens": tokens(r),
                "week_requests": int(r.get("count") or 0),
                "week_change_pct": round(float(r.get("change") or 0) * 100, 1),
                "as_of": r.get("date"),
            }
        )
    return out


def collect_model_usage(slug: str) -> dict[str, Any]:
    payload = next_payload(fetch(MODEL_PAGE_URL.format(slug=slug)))
    stats = query_data(payload, '["model-page","appStats"') or {}
    chart = stats.get("model_chart") or []
    daily: dict[str, dict[str, int]] = {}
    for r in chart:
        d = (r.get("date") or "")[:10]
        if not d:
            continue
        day = daily.setdefault(d, {"tokens": 0, "requests": 0})
        day["tokens"] += tokens(r)  # sums all variants (standard/free/...)
        day["requests"] += int(r.get("count") or 0)
    today = datetime.now(timezone.utc).date().isoformat()
    days = sorted((d for d in daily if d < today), reverse=True)  # drop today's partial day
    last7, prev7, last30 = days[:7], days[7:14], days[:30]
    t7 = sum(daily[d]["tokens"] for d in last7)
    p7 = sum(daily[d]["tokens"] for d in prev7)
    if len(prev7) < 7:
        p7 = 0  # not enough history for a fair week-over-week comparison; report as "new"
    return {
        "days_available": len(days),
        "tokens_7d": t7,
        "tokens_prev_7d": p7,
        "tokens_30d": sum(daily[d]["tokens"] for d in last30),
        "requests_7d": sum(daily[d]["requests"] for d in last7),
        "trend_7d_pct": round((t7 - p7) / p7 * 100, 1) if p7 else None,
        "latest_full_day": days[0] if days else None,
    }


def human(n: int | float | None) -> str:
    if n is None:
        return "n/a"
    n = float(n)
    for unit, div in (("T", 1e12), ("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if abs(n) >= div:
            return f"{n / div:.1f}{unit}"
    return f"{n:.0f}"


def usage_tier(tokens_7d: int) -> str:
    if tokens_7d >= 1_000_000_000_000:
        return "very_high"
    if tokens_7d >= 100_000_000_000:
        return "high"
    if tokens_7d >= 10_000_000_000:
        return "meaningful"
    if tokens_7d > 0:
        return "low"
    return "none"


def write_markdown(result: dict[str, Any], path: Path) -> None:
    models = result["models"]
    L = [
        "# OpenRouter Usage Snapshot",
        "",
        f"Generated: {result['generated_at']}",
        "",
        "Real-world adoption signal from OpenRouter. Token counts are summed across all OpenRouter",
        "variants of a model over the last 7 full days (UTC). Usage pages are undocumented public data.",
        "",
        "## Top models on OpenRouter this week (all models, incl. closed)",
        "",
    ]
    by_slug = {m["canonical_slug"]: m for m in models}
    for r in result["rankings"]:
        m = by_slug.get(r["permaslug"]) or {}
        weights = f"open weights `{m['hugging_face_id']}` · library: **{m.get('local_status')}**" if m.get("hugging_face_id") else "closed/unknown weights"
        L.append(f"{r['rank']}. `{r['permaslug']}` — {human(r['week_tokens'])} tokens ({r['week_change_pct']:+.1f}% w/w) · {weights}")
    open_sorted = sorted((m for m in models if m.get("usage")), key=lambda m: m["usage"]["tokens_7d"], reverse=True)
    L += ["", "## Most-used open-weight models (have a Hugging Face repo)", ""]
    for m in open_sorted[:40]:
        u = m["usage"]
        trend = f"{u['trend_7d_pct']:+.0f}%" if u.get("trend_7d_pct") is not None else "new"
        L.append(f"- `{m['hugging_face_id']}` — {human(u['tokens_7d'])} tokens/7d ({trend}) · library: **{m['local_status']}**")
    gaps = [m for m in open_sorted if m["local_status"] == "missing" and m["usage"]["tokens_7d"] >= 10_000_000_000]
    L += ["", "## Popular open-weight models NOT in the library (≥10B tokens/7d)", ""]
    L += [f"- `{m['hugging_face_id']}` — {human(m['usage']['tokens_7d'])} tokens/7d, context {m.get('context_length') or 'n/a'}" for m in gaps] or ["- none"]
    if result["errors"]:
        L += ["", "## Fetch errors", ""] + [f"- `{e['slug']}`: {e['error']}" for e in result["errors"][:20]]
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scope", choices=["open-weight", "all"], default="open-weight", help="Which models get per-model usage fetches")
    ap.add_argument("--rankings-only", action="store_true", help="Only fetch the weekly top-models ranking (1 page)")
    ap.add_argument("--max-model-pages", type=int, default=250)
    ap.add_argument("--delay", type=float, default=0.75, help="Seconds between model page fetches (be polite)")
    args = ap.parse_args()

    REPORTS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    inv = load_local_inventory()

    api_models = json.loads(fetch(MODELS_URL))["data"]
    print(f"OpenRouter models from API: {len(api_models)}")

    # Dedupe variants (:free, :batch, ...) by canonical slug.
    by_slug: dict[str, dict[str, Any]] = {}
    for m in api_models:
        slug = m.get("canonical_slug") or base_slug(m["id"])
        rec = by_slug.setdefault(
            slug,
            {
                "canonical_slug": slug,
                "openrouter_id": base_slug(m["id"]),
                "variants": [],
                "name": m.get("name"),
                "hugging_face_id": m.get("hugging_face_id") or None,
                "context_length": m.get("context_length"),
                "pricing": m.get("pricing"),
                "created": m.get("created"),
            },
        )
        rec["variants"].append(m["id"])
        if not rec["hugging_face_id"] and m.get("hugging_face_id"):
            rec["hugging_face_id"] = m["hugging_face_id"]
        if ":" not in m["id"]:
            rec["openrouter_id"] = m["id"]
            rec["pricing"] = m.get("pricing")

    rankings = collect_rankings()
    rank_by_slug = {r["permaslug"]: r for r in rankings}
    print(f"Weekly ranking rows: {len(rankings)}")

    models = list(by_slug.values())
    for rec in models:
        rec["weekly_rank"] = (rank_by_slug.get(rec["canonical_slug"]) or {}).get("rank")
        rec["local_status"] = local_status(rec["hugging_face_id"], inv) if rec["hugging_face_id"] else "closed_weights"

    errors: list[dict[str, str]] = []
    if not args.rankings_only:
        targets = [m for m in models if args.scope == "all" or m["hugging_face_id"]][: args.max_model_pages]
        print(f"Fetching usage pages for {len(targets)} models...")
        for i, rec in enumerate(targets, 1):
            try:
                rec["usage"] = collect_model_usage(rec["openrouter_id"])
                rec["usage"]["tier"] = usage_tier(rec["usage"]["tokens_7d"])
            except Exception as e:  # keep going; one bad page should not kill the scan
                errors.append({"slug": rec["openrouter_id"], "error": f"{type(e).__name__}: {e}"[:200]})
            if i % 25 == 0:
                print(f"  {i}/{len(targets)}")
            time.sleep(args.delay)

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": {"models_api": MODELS_URL, "rankings": RANKINGS_URL, "model_page": MODEL_PAGE_URL},
        "local_inventory_source": inv["source"],
        "rankings": rankings,
        "models": models,
        "errors": errors,
    }
    json_path = REPORTS / f"openrouter-usage-{stamp}.json"
    md_path = REPORTS / f"openrouter-usage-{stamp}.md"
    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    write_markdown(result, md_path)
    if not args.rankings_only:
        LATEST.write_text(json.dumps(result, indent=2), encoding="utf-8")
    with_usage = sum(1 for m in models if m.get("usage"))
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    print(f"Models with usage data: {with_usage}; fetch errors: {len(errors)}")


if __name__ == "__main__":
    main()
