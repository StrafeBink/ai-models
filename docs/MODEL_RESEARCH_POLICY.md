# Model Research Policy

This project uses Hermes to research, shortlist, download, sort, and archive Hugging Face models for the local model library mounted at:

```text
/Users/davideddy/mnt/models
```

The library is intentionally split between **models to run now** on the current Intel Arc B70 hardware and **strategic archive models** that may be too large to run today but are worth preserving.

## Recommendation outcomes

Every researched model should be assigned exactly one outcome:

| Outcome | Meaning |
|---|---|
| `Download Now` | Worth downloading and likely useful/runnable now. |
| `Watch` | Promising, but wait for better quants, benchmarks, tooling, or access. |
| `Archive` | Strategically important even if too large to run now. |
| `Ignore` | Low-signal, duplicate, unclear, weak, or not relevant. |

## Hardware-aware questions

For each candidate, Hermes should assess:

- Does it have GGUF, safetensors, OpenVINO, or other practical local formats?
- Is there a realistic path for Intel Arc B70 via Vulkan, SYCL, OpenVINO, or CPU fallback?
- What quantisation is likely appropriate: `Q4_K_M`, `Q5_K_M`, `Q6_K`, `IQ4_XS`, `UD-Q4_K_XL`, etc.?
- Is the storage burden reasonable for immediate use?
- Is the model better than, or complementary to, something already in the library?

## Strategic archive criteria

Huge models should not be archived merely because they are large. Archive when at least one criterion is strong:

- major open-weight release from a credible lab
- benchmark/capability frontier relevance
- unique architecture or modality
- important historical release
- possible future hardware value
- takedown, gating, or re-download risk

Archive recommendations should state:

```text
Archive value: High / Medium / Low
Can run now: Yes / Maybe / No
Suggested archive folder: Archive-Huge/<family>/<model>
Suggested files: full snapshot / selected weights / metadata only
Storage estimate: ...
Reason to preserve: ...
```

## Gated model policy

Hermes must not attempt to bypass Hugging Face access gates.

For gated models:

1. Report the model as `gated`.
2. Provide the Hugging Face approval URL.
3. Wait for user approval on the Hugging Face website.
4. Verify token access after approval.
5. Only then download.

Default policy:

| Model type | Auto-download? | If gated? |
|---|---:|---|
| Small open embeddings | Allowed after policy confidence | Ask once |
| Rerankers | Allowed after policy confidence | Ask once |
| Small/medium GGUF LLMs | Ask first initially | Ask first |
| Huge archive models | Always ask first | Always ask first |
| Unclear/custom license | Never auto-download | Ask first |

## Category taxonomy

Top-level library categories:

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

`RAG/` is a workflow area, not the default weight folder for embedding/reranker models:

```text
RAG/Bundles/
RAG/Pipelines/
RAG/Experimental/
```

`Archive-Huge/` mirrors model-family categories and also includes:

```text
Archive-Huge/Datasets-Model-Assets/
Archive-Huge/Research-Snapshots/
Archive-Huge/Unsorted-Pending-Review/
```

## Cadence

| Cadence | Purpose |
|---|---|
| Daily | Major release radar only; alert only if genuinely high signal. |
| Weekly | Full model research digest across categories. |
| Monthly | Installed library review, replacements, archive/delete suggestions. |

## Research report format

Each candidate should include:

```text
Model: org/model
Category: LLM / Coding / Embeddings / etc.
Recommendation: Download Now / Watch / Archive / Ignore
Suggested folder: /Users/davideddy/mnt/models/<Category>/<ModelName>
Gated: false/manual/auto/unknown
License: ...
Why it matters:
Hardware fit:
Tooling/format signal:
Risks:
Next action:
```
