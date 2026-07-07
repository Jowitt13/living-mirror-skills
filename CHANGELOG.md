# Changelog

## v0.6.1 - 2026-07-08

Local Voice Ingestion: added a WeChat-SILK specialization with multiprocess decoding.

Added:

- `scripts/batch_transcribe_wechat_silk.py` in every package: transcribes WeChat `.silk` voice exports with a user-supplied local FunASR model.
- Performance design: `pilk` decodes SILK directly to 16 kHz (no manual resampling), all SILK files are pre-decoded on CPU cores in parallel, then a single process runs batched FunASR inference so the GPU is fully saturated (utilization ~9% -> ~100%).
- Filename parsing recovers `timestamp` / `sender_wxid`; `--me-wxid` infers `is_self`.
- Output shape matches `batch_transcribe_local_voice.py`: `transcripts.jsonl` + `manifest.json` (resume) + `summary.md` + `run_summary.json`.

Docs:

- `docs/local-voice-ingestion.md` now documents the WeChat SILK path and the py3.13 install caveat (`pip install funasr --no-deps` to bypass the `editdistance` build failure).
- README and README.zh-CN add a "WeChat SILK Voices (multiprocess-optimized)" subsection.
- `packages/workbuddy/SKILL.md` Local Voice Ingestion section references the SILK script.

## v0.6 - 2026-07-07

Living Mirror v0.6 unifies the dynamic mirror upgrades into one named framework version.

Added:

- Human-understanding dimensions for body/energy, shame/defense, desire-action gap, aesthetic order, role switching, agency, attention rhythm, meaning narrative, boundaries, and repair.
- Context weight for time, relationship, body, environment, event, and medium.
- Three-part confidence: evidence, interpretation, and stability.
- Fact / interpretation / temporary-name separation.
- User-language priority layer.
- Counter-evidence index with `CE-XXX` entries.
- Machine-readable insight schema: `references/insight-schema-v0.6.json`.
- Quality check script: `scripts/quality_check_distillation.py`.
- Synthetic demo self portrait: `docs/demo-v0.6-self-portrait.md`.
- Visual templates for relationship maps, timelines, evidence ledgers, context dashboards, and social cards.

Changed:

- README and README.zh-CN now describe v0.6 as the current framework layer.
- Skill reference routing now points agents to the v0.6 schema and quality checker.
- Self-portrait and theme-report templates now require counter-evidence and user-language fields.

## v0.5 - 2026-07-07

Added optional sensitive theme 16: intimacy / sexuality expression. This theme is off by default and requires explicit user consent.

## v0.4 - 2026-07-07

Expanded longitudinal distillation from 10 themes to 15 themes by adding food preferences, lifestyle habits, thinking style, worldview/lifeview, and hobbies.

