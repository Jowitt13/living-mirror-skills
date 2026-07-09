---
name: living-mirror
description: 见己镜 Living Mirror v0.9：本地优先的自我蒸馏、数据体检、隐私脱敏、行动转译、关系场景和社区模板系统。从聊天记录、flomo、日记、语音转录等碎片数据中生成带证据、三段置信度、情境权重、反证索引、用户语言优先、允许矛盾、可被推翻、可回滚的自画像。Use when the user asks to 蒸馏自己, build a self portrait, analyze chat records, understand themselves, run monthly distillation, start without enough data, diagnose local inputs, redact a public artifact, create review questions, turn insights into 7-day experiments or scripts, build relationship maps, export Obsidian/Notion/PDF/social templates, or maintain Living Mirror community templates.
---

# 见己镜 Living Mirror v0.9

Living Mirror turns local fragments into a verifiable, correctable, living self portrait. It is not a personality clone and not a therapy replacement. It is a local-first mirror that keeps evidence, uncertainty, contradiction, correction, action, and privacy in the same system.

## Version Stack

- **v0.4**: expands longitudinal distillation from 10 themes to 15 themes.
- **v0.5**: adds optional sensitive theme 16: intimacy/sexuality expression, off by default and requiring explicit consent.
- **v0.6**: adds dynamic mirror rules: human-understanding dimensions, context weight, three-part confidence, fact/interpretation/name separation, counter-evidence, and user-language priority.
- **v0.7**: adds onboarding, cold-start interview, data diagnosis, consent scope, privacy levels, redaction, and forgetting/deletion rules.
- **v0.8**: adds action translation, relationship maps, repair/boundary scripts, and review queues.
- **v0.9**: adds community templates, export packs, public case-study shape, and productized starter workflows.

## Non-Negotiable Rules

1. Evidence first: every important insight needs `verbatim`, `artifact`, or clearly marked `impression`.
2. Verify sender before any claim about who said or did something.
3. Do not turn a temporary state into a permanent identity claim.
4. Keep contradictions visible in `conflicts.md`; do not flatten them into neat prose.
5. If the user says "I am not like this", write a Correction and update the portrait.
6. Prefer the user's own language over external labels.
7. Keep raw data local by default; never commit private records or real chat exports.
8. Sensitive theme 16 is opt-in. If the user hesitates, skip it without pressure.
9. Public outputs must be redacted and should avoid raw private quotes.
10. Local Voice Ingestion does not bundle or hardcode a speech model; the user provides one at runtime.

## Choose the Right Mode

Use `references/onboarding-and-data-diagnosis.md` when the user is starting, lacks clean data, or needs a data health report.

| Mode | Use when |
|---|---|
| `light_start` | Little/no prepared data; run a cold-start interview and mark insights as pending. |
| `standard` | One or two usable data sources; produce a focused monthly/quarterly portrait. |
| `deep` | Years of records; run time-batch + theme-based longitudinal distillation. |
| `repair_only` | One relationship conflict or communication loop matters most. |
| `public_share` | The user wants GitHub/social/blog/demo output. |

## Standard Workflow

1. **Diagnose inputs**: run `scripts/diagnose_distillation_inputs.py <workspace-or-raw-folder>` when files exist.
2. **Set consent scope**: read `references/privacy-consent-redaction.md`; decide source, time, relationship, theme, and output scope.
3. **Prepare data**: put records under `distillation/raw/`; use Local Voice Ingestion for audio if needed; merge with `scripts/merge_messages.py`.
4. **Review existing memory**: read `conflicts.md`, `corrections.md`, `manifest.json`, and prior self portraits.
5. **First pass by time**: use `scripts/filter_by_time.py`; write a batch report from `references/batch-report-template.md`.
6. **Second pass by theme**: use `scripts/filter_by_theme.py`; write theme reports from `references/theme-report-template.md`.
7. **Apply dynamic rules**: read `references/dynamic-mirror-rules.md`; include state/trait, context weight, three-part confidence, fact/interpretation/name, falsifiability, counter-evidence, and user language.
8. **Merge portrait**: use `references/self-portrait-template.md`; update conflicts, corrections, changelog, manifest, and archive.
9. **Quality check**: run `scripts/quality_check_distillation.py --input <artifact>`.
10. **User review**: run `scripts/make_review_queue.py --input <artifact>` and ask the user to confirm, reject, rename, or add counter-evidence.
11. **Translate to action**: when useful, read `references/action-translation.md` and produce a 7-day experiment, script, decision lens, or environment adjustment.
12. **Export or publish**: for public/shareable outputs, run `scripts/redact_public_artifact.py`; read `references/community-template-kit.md` and use templates in `assets/templates/`.

## Longitudinal Themes

1. Values and emotions
2. Behavior and decision patterns
3. Partner / close relationship
4. Family relationship
5. Friend relationship
6. Goals and direction
7. Personal history timeline
8. Speaking style evolution
9. Conflict handling evolution
10. Consumption values
11. Food preferences
12. Lifestyle habits
13. Thinking style
14. Worldview and lifeview
15. Hobbies and interest system
16. Intimacy / sexuality expression, optional and consent-gated

## Reference Routing

- Starting or diagnosing data: `references/onboarding-and-data-diagnosis.md`
- Consent, privacy, redaction, deletion: `references/privacy-consent-redaction.md`
- Evidence and confidence: `references/evidence-grading.md`
- Conflict tracking: `references/conflict-tracker.md`
- User corrections: `references/correction-rules.md`
- Sender verification: `references/sender-verification.md`
- Keyword search limits: `references/keyword-usage.md`
- Special periods: `references/special-period.md`
- Dynamic mirror rules: `references/dynamic-mirror-rules.md`
- Structured insight fields: `references/insight-schema-v0.9.json`
- Action translation: `references/action-translation.md`
- Relationship maps and repair: `references/relationship-pack.md`
- Community templates and exports: `references/community-template-kit.md`
- Full/batch/theme templates: `references/self-portrait-template.md`, `references/batch-report-template.md`, `references/theme-report-template.md`

## Script Routing

- Initialize workspace: `scripts/init_distillation.py <workspace>`
- Diagnose inputs: `scripts/diagnose_distillation_inputs.py <workspace-or-raw-folder>`
- Transcribe local audio: `scripts/batch_transcribe_local_voice.py --input raw/audio --output raw/voice-transcripts --model <local-asr-model-or-path>`
- Merge text and voice transcripts: `scripts/merge_messages.py`
- Generate stats: `scripts/stats_overview.py`
- Filter by time/theme: `scripts/filter_by_time.py`, `scripts/filter_by_theme.py`
- Verify sender: `scripts/verify_sender.py`
- Quality check: `scripts/quality_check_distillation.py`
- Build user review queue: `scripts/make_review_queue.py`
- Redact public artifacts: `scripts/redact_public_artifact.py`

## Output Discipline

- Use UTF-8.
- Do not hardcode real names, relationship names, chat names, or local paths in reusable templates.
- Quote sparingly. Prefer redacted paraphrase when direct quotes are not necessary.
- Keep `fact`, `interpretation`, and `temporary_name` separate.
- For public examples, use synthetic or redacted material only.
- End important reports with review questions and next actions.

