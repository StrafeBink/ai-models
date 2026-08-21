# Project Notes

Use this file for high-level decisions, links, and research notes for the AI Models project.

## 2026-08-16 — Model library automation foundation

Decisions:

- Use `/Users/davideddy/mnt/models` as the canonical mounted model library path on the Hermes Mac Mini.
- Backing SMB share is `//GUEST:@192.168.1.6/models`.
- Current hardware profile: Intel Arc B70; research should separate models that are runnable now from large strategic archive models.
- Keep a broad Hugging Face taxonomy now so automated downloading and sorting has stable destinations.
- Keep `RAG/` for bundles/pipelines/experiments rather than raw embedding or reranker weights.
- Keep `Archive-Huge/` for strategic preservation of important models that are too large to run today.

Implemented:

- `config/model_taxonomy.yaml` — taxonomy, category search terms, trusted orgs, cadence, and scoring thresholds.
- `docs/MODEL_RESEARCH_POLICY.md` — human-readable policy for research, gated models, archive criteria, and report format.
- `scripts/hf_model_manager.py` — CLI for status checks, taxonomy initialisation, library scans, HF research reports, and safe-by-default downloads.
- `requirements.txt` — Python dependencies for the model manager.

Hugging Face login:

- Tooling installed into `.venv` using Python 3.14.
- HF login verified as user `StrafeBink`.
- Token stored in the normal Hugging Face cache, not in this repository.

Operational notes:

- If the Mac Mini reboots and `/Users/davideddy/mnt/models` appears empty, remount with:

```bash
mount_smbfs //GUEST:@192.168.1.6/models /Users/davideddy/mnt/models
```

- Research reports are stored in `reports/` and should be reviewed before downloads are approved.
- Downloads are dry-run unless `--execute` is supplied.
- Gated models require manual Hugging Face approval plus `--confirm-gated-access`.

## 2026-08-21 — Reusable SMB-safe staging workflow

Issue:

- Direct or partial Hugging Face downloads to the SMB model share can stall on macOS in uninterruptible I/O (`U` state).
- The macOS/OpenBSD rsync available here is old (`2.6.9` compatible) and does not support `--info=progress2`.
- Normal rsync temp-file behaviour failed on the SMB share with errors like:

```text
mkstempat: '._hermes_model_metadata...' Permission denied
unexpected end of file
```

Working pattern:

1. Download large/fragile models to local staging when they fit local disk.
2. Copy the completed payload to the SMB target using in-place rsync:

```bash
COPYFILE_DISABLE=1 rsync -rt --inplace --progress --exclude '.cache/' <staging>/ <target>/
```

3. Verify source and destination payload file lists excluding `.cache`.
4. Delete staging and any quarantined bad partial only after verification.

Implemented:

- `scripts/hf_model_manager.py` now has reusable staging copy options:
  - `--staging-copy-method auto|rsync-inplace|shutil`
  - `--include-staging-cache` if Hugging Face cache metadata must also be copied
- On macOS, `auto` selects the SMB-friendly `rsync-inplace` method.
- `scripts/run_hybrid_repair_plan.py` now explicitly uses `--staging-copy-method rsync-inplace`.
- The one-off `scripts/download_stable_video_to_staging.py` recovery script was removed after its workflow was generalised.

Verified recovery:

- `stabilityai/stable-video-diffusion-img2vid-xt-1-1` was successfully installed under:

```text
/Users/davideddy/mnt/models/Video/stable-video-diffusion-img2vid-xt-1-1
```

- Final verified size: `17G`.
- Final verified payload files excluding `.cache`: `18`.
- Bad partial and local staging copies were deleted after verification.
