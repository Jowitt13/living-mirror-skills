# Changelog

## v0.9 - 2026-07-10

Living Mirror v0.9 upgrades the self-distillation core framework itself to **v0.9**. The earlier product-layer additions are now part of the unified framework, and new manifests, templates, self portraits, and framework documents should use `framework_version: "v0.9"`.

### Added

- v0.9 as the unified core framework version across README, package skills, references, templates, and scripts.
- v0.9 insight schema as the primary structured insight schema.
- Public case-study, export, and community template guidance as core framework outputs.

### Promoted into Core

- v0.7 onboarding, data diagnosis, consent scope, privacy levels, redaction, and forgetting/deletion rules.
- v0.8 action translation, relationship maps, repair/boundary scripts, and review queues.
- v0.9 community templates, export packs, public case-study shape, and contribution checklist.

### Changed

- Initialization now creates `framework_version: "v0.9"` and default portrait version `v0.9.0`.
- Quality checker now reports Living Mirror v0.9 checks and treats product/community fields as v0.9 framework fields.
- Documentation now treats v0.9 as the unified core framework rather than an external add-on.

## Skill Pack v0.8 - 2026-07-09

Living Mirror Skill Pack v0.8 turns v0.6 self-understanding into reviewable action and relationship workflows.

Added:

- Action translation reference for 7-day experiments, conversation scripts, boundary scripts, repair scripts, decision lenses, and environment adjustments.
- Relationship pack for relationship maps, conflict loops, repair maps, and consent-safe relationship analysis.
- Review queue script: `scripts/make_review_queue.py`.
- Weekly experiment and relationship-map templates.

## Skill Pack v0.7 - 2026-07-09

Living Mirror Skill Pack v0.7 lowers the barrier to starting and strengthens privacy.

Added:

- Onboarding and data diagnosis reference.
- Cold-start interview mode for users without organized records.
- Data diagnosis script: `scripts/diagnose_distillation_inputs.py`.
- Privacy, consent, redaction, and forgetting/deletion rules.
- Public/shareable artifact redaction script: `scripts/redact_public_artifact.py`.

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

- Skill reference routing points agents to the v0.6 schema and quality checker.
- Self-portrait and theme-report templates require counter-evidence and user-language fields.

## v0.5 - 2026-07-07

Added optional sensitive theme 16: intimacy / sexuality expression. This theme is off by default and requires explicit user consent.

## v0.4 - 2026-07-07

Expanded longitudinal distillation from 10 themes to 15 themes by adding food preferences, lifestyle habits, thinking style, worldview/lifeview, and hobbies.
