#!/usr/bin/env python3
"""Hugging Face model research, download, and sorting helper.

Safe-by-default:
- `research` only reads Hugging Face metadata and writes reports.
- `download` is dry-run unless `--execute` is passed.
- gated models require explicit `--confirm-gated-access` after the user has accepted terms on HF.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

# The model library is an SMB-mounted share. Hugging Face's Xet backend can hit
# file reconstruction I/O errors on SMB targets, so prefer standard/transfer
# downloads unless the caller explicitly overrides this environment variable.
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")

import yaml
from huggingface_hub import HfApi, model_info, snapshot_download, whoami
from huggingface_hub.errors import GatedRepoError, HfHubHTTPError, RepositoryNotFoundError

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = REPO_ROOT / "config" / "model_taxonomy.yaml"
DEFAULT_REPORT_DIR = REPO_ROOT / "reports"


@dataclass
class Candidate:
    repo_id: str
    category: str
    recommendation: str
    score: int
    archive_score: int
    suggested_folder: str
    gated: str
    private: bool | None
    downloads: int | None
    likes: int | None
    pipeline_tag: str | None
    tags: list[str]
    license: str | None
    author: str | None
    last_modified: str | None
    reason: str
    url: str


def load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_mount(model_root: Path) -> None:
    if not model_root.exists():
        raise SystemExit(f"Model root does not exist: {model_root}")
    expected = ["LLM", "Archive-Huge", "Embeddings"]
    missing = [name for name in expected if not (model_root / name).exists()]
    if missing:
        raise SystemExit(
            f"Model root is reachable but does not look like the mounted library. Missing: {missing}. "
            f"If the Mac rebooted, remount with: mount_smbfs //GUEST:@192.168.1.6/models {model_root}"
        )


def safe_folder_name(repo_id: str) -> str:
    return repo_id.split("/", 1)[-1].replace(" ", "-").replace(":", "-")


def parse_license(tags: Iterable[str]) -> str | None:
    for tag in tags:
        if tag.startswith("license:"):
            return tag.split(":", 1)[1]
    return None


def stringify_dt(value: Any) -> str | None:
    if value is None:
        return None
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def local_presence(model_root: Path, repo_id: str) -> tuple[bool, str | None]:
    name = safe_folder_name(repo_id)
    for child in model_root.glob(f"*/{name}"):
        if child.is_dir():
            return True, str(child)
    for child in (model_root / "Archive-Huge").glob(f"*/{name}") if (model_root / "Archive-Huge").exists() else []:
        if child.is_dir():
            return True, str(child)
    return False, None


def category_for_model(cfg: dict[str, Any], repo_id: str, tags: list[str], pipeline_tag: str | None) -> str:
    text = " ".join([repo_id, pipeline_tag or "", *tags]).lower()
    rules = [
        ("Coding", ["coder", "coding", "code-generation", "codegen", "programming", "program synthesis", "code llama", "deepseek-coder", "qwen-coder"]),
        ("Embeddings", ["embedding", "sentence-similarity", "sentence-transformers", "retrieval"]),
        ("Rerankers", ["reranker", "reranking", "cross-encoder"]),
        ("Speech-STT", ["automatic-speech-recognition", "whisper", "asr"]),
        ("Speech-TTS", ["text-to-speech", "tts", "voice"]),
        ("Diffusion-Image", ["text-to-image", "image-to-image", "diffusion", "flux", "stable-diffusion"]),
        ("Video", ["text-to-video", "image-to-video", "video"]),
        ("Vision-OCR", ["ocr", "document-question-answering", "image-to-text", "document"]),
        ("Multimodal", ["image-text-to-text", "vision-language", "multimodal", "vlm"]),
        ("Safety-Moderation", ["moderation", "safety", "toxicity", "guardrail", "nsfw"]),
        ("Computer-Vision", ["object-detection", "image-classification", "segmentation", "depth-estimation"]),
        ("Time-Series", ["time-series", "forecasting"]),
        ("Audio", ["text-to-audio", "audio-to-audio", "music"]),
        ("Agents-ToolUse", ["tool-calling", "function-calling", "agent", "computer-use"]),
    ]
    for category, needles in rules:
        if any(n in text for n in needles) and category in cfg["categories"]:
            return category
    return "LLM" if (pipeline_tag == "text-generation" or "text-generation" in tags) else "Unsorted-Pending-Review"


def score_candidate(cfg: dict[str, Any], repo_id: str, category: str, tags: list[str], downloads: int | None, likes: int | None, gated: str, pipeline_tag: str | None) -> tuple[int, int, str, str]:
    org = repo_id.split("/", 1)[0]
    trusted = org in set(cfg.get("trusted_orgs", []))
    tag_text = " ".join(tags).lower()
    downloads = downloads or 0
    likes = likes or 0

    score = 0
    reasons = []
    if trusted:
        score += 18
        reasons.append("trusted org")
    if downloads > 100_000:
        score += 18
        reasons.append("high downloads")
    elif downloads > 10_000:
        score += 10
        reasons.append("meaningful downloads")
    elif downloads > 1_000:
        score += 5
    if likes > 1000:
        score += 14
        reasons.append("high likes")
    elif likes > 200:
        score += 8
    elif likes > 50:
        score += 4

    practical_signals = ["gguf", "llama.cpp", "openvino", "mlx", "4bit", "8bit", "awq", "gptq", "quant"]
    if any(sig in tag_text or sig in repo_id.lower() for sig in practical_signals):
        score += 18
        reasons.append("local/quant tooling signal")

    if category in {"Embeddings", "Rerankers", "Coding", "LLM", "Speech-STT", "Vision-OCR"}:
        score += 10
        reasons.append("priority category")
    if gated not in {"False", "false", "None", "none"}:
        score -= 6
        reasons.append("gated access")

    archive_score = 0
    if trusted:
        archive_score += 25
    if category in {"LLM", "Coding", "Multimodal", "Diffusion-Image", "Video"}:
        archive_score += 15
    if any(x in repo_id.lower() for x in ["kimi", "deepseek", "qwen", "llama", "mistral", "gemma", "gpt-oss"]):
        archive_score += 18
    if any(x in tag_text for x in ["moe", "mixture", "reasoning", "long-context", "multimodal"]):
        archive_score += 12
    if downloads > 50_000 or likes > 500:
        archive_score += 15
    if gated not in {"False", "false", "None", "none"}:
        archive_score += 6

    thresholds = cfg.get("recommendation_thresholds", {})
    if archive_score >= thresholds.get("archive_score", 75) and score < thresholds.get("download_now_score", 70):
        rec = "Archive"
    elif score >= thresholds.get("download_now_score", 70):
        rec = "Download Now"
    elif score >= thresholds.get("watch_score", 45) or archive_score >= 45:
        rec = "Watch"
    else:
        rec = "Ignore"

    return min(score, 100), min(archive_score, 100), rec, ", ".join(reasons) or "low available signal"


def model_to_candidate(cfg: dict[str, Any], model: Any, model_root: Path) -> Candidate:
    repo_id = model.id
    tags = list(getattr(model, "tags", []) or [])
    pipeline_tag = getattr(model, "pipeline_tag", None)
    category = category_for_model(cfg, repo_id, tags, pipeline_tag)
    gated = str(getattr(model, "gated", None))
    private = getattr(model, "private", None)
    downloads = getattr(model, "downloads", None)
    likes = getattr(model, "likes", None)
    license_name = parse_license(tags)
    score, archive_score, rec, reason = score_candidate(cfg, repo_id, category, tags, downloads, likes, gated, pipeline_tag)
    folder_category = "Archive-Huge" if rec == "Archive" else category
    if folder_category == "Archive-Huge":
        suggested = model_root / "Archive-Huge" / (category if category != "Unsorted-Pending-Review" else "Unsorted-Pending-Review") / safe_folder_name(repo_id)
    else:
        suggested = model_root / folder_category / safe_folder_name(repo_id)
    present, present_path = local_presence(model_root, repo_id)
    if present:
        reason = f"already present at {present_path}; {reason}"
    return Candidate(
        repo_id=repo_id,
        category=category,
        recommendation=rec,
        score=score,
        archive_score=archive_score,
        suggested_folder=str(suggested),
        gated=gated,
        private=private,
        downloads=downloads,
        likes=likes,
        pipeline_tag=pipeline_tag,
        tags=tags[:30],
        license=license_name,
        author=getattr(model, "author", None),
        last_modified=stringify_dt(getattr(model, "last_modified", None)),
        reason=reason,
        url=f"https://huggingface.co/{repo_id}",
    )


def dedupe(candidates: list[Candidate]) -> list[Candidate]:
    best: dict[str, Candidate] = {}
    for c in candidates:
        old = best.get(c.repo_id)
        if old is None or (c.score + c.archive_score) > (old.score + old.archive_score):
            best[c.repo_id] = c
    return sorted(best.values(), key=lambda c: (c.recommendation != "Download Now", -(c.score + c.archive_score), c.repo_id.lower()))


def cmd_init_dirs(args: argparse.Namespace) -> None:
    cfg = load_config(args.config)
    root = Path(cfg["model_root"])
    ensure_mount(root.parent if root.name == "models" and not root.exists() else root)
    root.mkdir(parents=True, exist_ok=True)
    for category, meta in cfg["categories"].items():
        if category == "Archive-Huge":
            continue
        (root / category).mkdir(exist_ok=True)
        for sub in meta.get("subfolders", []) or []:
            (root / category / sub).mkdir(parents=True, exist_ok=True)
    archive = root / "Archive-Huge"
    archive.mkdir(exist_ok=True)
    for sub in cfg.get("archive_subfolders", []):
        (archive / sub).mkdir(parents=True, exist_ok=True)
    print(f"Ensured taxonomy directories under {root}")


def cmd_scan_library(args: argparse.Namespace) -> None:
    cfg = load_config(args.config)
    root = Path(cfg["model_root"])
    ensure_mount(root)
    print(f"Model library: {root}")
    for cat in sorted([p for p in root.iterdir() if p.is_dir()], key=lambda p: p.name.lower()):
        children = sorted([c for c in cat.iterdir() if c.is_dir()], key=lambda p: p.name.lower())
        print(f"\n{cat.name}/ ({len(children)} dirs)")
        for child in children[: args.limit]:
            print(f"  - {child.name}/")
        if len(children) > args.limit:
            print(f"  ... {len(children) - args.limit} more")


def cmd_status(args: argparse.Namespace) -> None:
    cfg = load_config(args.config)
    root = Path(cfg["model_root"])
    print(f"Repo: {REPO_ROOT}")
    print(f"Model root: {root}")
    try:
        ensure_mount(root)
        print("Model mount: OK")
    except SystemExit as e:
        print(f"Model mount: PROBLEM - {e}")
    try:
        me = whoami()
        print(f"HF login: OK ({me.get('name') or me.get('fullname') or 'unknown'})")
    except Exception as e:
        print(f"HF login: PROBLEM - {type(e).__name__}: {e}")


def research_for_category(api: HfApi, cfg: dict[str, Any], model_root: Path, category: str, limit: int) -> list[Candidate]:
    meta = cfg["categories"][category]
    found = []
    tasks = meta.get("hf_tasks") or []
    terms = meta.get("search_terms") or []
    # Recent and high-usage models by task. Hugging Face Hub does not expose a
    # separate direction argument in current huggingface_hub versions.
    for task in tasks[:3]:
        for sort_key in ["createdAt", "downloads", "likes"]:
            try:
                found.extend(api.list_models(pipeline_tag=task, sort=sort_key, limit=limit, full=True))
            except Exception as e:
                print(f"WARN: task search failed for {category}/{task}/{sort_key}: {e}", file=sys.stderr)
    # Search term models by recency and usage. This catches terms like GGUF,
    # reranker, whisper, FLUX, etc. that may not have reliable pipeline tags.
    for term in terms[:4]:
        for sort_key in ["createdAt", "downloads"]:
            try:
                found.extend(api.list_models(search=term, sort=sort_key, limit=limit, full=True))
            except Exception as e:
                print(f"WARN: text search failed for {category}/{term}/{sort_key}: {e}", file=sys.stderr)
    return [model_to_candidate(cfg, m, model_root) for m in found]


def write_reports(candidates: list[Candidate], report_dir: Path, label: str) -> tuple[Path, Path]:
    report_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    json_path = report_dir / f"model-research-{label}-{stamp}.json"
    md_path = report_dir / f"model-research-{label}-{stamp}.md"
    json_path.write_text(json.dumps([asdict(c) for c in candidates], indent=2), encoding="utf-8")
    lines = [f"# Model Research Report ({label})", "", f"Generated: {stamp}", ""]
    for outcome in ["Download Now", "Archive", "Watch", "Ignore"]:
        group = [c for c in candidates if c.recommendation == outcome]
        lines += [f"## {outcome} ({len(group)})", ""]
        for c in group[:50]:
            lines += [
                f"### {c.repo_id}",
                f"- Category: `{c.category}`",
                f"- Score: runnable `{c.score}/100`, archive `{c.archive_score}/100`",
                f"- Gated: `{c.gated}`; license: `{c.license or 'unknown'}`",
                f"- Downloads/Likes: `{c.downloads}` / `{c.likes}`",
                f"- Suggested folder: `{c.suggested_folder}`",
                f"- URL: {c.url}",
                f"- Reason: {c.reason}",
                "",
            ]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path


def cmd_research(args: argparse.Namespace) -> None:
    cfg = load_config(args.config)
    root = Path(cfg["model_root"])
    ensure_mount(root)
    api = HfApi()
    categories = args.category or [c for c in cfg["categories"] if c not in {"Archive-Huge", "RAG"}]
    candidates: list[Candidate] = []
    for category in categories:
        if category not in cfg["categories"]:
            raise SystemExit(f"Unknown category: {category}")
        print(f"Researching {category}...")
        candidates.extend(research_for_category(api, cfg, root, category, args.limit))
    candidates = dedupe(candidates)
    if args.outcome:
        candidates = [c for c in candidates if c.recommendation in args.outcome]
    json_path, md_path = write_reports(candidates, args.report_dir, args.label)
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    print(f"Candidates: {len(candidates)}")
    for outcome in ["Download Now", "Archive", "Watch", "Ignore"]:
        print(f"  {outcome}: {sum(1 for c in candidates if c.recommendation == outcome)}")


def snapshot_size_gib(info: Any) -> float | None:
    siblings = getattr(info, "siblings", None) or []
    sizes = [getattr(s, "size", None) for s in siblings]
    known = [s for s in sizes if isinstance(s, int)]
    if not known:
        return None
    return sum(known) / 1024**3


def copy_tree_contents(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)


def payload_files(root: Path, *, exclude_cache: bool = True) -> set[str]:
    files: set[str] = set()
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if exclude_cache and ".cache" in rel.parts:
            continue
        files.add(str(rel))
    return files


def verify_payload_copy(src: Path, dst: Path, *, exclude_cache: bool = True) -> None:
    src_files = payload_files(src, exclude_cache=exclude_cache)
    dst_files = payload_files(dst, exclude_cache=exclude_cache)
    missing = sorted(src_files - dst_files)
    extra = sorted(dst_files - src_files)
    print(f"Source payload files: {len(src_files)}")
    print(f"Destination payload files: {len(dst_files)}")
    if missing or extra:
        preview = {
            "missing_in_destination": missing[:20],
            "extra_in_destination": extra[:20],
            "missing_count": len(missing),
            "extra_count": len(extra),
        }
        raise SystemExit("Payload verification failed:\n" + json.dumps(preview, indent=2))
    print("Payload verification: OK")


def rsync_inplace_copy(src: Path, dst: Path, *, exclude_cache: bool = True) -> None:
    """Copy staged payload to a mounted target using SMB-friendly rsync flags.

    macOS ships an old rsync/openrsync. Avoid --info=progress2 and avoid the
    default temp-file rename path that can fail on SMB with dot-file permission
    errors. --inplace writes directly to the destination file, and .cache is
    optional Hugging Face transfer metadata that does not need to live on the
    model share.
    """
    dst.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.setdefault("COPYFILE_DISABLE", "1")
    cmd = ["rsync", "-rt", "--inplace", "--progress"]
    if exclude_cache:
        cmd += ["--exclude", ".cache/"]
    cmd += [str(src) + "/", str(dst) + "/"]
    print("Rsync staged payload to final target:")
    print("CMD: " + " ".join(cmd))
    subprocess.run(cmd, cwd=REPO_ROOT, env=env, check=True)


def copy_staged_to_target(src: Path, dst: Path, args: argparse.Namespace) -> None:
    method = args.staging_copy_method
    if method == "auto":
        # SMB-mounted targets on macOS are more reliable with rsync --inplace
        # than shutil/copytree or rsync's default temp-file rename behaviour.
        method = "rsync-inplace" if platform.system() == "Darwin" else "shutil"
    print(f"Staging copy method: {method}")
    if method == "rsync-inplace":
        rsync_inplace_copy(src, dst, exclude_cache=args.exclude_staging_cache)
    elif method == "shutil":
        copy_tree_contents(src, dst)
    else:
        raise SystemExit(f"Unknown staging copy method: {method}")
    verify_payload_copy(src, dst, exclude_cache=args.exclude_staging_cache)


def cmd_download(args: argparse.Namespace) -> None:
    cfg = load_config(args.config)
    root = Path(cfg["model_root"])
    ensure_mount(root)
    repo_id = args.repo_id
    try:
        info = model_info(repo_id, files_metadata=True)
    except RepositoryNotFoundError as e:
        raise SystemExit(f"Repository not found or inaccessible: {repo_id}\n{e}")
    except HfHubHTTPError as e:
        raise SystemExit(f"Could not query model: {repo_id}\n{e}")

    tags = list(info.tags or [])
    category = args.category or category_for_model(cfg, repo_id, tags, info.pipeline_tag)
    if category not in cfg["categories"] and category != "Unsorted-Pending-Review":
        raise SystemExit(f"Unknown category: {category}")

    gated = str(info.gated)
    if gated not in {"False", "false", "None", "none"} and not args.confirm_gated_access:
        raise SystemExit(
            f"{repo_id} is gated ({gated}). Approve access at https://huggingface.co/{repo_id} "
            "then rerun with --confirm-gated-access."
        )

    if args.archive:
        family = category if category in cfg.get("archive_subfolders", []) else "Unsorted-Pending-Review"
        target = root / "Archive-Huge" / family / safe_folder_name(repo_id)
    else:
        target = root / category / safe_folder_name(repo_id)

    if target.exists() and not args.resume:
        raise SystemExit(f"Target already exists: {target}. Use --resume to continue/update.")

    size_gib = snapshot_size_gib(info)
    target_has_partial = target.exists() and not (target / "_hermes_model_metadata.json").exists()
    use_staging = False
    download_dir = target
    staging_root = Path(args.staging_dir).expanduser() if args.staging_dir else None
    if staging_root and not (args.repair_direct_to_target and target_has_partial):
        if size_gib is not None and size_gib <= args.local_staging_threshold_gib:
            use_staging = True
            download_dir = staging_root / safe_folder_name(repo_id)

    print(f"Repo: {repo_id}")
    print(f"Category: {category}")
    print(f"Gated: {gated}")
    print(f"Estimated size: {size_gib:.2f} GiB" if size_gib is not None else "Estimated size: unknown")
    print(f"Target: {target}")
    print(f"Download dir: {download_dir}")
    print(f"Use local staging: {use_staging}")
    print(f"Max workers: {args.max_workers}")
    print(f"Allow patterns: {args.allow_pattern or '[all files]'}")
    print(f"Ignore patterns: {args.ignore_pattern or '[none]'}")
    if not args.execute:
        print("DRY RUN ONLY. Add --execute to download.")
        return

    os.environ.setdefault("HF_HUB_ENABLE_HF_TRANSFER", "1")
    download_dir.mkdir(parents=True, exist_ok=True)
    try:
        snapshot_download(
            repo_id=repo_id,
            local_dir=download_dir,
            allow_patterns=args.allow_pattern,
            ignore_patterns=args.ignore_pattern,
            max_workers=args.max_workers,
        )
    except GatedRepoError as e:
        raise SystemExit(f"Gated repository access failed. Approve on HF first: https://huggingface.co/{repo_id}\n{e}")

    metadata = {
        "repo_id": repo_id,
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "category": category,
        "archive": args.archive,
        "gated": gated,
        "license": parse_license(tags),
        "url": f"https://huggingface.co/{repo_id}",
        "allow_patterns": args.allow_pattern,
        "ignore_patterns": args.ignore_pattern,
        "estimated_size_gib": size_gib,
        "used_local_staging": use_staging,
        "download_dir": str(download_dir),
        "target": str(target),
        "max_workers": args.max_workers,
        "staging_copy_method": args.staging_copy_method if use_staging else None,
        "excluded_staging_cache_from_target": args.exclude_staging_cache if use_staging else None,
    }
    (download_dir / "_hermes_model_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    if use_staging:
        print(f"Copying staged download to final target: {target}")
        copy_staged_to_target(download_dir, target, args)
        if not args.keep_staging:
            print(f"Removing staging dir: {download_dir}")
            shutil.rmtree(download_dir)
    print(f"Download complete: {target}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status", help="Check HF auth and model mount status")
    s.set_defaults(func=cmd_status)

    s = sub.add_parser("init-dirs", help="Ensure taxonomy folders exist")
    s.set_defaults(func=cmd_init_dirs)

    s = sub.add_parser("scan-library", help="Print local model library contents")
    s.add_argument("--limit", type=int, default=25)
    s.set_defaults(func=cmd_scan_library)

    s = sub.add_parser("research", help="Research Hugging Face model candidates and write JSON/Markdown reports")
    s.add_argument("--category", action="append", help="Category to research; repeatable. Default: all active categories")
    s.add_argument("--limit", type=int, default=8, help="Results per search/task query")
    s.add_argument("--label", default="manual")
    s.add_argument("--report-dir", type=Path, default=DEFAULT_REPORT_DIR)
    s.add_argument("--outcome", action="append", choices=["Download Now", "Archive", "Watch", "Ignore"], help="Filter report to one or more outcomes")
    s.set_defaults(func=cmd_research)

    s = sub.add_parser("download", help="Download and sort a model snapshot")
    s.add_argument("repo_id")
    s.add_argument("--category", help="Override category destination")
    s.add_argument("--archive", action="store_true", help="Place under Archive-Huge/<category>/")
    s.add_argument("--allow-pattern", action="append", help="hf snapshot allow pattern; repeatable")
    s.add_argument("--ignore-pattern", action="append", default=["*.msgpack", "*.h5"], help="hf snapshot ignore pattern; repeatable")
    s.add_argument("--confirm-gated-access", action="store_true", help="Assert the user has approved this gated model on Hugging Face")
    s.add_argument("--resume", action="store_true", help="Allow downloading into an existing target folder")
    s.add_argument("--staging-dir", help="Optional local staging directory. If set and the model fits the threshold, download here first, then copy to final target.")
    s.add_argument("--local-staging-threshold-gib", type=float, default=120.0, help="Use local staging only when the estimated snapshot size is <= this value. Default: 120 GiB")
    s.add_argument("--repair-direct-to-target", action="store_true", help="If the final target already has partial files, resume directly there instead of using staging.")
    s.add_argument("--keep-staging", action="store_true", help="Do not remove local staging after a successful copy to the model share.")
    s.add_argument("--staging-copy-method", choices=["auto", "rsync-inplace", "shutil"], default="auto", help="How to copy a completed local staging download to the final target. auto uses SMB-friendly rsync --inplace on macOS. Default: auto")
    s.add_argument("--include-staging-cache", dest="exclude_staging_cache", action="store_false", help="Also copy Hugging Face .cache metadata from staging. Default excludes .cache from final model-share targets.")
    s.set_defaults(exclude_staging_cache=True)
    s.add_argument("--max-workers", type=int, default=2, help="Hugging Face download worker count. Lower is slower but more reliable. Default: 2")
    s.add_argument("--execute", action="store_true", help="Actually download; otherwise dry-run")
    s.set_defaults(func=cmd_download)
    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
