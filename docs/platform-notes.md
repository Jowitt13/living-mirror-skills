# Platform Notes

## WorkBuddy Version

Path:

```text
packages/workbuddy/
```

This version keeps WorkBuddy-style metadata in `SKILL.md`:

- `version`
- `updated`
- `platforms`
- `triggers`

Use it when your skill runner supports richer frontmatter and natural trigger phrases.

## Codex Version

Path:

```text
packages/codex/
```

This version uses Codex-compatible frontmatter:

```yaml
---
name: self-distillation
description: ...
---
```

It is intended to pass Codex skill validation.

## Claude Code Version

Path:

```text
packages/claude-code/
```

This version keeps Claude-friendly metadata and includes a small `README.md` with invocation examples.

## Shared Contents

All versions share:

- `references/framework-v2.md`
- `references/evidence-grading.md`
- `references/conflict-tracker.md`
- `references/correction-rules.md`
- `references/sender-verification.md`
- `references/special-period.md`
- `references/keyword-usage.md`
- report templates
- standard-library Python scripts

The core method is the same across platforms.
