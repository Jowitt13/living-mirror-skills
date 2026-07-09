# living-mirror for Claude Code

This package is the Claude Code version of Living Mirror v0.9.

## Recommended location

```text
C:\Users\<you>\.claude\skills\living-mirror
```

## Example prompts

- `Use living-mirror to diagnose these local records before distillation.`
- `使用 living-mirror 蒸馏我的聊天记录，先验证 sender。`
- `帮我把这份自画像生成复核队列。`
- `把这些洞察变成 7 天行动实验。`
- `生成一个 public 版本，先脱敏。`
- `按 relationship-pack 做一张关系地图。`

## Entry points

- `SKILL.md`: main workflow and routing.
- `references/`: evidence, conflict, correction, onboarding, privacy, action, relationship, and community template guides.
- `scripts/`: local utilities for diagnosis, filtering, sender verification, quality checks, review queues, voice ingestion, and redaction.
- `assets/templates/`: reusable Markdown templates for interviews, experiments, relationship maps, case studies, and Obsidian-style exports.

## Claude Code usage notes

1. Read `SKILL.md` first.
2. Diagnose data before deep distillation when local files are available.
3. Verify sender before using quotes or assigning actions to a person.
4. Keep sensitive theme 16 off unless the user explicitly opts in.
5. Generate review questions before promoting uncertain insights.
6. Redact public artifacts before sharing or committing.

