# Living Mirror Skills v0.9

> Living Mirror v0.9 is a unified self-distillation core framework. Start with messy records or no records, turn them into a correctable self portrait, then translate insights into review questions, actions, relationship maps, and public-safe templates.

Language: English | [????](README.zh-CN.md)

**Living Mirror** is a reusable self-distillation skill pack for Codex, Claude Code, and WorkBuddy. It helps an AI agent read local fragments such as chat logs, flomo notes, journals, and voice transcripts, then produce a self portrait that is evidence-backed, confidence-scored, contradiction-aware, correctable, versioned, and privacy-conscious.

It is not a personality clone. It does not try to make an assistant "be you." It builds a mirror that can revise itself, keep counter-evidence, ask for review, and turn insight into small next actions.

Current **self-distillation core framework**: **v0.9**.

## What v0.9 Adds

Living Mirror v0.9 promotes the earlier onboarding, privacy, review, action, relationship, export, and community-template layers into the unified core framework. From v0.9 onward, new manifests, templates, self portraits, and framework documents should use `framework_version: "v0.9"`.

| Version | Focus | What it solves |
|---|---|---|
| v0.4 | Longitudinal expansion | Extends theme distillation from 10 to 15 themes. |
| v0.5 | Sensitive opt-in theme | Adds consent-gated theme 16 for intimacy/sexuality expression. |
| v0.6 | Dynamic mirror rules | Adds context weight, three-part confidence, fact/interpretation/name separation, user-language priority, and counter-evidence. |
| v0.7 | Onboarding and trust | Cold-start interview, data diagnosis, consent scope, privacy levels, redaction, forgetting/deletion rules. |
| v0.8 | Action and relationships | 7-day experiments, conversation/boundary/repair scripts, relationship maps, review queue. |
| v0.9 | Productization and community | Reusable templates, Obsidian/Notion/PDF/social export shapes, public case-study format, contribution checklist. |

## What This Is Useful For

- Understand yourself from years of messages, notes, journals, and voice transcripts.
- Start even without a perfect archive through a guided cold-start interview.
- Diagnose whether local data is ready for distillation.
- Build monthly, quarterly, or life-stage self portraits.
- Analyze relationship patterns with consent and privacy boundaries.
- Track values, goals, habits, thinking style, lifestyle, speech style, conflicts, and changes over time.
- Keep an evidence trail and counter-evidence index for important insights.
- Ask the user to confirm, reject, rename, or correct the mirror.
- Turn insights into 7-day experiments, scripts, decision lenses, and review loops.
- Produce redacted public-safe artifacts for GitHub, blogs, slides, or Xiaohongshu.

## Who It Is For

- People who keep chat logs, notes, diaries, or voice transcripts and want reflective analysis.
- People who do not have organized data yet but want a structured way to begin.
- AI power users building a local-first personal memory system.
- Coaches, researchers, self-trackers, and reflective practitioners who need evidence-aware qualitative summaries.
- Couples, friends, or collaborators exploring communication patterns with consent.
- Developers packaging personal AI workflows into reusable skills.

Living Mirror is not therapy, medical advice, legal advice, or crisis support. It is a structured reflection and self-understanding tool.

## Core Method

```text
1. Onboarding layer
   Cold-start interview + data diagnosis + consent scope

2. Data layer
   Chat logs + notes + journals + local voice transcripts -> unified fragments

3. Distillation layer
   Core framework v0.9: 16-theme longitudinal distillation
   Evidence grading + sender verification + CONFLICT + Correction
   Dynamic mirror rules: context, state/trait, three-part confidence, counter-evidence

4. Review and action layer
   Review queue + 7-day experiments + relationship maps + scripts

5. Export layer
   Private portrait + shareable summary + public redacted templates
```

## The 16 Themes

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

## Safety Mechanisms

- **Evidence grading**: `verbatim`, `artifact`, `impression`.
- **Sender verification**: claims about who said or did something must be checked against source data.
- **Three-part confidence**: evidence, interpretation, stability.
- **Context weight**: time, relationship, body, environment, event, medium.
- **State vs trait**: do not turn a temporary state into a permanent identity.
- **Counter-evidence index**: visible `CE-XXX` entries for exceptions and alternative explanations.
- **Correction layer**: user corrections are recorded and propagated.
- **Consent scope**: source, time, relationship, theme, and output scope.
- **Privacy levels**: private, shareable, public.
- **Public redaction**: no raw private logs or identifiable third-party material in public examples.

## Local Voice Ingestion

Living Mirror can prepare voice records before self-distillation. The **Local Voice Ingestion** module turns local audio, including exported WeChat voice messages, meeting recordings, voice notes, and listening-practice files, into transcript artifacts.

The module does not bundle a speech model and does not hardcode one. Configure your own local ASR model at runtime with `--model` or `LIVING_MIRROR_ASR_MODEL`.

```bash
python scripts/batch_transcribe_local_voice.py --input raw/audio --output raw/voice-transcripts --recursive --resume --model <local-asr-model-or-path>
```

## Three Platform Versions

| Version | Path | Best for |
|---|---|---|
| WorkBuddy | `packages/workbuddy/` | WorkBuddy users who want platform metadata and natural Chinese triggers. |
| Codex | `packages/codex/` | Codex skill installation with minimal frontmatter. |
| Claude Code | `packages/claude-code/` | Claude Code users who want the same framework and scripts. |

All three packages share the same v0.9 framework, references, scripts, and templates.

## Quick Start

Copy the Codex package into your Codex skills directory:

```powershell
Copy-Item -Path .\packages\codex -Destination "$env:USERPROFILE\.codex\skills\living-mirror" -Recurse -Force
```

Initialize a workspace:

```bash
python scripts/init_distillation.py <workspace>
```

Diagnose local inputs:

```bash
python scripts/diagnose_distillation_inputs.py <workspace-or-raw-folder> --output data-diagnosis.md
```

Merge text messages and voice transcripts:

```bash
python scripts/merge_messages.py --messages raw/messages.jsonl --voice raw/voice-transcripts/transcripts.jsonl --output raw/merged.jsonl --sort
```

Quality-check a portrait:

```bash
python scripts/quality_check_distillation.py --input self-portrait-YYYY-MM.md --product --output quality-report.md
```

Create a user review queue:

```bash
python scripts/make_review_queue.py --input self-portrait-YYYY-MM.md --output review-queue.md
```

Redact a public artifact:

```bash
python scripts/redact_public_artifact.py --input self-portrait-YYYY-MM.md --output public-case-study.md --level public
```

## Repository Structure

```text
.
??? packages/
?   ??? workbuddy/
?   ??? codex/
?   ??? claude-code/
??? docs/
?   ??? design-lineage.md
?   ??? privacy-and-safety.md
?   ??? local-voice-ingestion.md
?   ??? productization-and-community.md
?   ??? visual-templates.md
??? CHANGELOG.md
??? README.md
??? README.zh-CN.md
```

Each package contains:

```text
SKILL.md
agents/openai.yaml
references/
scripts/
assets/templates/
```

## Design Lineage

Living Mirror's architecture is an original integration with conceptual references to `yourself-skill`, `immortal-skill`, and `ex-skill`. The dual Self Memory + Persona structure, contradiction tracking, Correction layer, and evidence grading are credited in [Design Lineage](docs/design-lineage.md).

## License

MIT License. See [LICENSE](LICENSE).
