# Project Notes

Use this file for high-level decisions, links, and research notes for the AI Models project.

## 2026-08-16 — Model library automation foundation

Decisions:

- Use `/Users/davideddy/mnt/models` as the canonical mounted model library path on the Hermes Mac Mini.
- Backing SMB share details are private/environment-specific and intentionally not documented with credentials.
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

- If the Mac Mini reboots and `/Users/davideddy/mnt/models` appears empty, remount the configured/private SMB model share at that path, then rerun the status check.

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

## 2026-08-21 — Capability and operations layer

Added a decision layer on top of the verified model folders so the project can answer practical questions such as "what should I use for this capability?", "what is archive-only?", and "where is storage concentrated?".

Added generator:

```text
scripts/generate_capability_reports.py
```

Generated durable docs:

```text
docs/MODEL_CAPABILITY_INDEX.md
docs/MODEL_STORAGE_DASHBOARD.md
docs/MODEL_REPLACEMENT_REVIEW.md
docs/LOCAL_SERVING_MAP.md
docs/RUNTIME_SMOKE_TEST_READINESS.md
```

Key outputs:

- Total downloaded model folders: `49`.
- Total measured model storage: `2700.35 GiB` / `2.64 TiB`.
- Largest concentration: `Archive-Huge/LLM` at `1543.36 GiB` / `57.2%`.
- Largest model: `Kimi-K3` at `1453.79 GiB`, marked as strategic archive.
- Serving map now identifies first candidates for chat/reasoning, coding, embeddings, prompt safety, STT, OCR, image, video, and audio.
- Replacement review identifies benchmark-before-delete candidates such as `whisper-large-v2`, older Llama archive models, older embedding variants, and `stable-diffusion-3-medium`.
- Runtime readiness report confirms the current manager venv is still deliberately lightweight; heavy inference runtimes such as `transformers`, `torch`, `sentence_transformers`, `llama_cpp`, `whisper`, and `faster_whisper` are not installed yet.

## 2026-08-21 — Reframed capability layer for separate AI box

Clarified the project operating model: this Mac/repo is the verified model library and file server; selected models are manually copied to a separate AI box for execution.

Updated the capability report generator to focus on transfer/handoff rather than local runtime installation on the file server:

```text
scripts/generate_capability_reports.py
```

Current durable decision docs:

```text
docs/MODEL_CAPABILITY_INDEX.md
docs/AI_BOX_TRANSFER_PRIORITY.md
docs/MODEL_STORAGE_DASHBOARD.md
docs/MODEL_REPLACEMENT_REVIEW.md
docs/AI_BOX_SERVING_MAP.md
docs/AI_BOX_HANDOFF_GUIDE.md
```

Removed/replaced earlier file-server runtime-oriented docs:

```text
docs/LOCAL_SERVING_MAP.md
docs/RUNTIME_SMOKE_TEST_READINESS.md
```

Key framing changes:

- File server remains focused on discovery, downloads, metadata, verification, storage, and transfer guidance.
- AI-box docs identify what to copy first and what runtime family the AI box needs.
- Transfer priority now separates `high`, `medium`, `review`, and `archive_only` models.
- Strategic archives such as `Kimi-K3` are explicitly marked as keep-on-file-server unless a specific future-hardware test requires transfer.

## 2026-08-25 — AI-box transfer manifests and bundles

Follow-up improvements added after confirming the Mac is a model file server and the AI box is the execution host.

Daily radar:

- Checked Hermes cron job `22313286443e` / `AI Models - Daily Major Release Radar`.
- It is currently healthy; latest status was `ok`, next run scheduled for `2026-08-26T07:00:00+08:00`.

Transfer tooling:

- Added manual transfer manifest generator:

```text
scripts/generate_ai_box_transfer_manifest.py
```

- It reads the verified model audit and writes dated transfer checklists under:

```text
transfer-manifests/
```

- Manifest checklists include source path, suggested AI-box destination placeholder, size, payload file count, metadata verification, and runtime-family hints.

Bundles:

- Added:

```text
docs/AI_BOX_BUNDLES.md
```

- Current bundle names:
  - `minimal-rag`
  - `coding-assistant`
  - `speech-and-docs`
  - `image-generation-small-first`
  - `llm-comparison`

Security hygiene:

- Redacted the explicit SMB connection string from README and from `hf_model_manager.py` mount-error guidance; docs now refer to configured/private SMB details instead of embedding the connection string.

## 2026-09-01 — Qwen smoke/coding additions

Downloaded and verified two approved Watch-list models:

```text
LLM/Qwen3-0.6B
Coding/Qwen2.5-Coder-14B-Instruct-AWQ
```

Verification:

- `Qwen3-0.6B`: metadata present, 11 payload files, 1.41 GiB.
- `Qwen2.5-Coder-14B-Instruct-AWQ`: metadata present, 14 payload files, 9.31 GiB.
- Local `download-staging/` was empty after cleanup.
- Post-download audit: 54 folders, 0 issues.
- Regenerated AI-box capability/priority/storage docs from the newest audit report.
- Generated manual AI-box transfer manifest:

```text
transfer-manifests/ai-box-transfer-qwen-new-downloads-20260901-172543Z.md
```

Script maintenance:

- `scripts/generate_capability_reports.py` now uses the newest `reports/model-library-audit-*.json` instead of a fixed historical audit path.
- `scripts/generate_ai_box_transfer_manifest.py` also uses the newest audit report and now gives clearer runtime hints for LLM/Coding safetensors, AWQ, GGUF, and Qwen-style models.

## 2026-09-07 — Completed all approved Watch/archive downloads

Downloaded or verified all five additional approved models:

```text
LLM/Qwen3-8B
Coding/Qwen2.5-Coder-32B-Instruct-AWQ
Multimodal/Qwen3.6-27B-FP8
Archive-Huge/LLM/gpt-oss-120b
Archive-Huge/LLM/DeepSeek-R1
```

Verification:

- `Qwen3-8B`: 16 payload files, 15.27 GiB, metadata present.
- `Qwen2.5-Coder-32B-Instruct-AWQ`: 16 payload files, 18.01 GiB, metadata present.
- `Qwen3.6-27B-FP8`: 81 payload files, 28.77 GiB, metadata present.
- `gpt-oss-120b`: 38 payload files, 182.32 GiB, metadata present.
- `DeepSeek-R1`: 175 payload files, 641.31 GiB, metadata present.
- Post-download audit: 59 folders, 0 issues.
- Generated transfer manifest:

```text
transfer-manifests/ai-box-transfer-all-approved-downloads-20260907-131056Z.md
```

Operational notes:

- `gpt-oss-120b` exposed two downloader pitfalls: the Python Hugging Face client refuses its 60.8 GiB `metal/model.bin` via regular HTTP, and direct-to-SMB writes can fail with `OSError: [Errno 5] Input/output error` during very large files.
- Added `scripts/download_archive_per_file.py`, which downloads one file at a time to local staging, verifies local size, copies to SMB with `rsync --inplace`, verifies destination size, then removes the local staging file.
- Installed `git-lfs` via Homebrew while investigating the large LFS failure path.
- Sanitized generated logs so bearer tokens are redacted before any project search/commit.

## 2026-10-16 — OpenRouter usage statistics in research scoring

- Added `scripts/openrouter_usage.py`. Official `/api/v1/models` gives 465 models, 158 unique open-weight models with a `hugging_face_id`. The public rankings page and model pages embed weekly top-20 and ~30 days of daily token usage (undocumented; may break).
- `hf_model_manager.py research` now uses the latest snapshot (<14 days) as a scoring signal, matches quants via `base_model:` tags, injects the top 10 popular missing open-weight models as candidates, and penalises >80 GiB / >200 GiB models so huge popular models land in Watch/Archive.
- First snapshot: most-used open-weight models are DeepSeek-V4.1-Flash (~37T tokens/7d), Step-5-Preview, GLM-5.3-Flash, MiMo-V2.6-Flash, Hy4-preview. Kimi-K3 and gpt-oss-120b/20b are already in the library. Nearly all top open-weight models are 150–1,450 GiB, so they are archive-scale.
- Weekly digest cron now runs `research --openrouter refresh` and adds an "OpenRouter adoption" section; daily radar uses `--openrouter-candidates 0` plus `openrouter_usage.py --rankings-only`.

Environment repair (same day):

- Homebrew `python@3.14` had been removed from the Mac, breaking `.venv` (dangling symlink; `source .venv/bin/activate` silently fell through to another Python without `yaml`). Rebuilt `.venv` from the uv-managed CPython 3.14.7 at `~/.local/share/uv/python/cpython-3.14.7-macos-aarch64-none`; old venv kept as `.venv.broken-homebrew-python-<date>`.
- The Mac had rebooted and the SMB model share was not remounted; remounted manually.

## 2026-10-16 — Voice pack and AI-box gap downloads

Downloaded and verified 15 models (112.17 GiB), 0 failures, staging empty, post-download audit 74 folders / 0 issues:

- Speech-TTS (new category in use): Kokoro-82M, Qwen3-TTS-12Hz-1.7B-CustomVoice, Qwen3-TTS-12Hz-1.7B-Base, chatterbox, VibeVoice-1.5B, VoxCPM2
- Speech-STT: parakeet-tdt-0.6b-v3, Qwen3-ASR-1.7B, Nemotron-3-Diarization, silero-vad
- Rerankers (first model): Qwen3-VL-Reranker-2B
- Embeddings: embeddinggemma-2
- LLM: Qwen3.8-27B-UD-Q4_K_XL, gemma-4-26B-A4B-it-UD-Q4_K_XL (single quant + mmproj-F16 from the unsloth GGUF repos)
- Diffusion-Image: Qwen-Image-2.1

Not downloaded: `pyannote/speaker-diarization-community-1` returns 403 until David accepts its terms on Hugging Face.

Update: David approved access; downloaded to `Speech-STT/speaker-diarization-community-1` (11 files, 32 MiB, metadata present). Audit: 75 folders, 0 issues.

Tooling:

- `hf_model_manager.py download --folder-name` sets the local folder (recorded as `local_folder_name`), for single-quant downloads from multi-quant GGUF repos.
- Size estimate now honours `--allow-pattern`/`--ignore-pattern`, so filtered GGUF downloads still use local staging.
- Batch script: `scripts/batches/2026-10-voice-and-gaps.sh`. Transfer manifest for the voice pack (41.74 GiB) generated under `transfer-manifests/`.
- Capability/transfer docs now recognise Speech-TTS, Rerankers, diarisation/VAD, non-Whisper STT and Qwen-Image.
- Share free space after batch: 3.4 TiB (97% used).


## 2026-10-29 — Decisions: auto-remount, archive batch, cleanup review

- Auto-remount: `~/.hermes/scripts/mount-model-share.sh` + LaunchAgent `~/Library/LaunchAgents/ai.hermes.models-mount.plist` (RunAtLoad, every 300 s). Only mounts when the share is missing and the file server answers on port 445; never unmounts; refuses to mount over a non-empty folder. Log: `~/.hermes/logs/model-share-mount.log`. Tested: unmount → script → remounted. The Hermes gateway blocks `launchctl bootstrap`, so the agent starts at next login (or load manually from Terminal).
- Archive batch started with `scripts/download_archive_per_file.py` (per-file local staging, curl handles the 94.6 GiB single file): `Archive-Huge/LLM/DeepSeek-V4-Flash-0731` (155 GiB), `Archive-Huge/Multimodal/GLM-5.3-Flash` (306 GiB), `Archive-Huge/Multimodal/DeepSeek-V4.1-Flash` (475 GiB). ~936 GiB total; leaves ~2.4 TiB free.
- Cleanup review prepared (no deletions without explicit approval).
- Removed the old broken venv backup. Homebrew Python removal was deliberate; the project venv is on the uv-managed CPython 3.14.7.
- Skipped: own OpenRouter account usage tracking; HF token rotation (David's call).

## 2026-10-29 — Frontier swap, new picks, Uncensored category

- Replaced the queued September `DeepSeek-V4.1-Flash` with `DeepSeek-V4.1-Flash-1017` (#1 on OpenRouter). Removed the empty Sept folder. New batch `scripts/batches/2026-10-archives-v2.sh` (supersedes `2026-10-archives.sh`): Unlimited-OCR-2, clef-flash, Qwen-Image-2.1-Turbo, then archives DeepSeek-V4-Flash-0731 (resume), Qwen3.8-Flash-Next-FP4-Local, MiniMax-M3.1-Flash, GLM-5.3-Flash, DeepSeek-V4.1-Flash-1017 (~1.3 TiB total).
- New top-level `Uncensored/` category with family subfolders `LLM, Coding, Multimodal, Diffusion-Image, Video, Audio, Speech-TTS, Other`; models live in `Uncensored/<family>/<model>` and metadata category is `Uncensored/<family>`.
- `uncensored_markers` in `config/model_taxonomy.yaml` (uncensored, abliterated, heretic, unfiltered, decensored, nsfw, not-for-all-audiences, ...) route matching repos to `Uncensored/<family>` in research and download. Classifier tasks (NSFW detectors) stay in Safety-Moderation.
- Research supports per-category `search_sorts` and `max_search_terms`; Uncensored searches 6 terms by trending, likes, downloads and recency. Included in the weekly digest and daily radar crons (both cron prompts now use the mount script instead of an inline SMB string).
- `audit_model_library.py` and presence checks understand the `Uncensored/<family>/` layout.

## 2026-10-16 — Massive scan + voice review

- Full scan (`research --label massive --limit 15 --openrouter refresh --openrouter-candidates 20`): 2,114 candidates; 12 Download Now, 25 Archive, 257 Watch (42 of these already in the library).
- Voice scan (`--category Speech-TTS --category Speech-STT --category Audio --limit 40`): 906 candidates. `Speech-TTS` is empty in the library, and Rerankers, Agents-ToolUse, Computer-Vision and Time-Series also hold no models.
- Scorer fixes: trusted-org match is now case-insensitive (`Tencent` never matched `tencent/...`); `Speech-TTS` is a priority category; added voice specialists (hexgrad, ResembleAI, k2-fsa, openbmb, fishaudio, kyutai, pyannote, ...) and top OpenRouter labs to `trusted_orgs`. Before this, Kokoro-82M, Chatterbox, OmniVoice and VoxCPM2 all scored "Ignore".
- Dedupe now prefers the candidate record that knows the snapshot size, so size penalties are not lost (DeepSeek-V4-Flash-0731, 155 GiB, had shown as Download Now).
- Share free space: 3.6 TiB of 92 TiB (97% used).
