# AI Models

Project workspace for AI model research, comparison, experiments, notes, and implementation work.

## Purpose

Use this repository to collect and develop work related to AI models, including:

- model comparisons and evaluations
- prompt and agent experiments
- local/cloud model notes
- benchmarking ideas
- tooling and scripts
- implementation notes and project decisions
- Hugging Face model research, download approval, sorting, and archive workflows

## Current model library

The live model library is mounted on the Mac Mini at:

```text
/Users/davideddy/mnt/models
```

The backing SMB share is:

```text
//GUEST:@192.168.1.6/models
```

If the Mac Mini has rebooted and the folder appears empty, remount it with:

```bash
mount_smbfs //GUEST:@192.168.1.6/models /Users/davideddy/mnt/models
```

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

## Safety defaults

- Research is read-only.
- Download is dry-run unless `--execute` is passed.
- Gated models require explicit `--confirm-gated-access`.
- Huge archives should be approved manually before downloading.
- The Hugging Face token should not be committed or pasted into project files.

## Status

Initial model research/download/sorting framework implemented by Hermes.
