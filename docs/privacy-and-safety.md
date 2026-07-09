# Privacy and Safety

Living Mirror Skills is designed for local-first qualitative analysis. The framework can touch intimate records, relationship material, family history, work stress, and voice transcripts, so privacy is a product feature, not an afterthought.

## Core Rules

1. Keep raw chat logs, notes, diaries, and voice transcripts local by default.
2. Do not commit private data to GitHub.
3. Do not include real chat exports in examples.
4. Quote only what is necessary.
5. Prefer paraphrase or redaction when a direct quote is not needed.
6. Treat relationship and family records as sensitive data.
7. Use synthetic or heavily redacted material for public demos.

## Consent Scope

Before deep analysis, identify:

- `source_scope`: which files or apps may be used.
- `time_scope`: which period may be analyzed.
- `relationship_scope`: which people or relationship categories may be included.
- `theme_scope`: which themes may be analyzed.
- `output_scope`: private, shareable, or public.

If the scope is unclear, choose the narrower interpretation and ask the user to confirm later.

## Privacy Levels

| Level | Use for | Rules |
|---|---|---|
| `private` | Local personal review. | Short verified quotes may appear; local source IDs are allowed. |
| `shareable` | Trusted coach, partner, collaborator, or researcher. | Remove real names, local paths, and non-consenting third-party quotes. |
| `public` | GitHub, blog, talk, Xiaohongshu, social cards. | No raw private logs by default; use synthetic or redacted examples. |

Run `scripts/redact_public_artifact.py` before publishing.

## Evidence Safety

Every meaningful insight should be traceable to evidence:

- `verbatim`: direct quote, sender verified.
- `artifact`: descriptive statistics or behavior traces.
- `impression`: interpretation, never enough alone.

Low-confidence insights should remain pending instead of being promoted into the self portrait.

## Stability Safety

Do not turn a temporary state into a permanent identity claim.

For important insights, separate:

- evidence confidence
- interpretation confidence
- stability confidence

A quote can be real and sender-verified while the broader interpretation is still uncertain. Mark context weight such as stress period, illness, relationship role, or medium before calling a pattern stable.

## Counter-Evidence Safety

Do not omit exceptions just because they make the portrait less neat. Important counter-evidence should be visible as `CE-XXX` entries and linked to the insight it challenges.

Strong counter-evidence should lower stability confidence, narrow the claim, create a CONFLICT, or overturn the insight.

## Sender Safety

Never make a claim about who said or did something from a summary alone. Go back to the original data and verify fields such as:

- `sender`
- `is_self`
- `talker`
- `conversation`
- `timestamp`

This is especially important for voice transcripts, group chats, and preprocessed summaries.

## Psychological Safety

This project can surface uncomfortable patterns. Use it gently:

- Do not turn observations into fixed identity labels.
- Do not let a diagnosis-like label replace the user's own language.
- Do not diagnose mental health conditions.
- Do not use a self portrait to pressure or manipulate someone.
- Let the user correct the analysis.
- Keep contradictions open when the evidence is mixed.
- Encourage professional support when the user is in danger or needs clinical care.

This is a reflective tool, not a clinical tool.

## Forgetting and Deletion

When a user removes a source, person, period, or theme:

1. Remove it from the active manifest.
2. Mark dependent insights as `needs_recheck` or move them to pending.
3. Do not keep deleted content in public examples.
4. Keep only a minimal changelog entry without reproducing the removed content.

