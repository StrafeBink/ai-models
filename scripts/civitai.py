#!/usr/bin/env python3
"""Civitai source for the model library: research and verified downloads.

Usage:
  python scripts/civitai.py research --type Checkpoint --type LORA --period Month --limit 50 --label month
  python scripts/civitai.py download <model_id> [--version <version_id>] --category Uncensored/LLM \
      [--folder-name NAME] [--all-files] [--allow-paid] [--execute]

Notes:
- API key is read from $CIVITAI_TOKEN or ~/.config/civitai/token and is never printed or
  passed on a command line (curl reads it from stdin config).
- Safety filter (always on): models flagged as depicting real people (`poi`) or minors
  (`minor`), and face-swap / likeness tools, are refused.
- Paid (`paidAccess`) versions are skipped unless --allow-paid.
- Files are verified with Civitai's published SHA256, copied to the share with
  rsync --inplace, size-verified, and only then is `_hermes_model_metadata.json` written.
- Civitai blocks Australia; this only works through David's VPN (his decision).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vpn_only  # noqa: E402  scripts/vpn_only.py: VPN-only model downloads (Civitai also needs a non-AU exit)

REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = Path("/Users/davideddy/mnt/models")
STAGING = REPO_ROOT / "download-staging" / "civitai"
REPORTS = REPO_ROOT / "reports"
API = "https://civitai.red/api/v1"
METADATA = "_hermes_model_metadata.json"
UNCENSORED_FAMILIES = {"LLM", "Coding", "Multimodal", "Diffusion-Image", "Video", "Audio", "Speech-TTS", "Other"}
BLOCK_PATTERNS = re.compile(
    r"face ?swap|faceswap|face[- ]?id|reactor|lookalike|look-alike|celebrit|real person|deepfake|instantid|pulid",
    re.I,
)


def token() -> str:
    tok = os.environ.get("CIVITAI_TOKEN")
    if not tok:
        p = Path.home() / ".config" / "civitai" / "token"
        tok = p.read_text().strip() if p.exists() else ""
    if not tok:
        raise SystemExit("No Civitai API key: set CIVITAI_TOKEN or ~/.config/civitai/token")
    return tok


def api_get(path: str, params: dict | None = None, auth: bool = True) -> dict:
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True)
    headers = {"User-Agent": "Mozilla/5.0 (hermes model library)"}
    if auth:
        headers["Authorization"] = f"Bearer {token()}"
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=90) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 451:
                raise SystemExit("Civitai returned 451 REGION_BLOCKED (VPN off?).")
            if e.code in (429, 500, 502, 503, 504) and attempt < 4:
                time.sleep(5 * (attempt + 1))
                continue
            raise
        except urllib.error.URLError:
            if attempt < 4:
                time.sleep(5 * (attempt + 1))
                continue
            raise
    raise SystemExit("unreachable")


def blocked_reason(model: dict) -> str | None:
    if model.get("poi"):
        return "depicts a real person (poi)"
    if model.get("minor"):
        return "flagged minor"
    text = " ".join([model.get("name", ""), " ".join(model.get("tags") or [])])
    if BLOCK_PATTERNS.search(text):
        return "face-swap / likeness tool"
    return None


def slug(text: str) -> str:
    text = text.encode("ascii", "ignore").decode()
    text = re.sub(r"[^A-Za-z0-9._-]+", "-", text).strip("-._")
    return re.sub(r"-{2,}", "-", text)[:80] or "model"


def library_index() -> dict[str, str]:
    """civitai model id -> local path, from metadata files under Uncensored/ and other categories."""
    out: dict[str, str] = {}
    for pattern in ("*/*/" + METADATA, "Uncensored/*/*/" + METADATA):
        for meta in MODEL_ROOT.glob(pattern):
            try:
                md = json.loads(meta.read_text())
            except Exception:
                continue
            if md.get("source") == "civitai" and md.get("civitai_model_id"):
                out[str(md["civitai_model_id"])] = str(meta.parent)
    return out


# ---------------------------------------------------------------- research
def cmd_research(args: argparse.Namespace) -> None:
    have = library_index() if MODEL_ROOT.exists() else {}
    rows = []
    for typ in args.type:
        params = {"limit": args.limit, "nsfw": "true", "sort": args.sort, "period": args.period, "types": typ}
        if args.base_model:
            params["baseModels"] = args.base_model
        data = api_get("/models", params)
        for m in data.get("items", []):
            v = (m.get("modelVersions") or [{}])[0]
            f = next((x for x in v.get("files", []) if x.get("primary")), (v.get("files") or [{}])[0])
            rows.append({
                "model_id": m["id"], "version_id": v.get("id"), "name": m["name"], "type": m["type"],
                "base_model": v.get("baseModel"), "nsfw": m.get("nsfw"),
                "downloads": (m.get("stats") or {}).get("downloadCount"),
                "thumbs_up": (m.get("stats") or {}).get("thumbsUpCount"),
                "size_gib": round((f.get("sizeKB") or 0) / 1024 / 1024, 2),
                "paid": bool(v.get("paidAccess")), "paid_access": v.get("paidAccess"),
                "blocked": blocked_reason(m), "in_library": have.get(str(m["id"])),
                "url": f"https://civitai.red/models/{m['id']}",
            })
        time.sleep(1)
    REPORTS.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    jp = REPORTS / f"civitai-research-{args.label}-{stamp}.json"
    jp.write_text(json.dumps(rows, indent=2))
    lines = [f"# Civitai research ({args.label})", "", f"Generated: {stamp}", ""]
    for r in sorted(rows, key=lambda r: -(r["downloads"] or 0)):
        flag = "BLOCKED: " + r["blocked"] if r["blocked"] else ("PAID" if r["paid"] else ("IN LIBRARY" if r["in_library"] else "free"))
        lines.append(f"- [{flag}] {r['type']} `{r['model_id']}` **{r['name']}** — base {r['base_model']}, "
                     f"{r['size_gib']} GiB, {r['downloads']:,} downloads — {r['url']}")
    mp = jp.with_suffix(".md")
    mp.write_text("\n".join(lines) + "\n")
    print(f"Wrote {jp}\nWrote {mp}\nModels: {len(rows)}; free & allowed: "
          f"{sum(1 for r in rows if not r['paid'] and not r['blocked'])}; paid: {sum(r['paid'] for r in rows)}; "
          f"blocked by safety filter: {sum(1 for r in rows if r['blocked'])}")


# ---------------------------------------------------------------- download
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(16 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def curl_download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    # Token goes in via a stdin config so it never appears in `ps` or logs.
    cfg = f'header = "Authorization: Bearer {token()}"\n'
    cmd = ["curl", "-L", "--fail", "--retry", "20", "--retry-delay", "30", "--retry-all-errors",
           "--continue-at", "-", "-K", "-", "--output", str(dest), url]
    print("CMD: curl -L --fail --retry 20 --continue-at - -K <auth> --output", dest, url.split("?")[0])
    subprocess.run(cmd, input=cfg, text=True, check=True)


def rsync_inplace(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, COPYFILE_DISABLE="1")
    cmd = ["rsync", "-rt", "--inplace", "--progress", "--exclude", "/" + METADATA, f"{src}/", f"{dst}/"]
    print("CMD:", " ".join(cmd))
    subprocess.run(cmd, env=env, check=True)


def cmd_download(args: argparse.Namespace) -> None:
    family = args.category.split("/", 1)[1] if args.category.startswith("Uncensored/") else None
    if args.category.startswith("Uncensored/") and family not in UNCENSORED_FAMILIES:
        raise SystemExit(f"Unknown Uncensored family: {family}")
    model = api_get(f"/models/{args.model_id}")
    reason = blocked_reason(model)
    if reason:
        raise SystemExit(f"Refusing {model.get('name')}: {reason}")
    versions = model.get("modelVersions") or []
    if args.version:
        version = next((v for v in versions if str(v["id"]) == str(args.version)), None)
    elif args.base_model:
        wanted = {b.lower() for b in args.base_model}
        version = next((v for v in versions if str(v.get("baseModel", "")).lower() in wanted), None)
        if not version:
            have = sorted({str(v.get("baseModel")) for v in versions})
            raise SystemExit(f"No version of {model.get('name')} for base {args.base_model}; available: {have}")
    else:
        version = versions[0] if versions else None
    if not version:
        raise SystemExit("Version not found")
    if version.get("paidAccess") and not args.allow_paid:
        raise SystemExit(f"Version {version['id']} is paid ({json.dumps(version['paidAccess'])}); rerun with --allow-paid to buy/download.")
    files = version.get("files") or []
    if not args.all_files:
        files = [f for f in files if f.get("primary")] or files[:1]
    folder = args.folder_name or slug(f"{model['name']}-{version.get('name', '')}")
    target = MODEL_ROOT / args.category / folder
    total = sum((f.get("sizeKB") or 0) * 1024 for f in files)
    print(f"Model: {model['name']} ({model['type']}, base {version.get('baseModel')})")
    print(f"Version: {version.get('name')} [{version['id']}]  files: {len(files)}  size: {total / 1024**3:.2f} GiB")
    print(f"Target: {target}")
    if (target / METADATA).exists() and not args.force:
        print(f"Target already has Hermes metadata; assuming complete: {target}")
        return
    if not args.execute:
        print("DRY RUN ONLY. Add --execute to download.")
        return
    stage = STAGING / folder
    stage.mkdir(parents=True, exist_ok=True)
    for f in files:
        dest = stage / f["name"]
        want = (f.get("hashes") or {}).get("SHA256", "").upper()
        if not (dest.exists() and want and sha256(dest) == want):
            vpn_only.run(lambda: curl_download(f["downloadUrl"], dest), what=f["name"])
        got = sha256(dest)
        if want and got != want:
            dest.unlink(missing_ok=True)
            raise SystemExit(f"SHA256 mismatch for {f['name']}: got {got}, expected {want} (partial removed; re-run)")
        print(f"Verified SHA256: {f['name']}")
    # Model card for licence/trigger words
    (stage / "civitai_model.json").write_text(json.dumps({"model": {k: v for k, v in model.items() if k != "modelVersions"},
                                                           "version": version}, indent=2))
    rsync_inplace(stage, target)
    src = {p.relative_to(stage).as_posix(): p.stat().st_size for p in stage.rglob("*") if p.is_file()}
    dst = {p.relative_to(target).as_posix(): p.stat().st_size for p in target.rglob("*") if p.is_file() and p.name != METADATA}
    bad = [k for k in src if dst.get(k) != src[k]]
    if bad:
        raise SystemExit(f"Copy verification failed for: {bad}")
    print("Payload verification: OK")
    meta = {
        "repo_id": f"civitai:{model['id']}@{version['id']}",
        "source": "civitai",
        "civitai_model_id": model["id"],
        "civitai_version_id": version["id"],
        "name": model["name"],
        "version_name": version.get("name"),
        "model_type": model["type"],
        "base_model": version.get("baseModel"),
        "trained_words": version.get("trainedWords"),
        "nsfw": model.get("nsfw"),
        "allow_commercial_use": model.get("allowCommercialUse"),
        "allow_derivatives": model.get("allowDerivatives"),
        "paid_access": version.get("paidAccess"),
        "files": [{"name": f["name"], "sha256": (f.get("hashes") or {}).get("SHA256"), "size_bytes": src.get(f["name"])} for f in files],
        "url": f"https://civitai.red/models/{model['id']}?modelVersionId={version['id']}",
        "category": args.category,
        "local_folder_name": folder,
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "target": str(target),
    }
    (target / METADATA).write_text(json.dumps(meta, indent=2))
    shutil.rmtree(stage)
    print(f"Download complete: {target}")
    try:
        import write_how_to_use
        write_how_to_use.write_one(target)
    except Exception as exc:  # noqa: BLE001 - readme is best-effort
        print(f"Note: could not write _HOW_TO_USE.md ({exc}); run scripts/write_how_to_use.py")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("research")
    r.add_argument("--type", action="append", default=None, help="Checkpoint, LORA, ... (repeatable)")
    r.add_argument("--base-model", action="append", help="Civitai baseModel filter (repeatable)")
    r.add_argument("--period", default="Month", choices=["Day", "Week", "Month", "Year", "AllTime"])
    r.add_argument("--sort", default="Most Downloaded", choices=["Most Downloaded", "Highest Rated", "Newest"])
    r.add_argument("--limit", type=int, default=50)
    r.add_argument("--label", default="manual")
    r.set_defaults(func=cmd_research)
    d = sub.add_parser("download")
    d.add_argument("model_id")
    d.add_argument("--version")
    d.add_argument("--base-model", action="append", help="Pick the newest version for this Civitai baseModel (repeatable)")
    d.add_argument("--category", required=True, help="e.g. Uncensored/Diffusion-Image")
    d.add_argument("--folder-name")
    d.add_argument("--all-files", action="store_true")
    d.add_argument("--allow-paid", action="store_true")
    d.add_argument("--force", action="store_true")
    d.add_argument("--execute", action="store_true")
    d.set_defaults(func=cmd_download)
    args = p.parse_args()
    if args.cmd == "research" and not args.type:
        args.type = ["Checkpoint", "LORA"]
    # Civitai is region-blocked in Australia: all API calls and downloads go VPN-only
    # (pauses if the VPN drops; never falls back to the home connection).
    vpn_only.enable()
    args.func(args)


if __name__ == "__main__":
    main()
