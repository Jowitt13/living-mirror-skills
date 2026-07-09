# Community Template Kit v0.9

Use this reference when producing reusable templates, public examples, Obsidian/Notion-style exports, social cards, or contribution-ready community artifacts.

v0.9 turns Living Mirror from a private framework into something people can copy, adapt, and safely share.

## Community Template Principles

1. No real private data in templates.
2. Every example should use synthetic or heavily redacted content.
3. Templates should state the pain point they solve.
4. The user should be able to choose `light_start`, `standard`, or `deep`.
5. Public artifacts should preserve the method without exposing the life.

## Template Categories

| Category | Solves | Example output |
|---|---|---|
| Starter | "I do not know how to begin." | Cold-start interview and starter portrait. |
| Trust | "I am afraid of exposing my records." | Privacy checklist and redacted public artifact. |
| Review | "The AI may be wrong." | Review queue and Correction prompts. |
| Action | "The portrait is accurate, but what do I do?" | 7-day experiment cards and scripts. |
| Relationship | "My pain is in relationships." | Relationship map, conflict loop, repair map. |
| Creator / Work | "I want to understand my energy and projects." | Attention rhythm, decision lens, project pattern review. |
| Public Showcase | "I want to post this beautifully." | Social cards, GitHub README, demo case study. |

## Export Targets

| Target | Structure |
|---|---|
| Obsidian | `index.md`, `insights/`, `evidence/`, `reviews/`, `actions/` |
| Notion | One dashboard page plus linked databases for insights, evidence, experiments, corrections. |
| PDF | Executive summary, method, portrait, evidence ledger, review questions. |
| Static HTML | Public-safe case study, visual cards, privacy note. |
| Xiaohongshu / social | 4 to 8 cards: pain point, method, framework, example, privacy, call-to-reflect. |

## Community Contribution Checklist

Before accepting a new template:

- [ ] It solves a recognizable user pain.
- [ ] It does not require private data to understand.
- [ ] It includes consent and privacy guidance.
- [ ] It keeps evidence and counter-evidence visible.
- [ ] It includes a review or correction step.
- [ ] It does not diagnose, moralize, or manipulate.
- [ ] It can run in at least one of Codex, Claude Code, or WorkBuddy.

## Public Case Study Shape

```markdown
# <Use Case Name>

## Pain Point
<What common problem this template solves.>

## Who It Is For
<Audience.>

## Inputs
<Data needed; include a no-data light-start path.>

## Workflow
1. <Step>
2. <Step>
3. <Step>

## Outputs
- <Artifact>
- <Artifact>

## Privacy Notes
<What must be redacted before sharing.>

## Example
<Synthetic or anonymized example only.>
```

