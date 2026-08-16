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
