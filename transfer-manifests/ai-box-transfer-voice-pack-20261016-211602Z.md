# AI Box Transfer Manifest: voice-pack

Generated: 20261016-211602Z
Destination root placeholder: `/mnt/ai-box/models`
Models: `10`
Total estimated transfer size: `41.74 GiB`

## Transfer checklist

- [ ] Confirm available free space on the AI box.
- [ ] Copy one model at a time or one bundle at a time.
- [ ] Preserve directory structure under the AI-box model root.
- [ ] Verify `_hermes_model_metadata.json` exists after copy.
- [ ] Verify approximate size and payload file count after copy.
- [ ] Run the AI-box runtime benchmark/smoke test.
- [ ] Record result back into this repo.

## Models

| Model | Repo | Size | Payload files | AI-box runtime hint | Source | Suggested destination |
|---|---|---:|---:|---|---|---|
| `Speech-TTS/Kokoro-82M` | `hexgrad/Kokoro-82M` | 0.34 GiB | 73 | model-specific TTS package (kokoro / chatterbox / qwen-tts / vibevoice / voxcpm) on AI box | `/Users/davideddy/mnt/models/Speech-TTS/Kokoro-82M` | `/mnt/ai-box/models/Speech-TTS/Kokoro-82M` |
| `Speech-TTS/Qwen3-TTS-12Hz-1.7B-CustomVoice` | `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice` | 4.21 GiB | 14 | model-specific TTS package (kokoro / chatterbox / qwen-tts / vibevoice / voxcpm) on AI box | `/Users/davideddy/mnt/models/Speech-TTS/Qwen3-TTS-12Hz-1.7B-CustomVoice` | `/mnt/ai-box/models/Speech-TTS/Qwen3-TTS-12Hz-1.7B-CustomVoice` |
| `Speech-TTS/Qwen3-TTS-12Hz-1.7B-Base` | `Qwen/Qwen3-TTS-12Hz-1.7B-Base` | 4.23 GiB | 14 | model-specific TTS package (kokoro / chatterbox / qwen-tts / vibevoice / voxcpm) on AI box | `/Users/davideddy/mnt/models/Speech-TTS/Qwen3-TTS-12Hz-1.7B-Base` | `/mnt/ai-box/models/Speech-TTS/Qwen3-TTS-12Hz-1.7B-Base` |
| `Speech-TTS/chatterbox` | `ResembleAI/chatterbox` | 12.91 GiB | 19 | model-specific TTS package (kokoro / chatterbox / qwen-tts / vibevoice / voxcpm) on AI box | `/Users/davideddy/mnt/models/Speech-TTS/chatterbox` | `/mnt/ai-box/models/Speech-TTS/chatterbox` |
| `Speech-TTS/VibeVoice-1.5B` | `microsoft/VibeVoice-1.5B` | 5.04 GiB | 10 | model-specific TTS package (kokoro / chatterbox / qwen-tts / vibevoice / voxcpm) on AI box | `/Users/davideddy/mnt/models/Speech-TTS/VibeVoice-1.5B` | `/mnt/ai-box/models/Speech-TTS/VibeVoice-1.5B` |
| `Speech-TTS/VoxCPM2` | `openbmb/VoxCPM2` | 4.62 GiB | 10 | model-specific TTS package (kokoro / chatterbox / qwen-tts / vibevoice / voxcpm) on AI box | `/Users/davideddy/mnt/models/Speech-TTS/VoxCPM2` | `/mnt/ai-box/models/Speech-TTS/VoxCPM2` |
| `Speech-STT/parakeet-tdt-0.6b-v3` | `nvidia/parakeet-tdt-0.6b-v3` | 5.34 GiB | 13 | NVIDIA NeMo on AI box | `/Users/davideddy/mnt/models/Speech-STT/parakeet-tdt-0.6b-v3` | `/mnt/ai-box/models/Speech-STT/parakeet-tdt-0.6b-v3` |
| `Speech-STT/Qwen3-ASR-1.7B` | `Qwen/Qwen3-ASR-1.7B` | 4.38 GiB | 13 | faster-whisper preferred; transformers fallback | `/Users/davideddy/mnt/models/Speech-STT/Qwen3-ASR-1.7B` | `/mnt/ai-box/models/Speech-STT/Qwen3-ASR-1.7B` |
| `Speech-STT/Nemotron-3-Diarization` | `nvidia/Nemotron-3-Diarization` | 0.66 GiB | 17 | NeMo / ONNX runtime on AI box (tiny; CPU is fine) | `/Users/davideddy/mnt/models/Speech-STT/Nemotron-3-Diarization` | `/mnt/ai-box/models/Speech-STT/Nemotron-3-Diarization` |
| `Speech-STT/silero-vad` | `onnx-community/silero-vad` | 0.01 GiB | 12 | NeMo / ONNX runtime on AI box (tiny; CPU is fine) | `/Users/davideddy/mnt/models/Speech-STT/silero-vad` | `/mnt/ai-box/models/Speech-STT/silero-vad` |

## Per-model verification notes

### `Speech-TTS/Kokoro-82M`

- Source: `/Users/davideddy/mnt/models/Speech-TTS/Kokoro-82M`
- Repo: `hexgrad/Kokoro-82M`
- Expected size: `0.34 GiB`
- Expected payload files excluding `.cache`: `73`
- Metadata: `_hermes_model_metadata.json` should exist in the destination folder.
- Runtime hint: model-specific TTS package (kokoro / chatterbox / qwen-tts / vibevoice / voxcpm) on AI box
- Verification: Compare source and AI-box copy: size ≈ 0.34 GiB, payload files = 73, metadata file present

### `Speech-TTS/Qwen3-TTS-12Hz-1.7B-CustomVoice`

- Source: `/Users/davideddy/mnt/models/Speech-TTS/Qwen3-TTS-12Hz-1.7B-CustomVoice`
- Repo: `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice`
- Expected size: `4.21 GiB`
- Expected payload files excluding `.cache`: `14`
- Metadata: `_hermes_model_metadata.json` should exist in the destination folder.
- Runtime hint: model-specific TTS package (kokoro / chatterbox / qwen-tts / vibevoice / voxcpm) on AI box
- Verification: Compare source and AI-box copy: size ≈ 4.21 GiB, payload files = 14, metadata file present

### `Speech-TTS/Qwen3-TTS-12Hz-1.7B-Base`

- Source: `/Users/davideddy/mnt/models/Speech-TTS/Qwen3-TTS-12Hz-1.7B-Base`
- Repo: `Qwen/Qwen3-TTS-12Hz-1.7B-Base`
- Expected size: `4.23 GiB`
- Expected payload files excluding `.cache`: `14`
- Metadata: `_hermes_model_metadata.json` should exist in the destination folder.
- Runtime hint: model-specific TTS package (kokoro / chatterbox / qwen-tts / vibevoice / voxcpm) on AI box
- Verification: Compare source and AI-box copy: size ≈ 4.23 GiB, payload files = 14, metadata file present

### `Speech-TTS/chatterbox`

- Source: `/Users/davideddy/mnt/models/Speech-TTS/chatterbox`
- Repo: `ResembleAI/chatterbox`
- Expected size: `12.91 GiB`
- Expected payload files excluding `.cache`: `19`
- Metadata: `_hermes_model_metadata.json` should exist in the destination folder.
- Runtime hint: model-specific TTS package (kokoro / chatterbox / qwen-tts / vibevoice / voxcpm) on AI box
- Verification: Compare source and AI-box copy: size ≈ 12.91 GiB, payload files = 19, metadata file present

### `Speech-TTS/VibeVoice-1.5B`

- Source: `/Users/davideddy/mnt/models/Speech-TTS/VibeVoice-1.5B`
- Repo: `microsoft/VibeVoice-1.5B`
- Expected size: `5.04 GiB`
- Expected payload files excluding `.cache`: `10`
- Metadata: `_hermes_model_metadata.json` should exist in the destination folder.
- Runtime hint: model-specific TTS package (kokoro / chatterbox / qwen-tts / vibevoice / voxcpm) on AI box
- Verification: Compare source and AI-box copy: size ≈ 5.04 GiB, payload files = 10, metadata file present

### `Speech-TTS/VoxCPM2`

- Source: `/Users/davideddy/mnt/models/Speech-TTS/VoxCPM2`
- Repo: `openbmb/VoxCPM2`
- Expected size: `4.62 GiB`
- Expected payload files excluding `.cache`: `10`
- Metadata: `_hermes_model_metadata.json` should exist in the destination folder.
- Runtime hint: model-specific TTS package (kokoro / chatterbox / qwen-tts / vibevoice / voxcpm) on AI box
- Verification: Compare source and AI-box copy: size ≈ 4.62 GiB, payload files = 10, metadata file present

### `Speech-STT/parakeet-tdt-0.6b-v3`

- Source: `/Users/davideddy/mnt/models/Speech-STT/parakeet-tdt-0.6b-v3`
- Repo: `nvidia/parakeet-tdt-0.6b-v3`
- Expected size: `5.34 GiB`
- Expected payload files excluding `.cache`: `13`
- Metadata: `_hermes_model_metadata.json` should exist in the destination folder.
- Runtime hint: NVIDIA NeMo on AI box
- Verification: Compare source and AI-box copy: size ≈ 5.34 GiB, payload files = 13, metadata file present

### `Speech-STT/Qwen3-ASR-1.7B`

- Source: `/Users/davideddy/mnt/models/Speech-STT/Qwen3-ASR-1.7B`
- Repo: `Qwen/Qwen3-ASR-1.7B`
- Expected size: `4.38 GiB`
- Expected payload files excluding `.cache`: `13`
- Metadata: `_hermes_model_metadata.json` should exist in the destination folder.
- Runtime hint: faster-whisper preferred; transformers fallback
- Verification: Compare source and AI-box copy: size ≈ 4.38 GiB, payload files = 13, metadata file present

### `Speech-STT/Nemotron-3-Diarization`

- Source: `/Users/davideddy/mnt/models/Speech-STT/Nemotron-3-Diarization`
- Repo: `nvidia/Nemotron-3-Diarization`
- Expected size: `0.66 GiB`
- Expected payload files excluding `.cache`: `17`
- Metadata: `_hermes_model_metadata.json` should exist in the destination folder.
- Runtime hint: NeMo / ONNX runtime on AI box (tiny; CPU is fine)
- Verification: Compare source and AI-box copy: size ≈ 0.66 GiB, payload files = 17, metadata file present

### `Speech-STT/silero-vad`

- Source: `/Users/davideddy/mnt/models/Speech-STT/silero-vad`
- Repo: `onnx-community/silero-vad`
- Expected size: `0.01 GiB`
- Expected payload files excluding `.cache`: `12`
- Metadata: `_hermes_model_metadata.json` should exist in the destination folder.
- Runtime hint: NeMo / ONNX runtime on AI box (tiny; CPU is fine)
- Verification: Compare source and AI-box copy: size ≈ 0.01 GiB, payload files = 12, metadata file present
