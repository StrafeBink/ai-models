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
- `--resume` now skips targets that already contain `_hermes_model_metadata.json` unless `--force-update` is supplied, preventing repair runs from re-opening verified SMB targets.
- The one-off `scripts/download_stable_video_to_staging.py` recovery script was removed after its workflow was generalised.

Verified recovery:

- `stabilityai/stable-video-diffusion-img2vid-xt-1-1` was successfully installed under:

```text
/Users/davideddy/mnt/models/Video/stable-video-diffusion-img2vid-xt-1-1
```

- Final verified size: `17G`.
- Final verified payload files excluding `.cache`: `18`.
- Bad partial and local staging copies were deleted after verification.

## 2026-08-21 — Gated plan cleanup

Completed the remaining gated-plan category corrections:

- `meta-llama/Prompt-Guard-86M` belongs under `Safety-Moderation/Prompt-Guard-86M`, not `Embeddings/`.
- Stable Video Diffusion belongs under `Video/`, not `Diffusion-Image/`.
- Stable Audio 3 Medium and Stable Audio 3 Small SFX belong under `Audio/`, not `Diffusion-Image/`.

Operational result:

- `reports/gated-download-plan.json` was locally updated so all 19 gated-plan entries now point to complete verified targets.
- `Prompt-Guard-86M` is installed at:

```text
/Users/davideddy/mnt/models/Safety-Moderation/Prompt-Guard-86M
```

- Verified Prompt Guard target size: `1.1G`.
- Verified Prompt Guard payload files excluding `.cache`: `12`.
- Local staging remained empty after the skip-complete verification.

## 2026-08-21 — Full library cleanup and verification

Ran a full structural audit of the mounted model library and then cleaned up all reported issues.

Initial audit result:

```text
Audited folders: 52
Folders with issues: 18
Missing Hermes metadata: 17
Duplicate repo IDs: 0
```

Cleanup actions:

- Added `_hermes_model_metadata.json` to legacy/manual model folders that were missing Hermes metadata.
- Renamed clear Hugging Face slug/case mismatches:
  - `Diffusion-Image/FLUX.2-Dev` → `Diffusion-Image/FLUX.2-dev`
  - `Diffusion-Image/FLUX.2-Klein-9B-FP8` → `Diffusion-Image/FLUX.2-klein-9b-fp8`
- Kept curated quantised local folder names where useful, recording `local_folder_name` in metadata so the audit recognises them as intentional.
- Added reusable audit tooling:

```text
scripts/audit_model_library.py
```

Post-cleanup audit result:

```text
Audited folders: 52
Folders with issues: 0
Missing Hermes metadata: 0
Duplicate repo IDs: 0
```

Latest audit report:

```text
reports/model-library-audit-post-cleanup-20260821-133801Z.md
```

## 2026-08-21 — Integrity checks, smoke tests, and monthly audit cron

Completed the three follow-up verification tasks.

High-value integrity check:

- Added reusable script:

```text
scripts/verify_model_integrity.py
```

- Initial run found two repairable issues:
  - `moonshotai/Kimi-K3`: `encoding_k3.py` size mismatch against Hugging Face.
  - `sentence-transformers/all-MiniLM-L6-v2`: missing optional `tf_model.h5` payload file.
- Repaired both by fetching the exact files from Hugging Face and writing them to the mounted model library.
- Post-repair result:

```text
Checked models: 7
Issues: 0
```

Functional smoke tests:

- Added reusable script:

```text
scripts/smoke_test_models.py
```

- Representative tests covered:
  - MiniLM embeddings
  - Prompt Guard
  - Whisper large v3 turbo
  - GGUF LLM
  - GGUF coding model
  - DeepSeek OCR
  - Stable Video Diffusion
- Result:

```text
Tests: 7
Failures: 0
```

Monthly audit cron:

- Created Hermes cron job:

```text
AI Models monthly library audit
job_id: 2439cd8f55c0
schedule: 0 9 1 * *
next_run_at: 2026-09-01T09:00:00+08:00
```

- Cron script:

```text
~/.hermes/scripts/model-library-monthly-audit.sh
```

- The script is silent when the library is clean and sends an alert only if audit issues appear or the audit cannot produce a report.
