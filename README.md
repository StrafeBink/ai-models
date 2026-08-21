# AI Models

Project workspace for AI model research, verified file-server storage, curation, AI-box transfer guidance, and implementation notes.

## Purpose

Use this repository to collect and develop work related to AI models, including:

- model comparisons and evaluations
- file-server model library curation
- AI-box transfer priority and handoff notes
- benchmarking ideas and results from the separate AI box
- tooling and scripts
- implementation notes and project decisions
- Hugging Face model research, download approval, sorting, verification, and archive workflows

## Current model library

The live model library is mounted on the Mac Mini at:

```text
/Users/davideddy/mnt/models
```

The backing SMB share details are environment-specific and intentionally not documented with credentials here.

If the Mac Mini has rebooted and the folder appears empty, remount the SMB model share using the known local/private connection details, then verify the mount before moving or downloading models.

## Taxonomy

Top-level model categories:

```text
Agents-ToolUse/
Archive-Huge/
Audio/
Coding/
Computer-Vision/
Diffusion-Image/
Embeddings/
LLM/
Multimodal/
RAG/
Rerankers/
Safety-Moderation/
Speech-STT/
Speech-TTS/
Time-Series/
Video/
Vision-OCR/
```

`RAG/` is reserved for workflow material:

```text
RAG/Bundles/
RAG/Pipelines/
RAG/Experimental/
```

Huge strategic archives live under `Archive-Huge/`, grouped by model family. Example:

```text
Archive-Huge/LLM/Kimi-K3/
```

Full rules live in:

```text
docs/MODEL_RESEARCH_POLICY.md
config/model_taxonomy.yaml
```

## Python environment

Create or refresh the local virtual environment:

```bash
cd "/Users/davideddy/AI Models"
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
python -m pip install -r requirements.txt
```

Hugging Face auth is stored in the standard user cache:

```text
~/.cache/huggingface/token
```

Check login:

```bash
source .venv/bin/activate
hf auth whoami
```

## Model manager

The main helper is:

```text
scripts/hf_model_manager.py
```

### Status check

```bash
source .venv/bin/activate
python scripts/hf_model_manager.py status
```

Checks:

- local model mount
- Hugging Face login

### Ensure taxonomy folders

```bash
python scripts/hf_model_manager.py init-dirs
```

### Scan local library

```bash
python scripts/hf_model_manager.py scan-library
```

### Audit local library structure and metadata

For a deeper verification of folder names, metadata, category placement,
duplicates, suspicious partial folders, sizes, and payload file counts:

```bash
python scripts/audit_model_library.py --label manual
```

Reports are written to:

```text
reports/model-library-audit-<label>-<timestamp>.json
reports/model-library-audit-<label>-<timestamp>.md
```

### Verify selected model integrity

For high-value models, compare local payload files against Hugging Face manifests
without hashing every large weight file:

```bash
python scripts/verify_model_integrity.py --label high-value
```

This checks missing files, exact file sizes, size mismatches, and unexpected
payload files. Curated single-file GGUF folders can be represented with
`selected_file` metadata and are treated as intentional partial selections.

### Functional smoke tests

Run lightweight structural smoke tests for representative local models:

```bash
python scripts/smoke_test_models.py --label representative
```

These tests read JSON configs/tokenizers, GGUF magic headers, and safetensors
headers without loading full model weights into memory.

### Capability and operations reports

Generate the human decision layer for the local library:

```bash
python scripts/generate_capability_reports.py
```

Durable docs are kept in:

```text
docs/MODEL_CAPABILITY_INDEX.md
docs/AI_BOX_TRANSFER_PRIORITY.md
docs/MODEL_STORAGE_DASHBOARD.md
docs/MODEL_REPLACEMENT_REVIEW.md
docs/AI_BOX_SERVING_MAP.md
docs/AI_BOX_HANDOFF_GUIDE.md
```

These reports answer: what each verified model is for, which models are worth manually copying to the separate AI box, what runtime family the AI box will need, what may be superseded, and where file-server storage is concentrated.

### Research Hugging Face models

Research all active categories:

```bash
python scripts/hf_model_manager.py research --label weekly --limit 8
```

Research a single category:

```bash
python scripts/hf_model_manager.py research --category Coding --label coding-smoke --limit 5
```

Reports are written to:

```text
reports/model-research-<label>-<timestamp>.json
reports/model-research-<label>-<timestamp>.md
```

### Dry-run a download

Downloads are dry-run by default:

```bash
python scripts/hf_model_manager.py download Qwen/Qwen2.5-0.5B-Instruct --category LLM
```

Actually download:

```bash
python scripts/hf_model_manager.py download Qwen/Qwen2.5-0.5B-Instruct --category LLM --execute
```

Archive a strategically important model:

```bash
python scripts/hf_model_manager.py download org/huge-model --category LLM --archive --execute
```

For gated models, first approve access on the Hugging Face website, then run with:

```bash
python scripts/hf_model_manager.py download meta-llama/Llama-3.1-8B-Instruct --category LLM --confirm-gated-access --execute
```

### Hybrid local-staging downloads for SMB reliability

For large or fragile downloads, use local staging first and then copy to the
mounted model share. On macOS/SMB, the manager defaults to an SMB-friendly copy
method that avoids rsync temp-file rename failures:

```bash
python scripts/hf_model_manager.py download stabilityai/stable-video-diffusion-img2vid-xt-1-1 \
  --category Video \
  --confirm-gated-access \
  --staging-dir download-staging \
  --local-staging-threshold-gib 120 \
  --staging-copy-method rsync-inplace \
  --max-workers 1 \
  --execute
```

The reusable copy workflow uses:

```bash
COPYFILE_DISABLE=1 rsync -rt --inplace --progress --exclude '.cache/' <staging>/ <target>/
```

and then verifies the source/destination payload file lists, excluding optional
Hugging Face `.cache` transfer metadata.

When `--resume` points at a target that already contains
`_hermes_model_metadata.json`, the manager treats it as complete and skips it
unless `--force-update` is supplied. This prevents repair runs from re-opening
already verified SMB targets.

Use the combined repair runner for a reviewed repair plan:

```bash
python scripts/run_hybrid_repair_plan.py
```

## Safety defaults

- Research is read-only.
- Download is dry-run unless `--execute` is passed.
- Gated models require explicit `--confirm-gated-access`.
- Huge archives should be approved manually before downloading.
- The Hugging Face token should not be committed or pasted into project files.

## Status

Model research/download/sorting framework implemented by Hermes. Current
workflow includes hybrid local-staging downloads with SMB-friendly in-place copy
verification for fragile large model transfers.
