# Self Distillation Skills

> Turn local chat logs, notes, and journals into an evidence-backed self portrait.

Self Distillation Skills is a reusable skill pack for building a "self-distillation memory system": a method for reading your own fragmented records, such as chat histories, flomo notes, journals, and voice transcripts, and producing a self portrait that is evidence-backed, confidence-scored, contradiction-aware, correctable, and versioned.

It is not a personality clone. It is a mirror that can revise itself.

## What This Is

Most personal-memory projects try to make an assistant "sound like you" or remember more facts. This project takes a different route:

- It extracts patterns, values, changes, conflicts, and recurring behaviors from your own records.
- It requires evidence for every insight.
- It marks uncertainty instead of pretending to know.
- It keeps contradictions instead of flattening them.
- It lets the user overturn the analysis through a Correction layer.
- It keeps versions so the portrait can evolve and roll back.

The result is a living self portrait, not a fixed label.

## What It Is Useful For

Use this skill pack when you want to:

- Understand yourself from years of real messages, notes, and journals.
- Build a monthly or quarterly self portrait.
- Analyze relationship patterns without relying on vague impressions.
- Track how values, goals, emotions, habits, speech style, and conflicts evolve.
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
   Part A: five self-memory dimensions
   Part B: five personality layers
   Evidence grading + CONFLICT tracking + Correction + versioning

3. Output layer
   Self portrait + conflicts + corrections + changelog + manifest
```

### Part A: Five Self-Memory Dimensions

1. Values and emotions
2. Behavior and decision patterns
3. Relationships
4. Goals and direction
5. Personal history and growth timeline

### Part B: Five Personality Layers

1. Hard rules
2. Identity
3. Speaking style
4. Emotional patterns
5. Interpersonal behavior

## The Four Safety Mechanisms

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

## Three Platform Versions

This repository ships three ready-to-use versions of the same framework.

| Version | Path | Best For |
|---|---|---|
| WorkBuddy | `packages/workbuddy/` | WorkBuddy users who want platform metadata such as `version`, `updated`, `platforms`, and `triggers`. |
| Codex | `packages/codex/` | Codex skill installation. Uses Codex-compatible frontmatter with only `name` and `description`. |
| Claude Code | `packages/claude-code/` | Claude Code users. Includes a small `README.md` and Claude-oriented trigger guidance. |

All three versions share the same references and scripts.

## Installation

### Codex

Copy the Codex package into your Codex skills directory:

```powershell
Copy-Item -Path .\packages\codex -Destination "$env:USERPROFILE\.codex\skills\self-distillation" -Recurse -Force
```

Then invoke it by asking Codex for self distillation, for example:

```text
Use $self-distillation to analyze my local chat records and build a monthly self portrait.
```

### Claude Code

Copy the Claude Code package into your Claude skills directory:

```powershell
Copy-Item -Path .\packages\claude-code -Destination "$env:USERPROFILE\.claude\skills\self-distillation" -Recurse -Force
```

Then ask Claude Code:

```text
Use self-distillation to distill these JSONL chat records. Verify sender before quoting anything.
```

### WorkBuddy

Copy the WorkBuddy package into your WorkBuddy skills directory:

```powershell
Copy-Item -Path .\packages\workbuddy -Destination "$env:USERPROFILE\.workbuddy\skills\self-distillation" -Recurse -Force
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

Merge text messages and voice transcripts:

```bash
python scripts/merge_messages.py --messages raw/messages.jsonl --voice raw/voice_transcriptions.json --output raw/merged.jsonl --sort
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
6. Run a second pass by the 10 longitudinal themes.
7. Verify sender for every key quote.
8. Ask the user to review each theme report.
9. Merge the reports into `self-portrait-YYYY-MM.md`.
10. Update `manifest.json`, `changelog.md`, `conflicts.md`, and `corrections.md`.

## Repository Structure

```text
.
├── packages/
│   ├── workbuddy/
│   ├── codex/
│   └── claude-code/
├── docs/
│   ├── examples.md
│   ├── privacy-and-safety.md
│   └── platform-notes.md
├── LICENSE
└── README.md
```

Each package contains:

```text
SKILL.md
agents/openai.yaml
references/
scripts/
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
