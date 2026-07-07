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

## WeChat SILK Voices (FunASR, multiprocess-optimized)

WeChat exports voice messages as `.silk` files (SILK codec), which no ASR model can read directly. The `batch_transcribe_wechat_silk.py` script in every package is the WeChat-specific specialization of this module:

- Decodes SILK with `pilk` directly to 16 kHz PCM (`pilk.decode(silk, pcm, 16000)`) — no manual resampling.
- **Multiprocess pre-decode**: all SILK files are decoded to WAV on CPU cores in parallel, so the GPU never waits on the CPU decode stage.
- **Single-process batched inference**: the main process feeds batches of WAV paths to `model.generate(input=[...])`, saturating the GPU (utilization rises from ~9% to ~100%).

```bash
LIVING_MIRROR_ASR_MODEL="paraformer-zh" \
  python scripts/batch_transcribe_wechat_silk.py \
  --input "D:/wechat/voice" --output raw/voice-transcripts --resume
```

It parses the WeChat SILK filename convention (`<seq>_<sender_wxid>_<receiver_wxid>_<unk>_<timestamp10>_<ms>.silk`) to recover `timestamp` and `sender_wxid`; pass `--me-wxid` to infer `is_self` automatically. Output is `transcripts.jsonl` + `manifest.json` (resume state) + `summary.md` + `run_summary.json`, the same shape as `batch_transcribe_local_voice.py`.

Environment caveats (Python 3.13 + Windows): FunASR depends on `editdistance`, which has no prebuilt wheel for py3.13 and fails to compile, rolling back the whole install. Fix: install all other deps first, then `pip install funasr --no-deps` (`editdistance` is only used for WER scoring, not transcription). Also install `torchaudio` (FunASR imports it at top level).

## Privacy

Keep raw recordings and transcripts out of Git. Treat voice data as sensitive personal material.

