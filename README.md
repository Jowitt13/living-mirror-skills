# Living Mirror Skills v0.6

> A verifiable mirror for your inner life: turn local chat logs, notes, and journals into an evidence-backed self portrait.

Language: English | [简体中文](README.zh-CN.md)

**Living Mirror** is the public name for this self-distillation skill pack. It reads your fragmented records, such as chat histories, flomo notes, journals, and voice transcripts, and helps an AI agent produce a self portrait that is evidence-backed, confidence-scored, contradiction-aware, correctable, and versioned.

It is not a personality clone. It is a mirror that can revise itself, admit uncertainty, and learn from correction.

Current framework version: **v0.6**.

## Local Voice Ingestion

Living Mirror can also prepare voice records before self-distillation. The **Local Voice Ingestion** module turns local audio, including exported WeChat voice messages, meeting recordings, voice notes, and listening-practice files, into transcript artifacts.

The module does not bundle a speech model and does not hardcode one. Configure your own local ASR model at runtime with `--model` or `LIVING_MIRROR_ASR_MODEL`.

## Design Lineage

Living Mirror's architecture is an original integration with conceptual references to `yourself-skill`, `immortal-skill`, and `ex-skill`. The dual Self Memory + Persona structure, contradiction tracking, Correction layer, and evidence grading are credited in [Design Lineage](docs/design-lineage.md).

## What This Is

Most personal-memory projects try to make an assistant "sound like you" or remember more facts. This project takes a different route:

- It extracts patterns, values, changes, conflicts, and recurring behaviors from your own records.
- It requires evidence for every insight.
- It marks uncertainty instead of pretending to know.
- It keeps contradictions instead of flattening them.
- It lets the user overturn the analysis through a Correction layer.
- It keeps versions so the portrait can evolve and roll back.
- It separates stable traits from temporary states, relationship-triggered patterns, and special-period reactions.
- It keeps counter-evidence visible instead of hiding exceptions inside prose.

The result is a living self portrait, not a fixed label.

## What It Is Useful For

Use this skill pack when you want to:

- Understand yourself from years of real messages, notes, and journals.
- Build a monthly or quarterly self portrait.
- Analyze relationship patterns without relying on vague impressions.
- Track how values, goals, emotions, habits, thinking style, lifestyle preferences, speech style, and conflicts evolve.
- Keep an evidence trail for every important insight.
- Avoid common AI analysis mistakes such as sender attribution errors, keyword overinterpretation, and special-period bias.
- Build a local-first personal memory workflow for Codex, Claude Code, or WorkBuddy.

## Who It Is For

This project is especially useful for:

- People who keep chat logs, notes, diaries, or voice transcripts and want reflective analysis.
- AI power users building a personal memory system.
- Therapists, coaches, researchers, or self-trackers who need evidence-aware qualitative summaries.
- Couples or close friends analyzing long-term communication patterns, with consent and privacy boundaries.
- Developers packaging local-first AI workflows into reusable skills.

It is not a replacement for therapy, medical care, legal advice, or crisis support. It is a structured reflection tool.

## Core Method

The framework has three layers:

```text
1. Data collection layer
   Chat logs + notes + journals -> unified fragments

2. Distillation layer
   Part A: 11 self-memory dimensions
   Part B: five personality layers
   Evidence grading + CONFLICT tracking + Correction + versioning + v0.6 dynamic mirror rules

3. Output layer
   Self portrait + conflicts + corrections + changelog + manifest
```

### Part A: 11 Self-Memory Dimensions

1. Values and emotions
2. Behavior and decision patterns
3. Relationships
4. Goals and direction
5. Personal history and growth timeline
6. Food preferences
7. Lifestyle habits
8. Thinking style
9. Worldview and lifeview
10. Hobbies and interest system
11. Intimacy / sexuality expression (optional sensitive dimension; explicit user consent required)

### v0.4 / v0.5 Framework Extensions

v0.4 expands the longitudinal map from 10 themes to 15 by adding food preferences, lifestyle habits, thinking style, worldview/lifeview, and hobbies.

v0.5 adds a 16th optional sensitive theme: intimacy / sexuality expression. This theme is off by default, must be explicitly authorized by the user, and can be skipped without affecting the main workflow. When enabled, it requires stricter privacy handling, redacted quotes, sender verification, and no moralizing or pathologizing.

### v0.6 Dynamic Mirror Rules

Living Mirror v0.6 unifies the dynamic judgment layer into a named framework version. Important insights should state:

- Which human-understanding dimension is being used: body/energy, shame/defense, desire-action gap, aesthetic order, role switching, agency, attention rhythm, meaning narrative, boundaries, or repair.
- Whether the pattern is a stable trait, stage state, special-period response, relationship-triggered pattern, or pending pattern.
- Which context shaped the evidence: time, relationship, body/energy state, environment, event, or medium.
- Three confidence scores: evidence confidence, interpretation confidence, and stability confidence.
- The difference between fact, interpretation, and a temporary pattern name.
- What would overturn or weaken the insight.
- Which counter-evidence entries challenge the insight.
- The user's own language for the pattern, when available.

This makes the framework better at describing living people instead of freezing them into labels.

v0.6 also adds a machine-readable schema, a quality-check script, a synthetic demo artifact, visual templates, and this repository changelog.

### Part B: Five Personality Layers

1. Hard rules
2. Identity
3. Speaking style
4. Emotional patterns
5. Interpersonal behavior

## Safety Mechanisms

### Evidence Grading

Every insight must carry evidence:

| Level | Meaning |
|---|---|
| `verbatim` | Direct quote from source data. Sender must be verified. |
| `artifact` | Statistics, files, timestamps, message density, or behavior traces. |
| `impression` | The distiller's interpretation. Lowest confidence and never enough alone. |

Confidence is marked as `high`, `medium`, or `low`.

### CONFLICT Tracking

Contradictions are not forced into one neat conclusion. They are recorded in `conflicts.md`:

- `green / resolved`
- `yellow / pending verification`
- `red / conflict intensified`

### Correction Layer

When the user says "this is not me", the system corrects immediately:

- Keep the original insight.
- Mark it as overturned.
- Record the reason in `corrections.md`.
- Update the self portrait.

### Incremental Merge and Versioning

Monthly updates do not overwrite the old portrait. New insights, revisions, conflicts, corrections, and metadata are versioned through `manifest.json`, `changelog.md`, and `archive/`.

### State/Trait and Falsifiability

The dynamic mirror rules prevent overclaiming. A powerful quote can make evidence confidence high, while stability confidence remains low. Every important insight should say what context shaped it and what future evidence or user correction would overturn it.

### Counter-Evidence Index

Important insights can carry `CE-XXX` entries. Each entry links a claim to an exception, contrary artifact, user correction, or alternative explanation, then marks whether it weakens, narrows, overturns, or creates a CONFLICT for the insight.

### Schema and Quality Check

Each package includes:

```text
references/insight-schema-v0.6.json
scripts/quality_check_distillation.py
```

Run the quality checker on a Markdown self portrait or a structured JSON insight file:

```bash
python scripts/quality_check_distillation.py --input self-portrait-YYYY-MM.md --output quality-report.md
python scripts/quality_check_distillation.py --input insights.json --json quality-findings.json
```

## Optional Outputs

Besides the full self portrait, the skill can produce:

- A short portrait with 5 to 9 evidence-backed bullets.
- A relationship map organized by relationship type or a consented specific relationship.
- A change timeline showing when patterns appeared, intensified, softened, or were corrected.
- A validation question list for the user to confirm, reject, or rename low-confidence insights.
- An evidence ledger with supporting evidence, counter-evidence, confidence, and status.
- A context dashboard showing which contexts are shaping the current portrait.
- A repair map for conflict, apology, re-contact, and non-repair patterns.
- A naming glossary that preserves the user's own phrases before external labels.

## Three Platform Versions

This repository ships three ready-to-use versions of the same framework.

| Version | Path | Best For |
|---|---|---|
| WorkBuddy | `packages/workbuddy/` | WorkBuddy users who want platform metadata such as `version`, `updated`, `platforms`, and `triggers`. |
| Codex | `packages/codex/` | Codex skill installation. Uses Codex-compatible frontmatter with only `name` and `description`. |
| Claude Code | `packages/claude-code/` | Claude Code users. Includes a small `README.md` and Claude-oriented trigger guidance. |

All three versions share the same references and scripts, including the local voice-ingestion utilities.

## Installation

### Codex

Copy the Codex package into your Codex skills directory:

```powershell
Copy-Item -Path .\packages\codex -Destination "$env:USERPROFILE\.codex\skills\living-mirror" -Recurse -Force
```

Then invoke it by asking Codex for self distillation, for example:

```text
Use $living-mirror to analyze my local chat records and build a monthly self portrait.
```

### Claude Code

Copy the Claude Code package into your Claude skills directory:

```powershell
Copy-Item -Path .\packages\claude-code -Destination "$env:USERPROFILE\.claude\skills\living-mirror" -Recurse -Force
```

Then ask Claude Code:

```text
Use living-mirror to distill these JSONL chat records. Verify sender before quoting anything.
```

### WorkBuddy

Copy the WorkBuddy package into your WorkBuddy skills directory:

```powershell
Copy-Item -Path .\packages\workbuddy -Destination "$env:USERPROFILE\.workbuddy\skills\living-mirror" -Recurse -Force
```

Use natural triggers such as:

- `蒸馏自己`
- `自画像`
- `分析我的聊天记录`
- `月度蒸馏`
- `self-distillation`

## Basic Usage

Initialize a distillation workspace:

```bash
python scripts/init_distillation.py <workspace>
```

Transcribe local audio with a user-provided local ASR model:

```bash
LIVING_MIRROR_ASR_MODEL="<your-model-or-local-path>" python scripts/batch_transcribe_local_voice.py --input raw/audio --output raw/voice-transcripts --recursive --resume
```

Merge text messages and voice transcripts:

```bash
python scripts/merge_messages.py --messages raw/messages.jsonl --voice raw/voice-transcripts/transcripts.jsonl --output raw/merged.jsonl --sort
```

Generate descriptive statistics:

```bash
python scripts/stats_overview.py --input raw/merged.jsonl --output stats.md --json stats.json
```

Filter by time:

```bash
python scripts/filter_by_time.py --input raw/merged.jsonl --output batch-2025.jsonl --start 2025-01-01 --end 2025-12-31
```

Filter by theme:

```bash
python scripts/filter_by_theme.py --input raw/merged.jsonl --output values.jsonl --theme "价值观与情绪" --context 3
```

Verify sender before using a quote:

```bash
python scripts/verify_sender.py --input raw/merged.jsonl --keyword "自由" --start 2024-01-01 --context 2
```

## Recommended Workflow

1. Collect local records into `distillation/raw/`.
2. Merge messages and voice transcripts.
3. Generate a stats overview.
4. Review existing `conflicts.md` and `corrections.md`.
5. Run a first pass by time period.
6. Run a second pass by up to 16 longitudinal themes; theme 16 is optional and requires explicit user consent.
7. Verify sender for every key quote.
8. Apply v0.6 dynamic mirror rules: human-understanding dimension, state/trait, context weight, three-part confidence, fact/interpretation/name, counter-evidence index, user-language priority, and falsifiability.
9. Run `quality_check_distillation.py` for a structural pass.
10. Ask the user to review each theme report.
11. Merge the reports into `self-portrait-YYYY-MM.md`.
12. Update `manifest.json`, `changelog.md`, `conflicts.md`, and `corrections.md`.

## Repository Structure

```text
.
├── packages/
│   ├── workbuddy/
│   ├── codex/
│   └── claude-code/
├── docs/
│   ├── examples.md
│   ├── demo-v0.6-self-portrait.md
│   ├── visual-templates.md
│   ├── design-lineage.md
│   ├── local-voice-ingestion.md
│   ├── privacy-and-safety.md
│   └── platform-notes.md
├── LICENSE
├── CHANGELOG.md
└── README.md
```

Each package contains:

```text
SKILL.md
agents/openai.yaml
references/
scripts/
```

Key v0.6 files inside every package:

```text
references/insight-schema-v0.6.json
scripts/quality_check_distillation.py
```

## Privacy Principles

This skill is designed for local-first work:

- Keep raw data local by default.
- Do not upload private chat records unless you explicitly choose to.
- Quote sparingly.
- Prefer desensitized paraphrase when a direct quote is not necessary.
- Verify sender before making claims about who said or did something.

See [Privacy and Safety](docs/privacy-and-safety.md).

## Why Sender Verification Matters

One of the easiest ways for AI distillation to fail is to assign a quote or action to the wrong person. This framework treats sender verification as mandatory:

```text
Any claim about "who said what" or "who did what" must go back to the original data.
```

The package includes `scripts/verify_sender.py` and a dedicated reference document:

```text
references/sender-verification.md
```

## License

MIT License. See [LICENSE](LICENSE).


