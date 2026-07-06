# Local Voice Ingestion / 本地语音入口

Living Mirror can ingest voice records by turning local audio into transcript files before self-distillation.

Publicly, this module is called **Local Voice Ingestion**. It does not bundle a speech model and does not hardcode one in the skill. The user chooses a local ASR model at runtime with `--model` or `LIVING_MIRROR_ASR_MODEL`.

## What It Produces

The batch script writes:

- `transcripts.jsonl`: machine-readable transcript records
- `summary.md`: human-readable transcript review
- `errors.jsonl`: failed files with error messages
- `manifest.json`: resume/cache state
- `run_summary.json`: counts, model metadata, elapsed time, and output paths

These files can be merged into `distillation/raw/merged.jsonl` with `merge_messages.py`.

## Usage

PowerShell:

```powershell
$env:LIVING_MIRROR_ASR_MODEL = "your-local-asr-model-name-or-path"
python scripts/probe_local_voice_env.py
python scripts/batch_transcribe_local_voice.py `
  --input "C:\path\to\audio" `
  --output "distillation\raw\voice-transcripts" `
  --recursive `
  --resume
```

Bash:

```bash
LIVING_MIRROR_ASR_MODEL="<your-local-asr-model-name-or-path>" \
python scripts/batch_transcribe_local_voice.py \
  --input raw/audio \
  --output distillation/raw/voice-transcripts \
  --recursive \
  --resume
```

## Privacy

Keep raw recordings and transcripts out of Git. Treat voice data as sensitive personal material.

