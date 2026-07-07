# Dynamic Mirror Rules

Use these rules when writing a self portrait, merging theme reports, deciding whether an observation is stable, or turning repeated evidence into a user-facing insight.

The goal is to keep Living Mirror from becoming a fixed personality labeler. A person is partly stable, partly contextual, partly changing, and partly still unknown.

## Human Understanding Dimensions

These dimensions can be added to the 16-theme framework when the source data supports them. Do not force them when evidence is thin. Use them as lenses for understanding the person behind the records, not as extra labels to fill.

1. **Body and energy state**: sleep, fatigue, appetite, sensory load, recovery rhythm, illness periods, and how the body changes emotional or social capacity.
2. **Shame, defense, and self-protection**: moments where the user hides, jokes, withdraws, overexplains, attacks first, freezes, or avoids being seen.
3. **Desire-action gap**: what the user repeatedly wants, says they value, or imagines doing, compared with what they actually choose under time, money, fear, habit, or relationship pressure.
4. **Aesthetic and order system**: preferred texture, color, density, cleanliness, ritual, digital/physical organization, and the kind of environment that makes the user feel like themselves.
5. **Relationship role switching**: how the user changes between partner, child, friend, creator, worker, caregiver, learner, leader, or protected person.
6. **Agency and control**: where the user seeks autonomy, where they surrender control, and what makes them feel trapped or free.
7. **Attention and learning rhythm**: how curiosity starts, deepens, scatters, or becomes mastery.
8. **Meaning and narrative**: the stories the user uses to explain their life, wounds, luck, effort, love, failure, and becoming.
9. **Boundary and consent pattern**: how the user says yes, says no, delays, tests safety, or changes their mind.
10. **Repair and reconciliation**: how the user apologizes, reopens contact, makes meaning after conflict, or decides not to repair.

## State vs Trait

Every major insight should include a pattern type:

- `stable_trait`: appears across time, relationships, and contexts.
- `stage_state`: belongs to a life stage, project cycle, relationship phase, or identity transition.
- `special_period_response`: likely caused or amplified by exams, illness, travel, grief, major deadlines, conflict, crisis, or unusual workload.
- `relationship_triggered`: appears mainly with specific people, roles, or relational stakes.
- `pending_pattern`: plausible but not yet supported enough to promote.

Do not call something a stable trait if it only appears in one period, one relationship, or one emotional spike.

## Context Weight

For each insight, mark the context weight that shaped it:

- `time_weight`: recent, old, repeated, seasonal, or tied to a named period.
- `relationship_weight`: partner, family, friend, group, stranger, colleague, self-talk.
- `body_weight`: sleep, illness, fatigue, hunger, medication, cycle, sensory overload, recovery.
- `environment_weight`: school, work, home, travel, city, online space, financial pressure.
- `event_weight`: deadline, breakup, reunion, exam, launch, loss, achievement, conflict.
- `medium_weight`: text, voice, note, diary, long-form writing, screenshot, artifact.

If a context weight is strong, say so before turning the insight into identity language.

## Three-Part Confidence

Replace one flat confidence score with three scores when the insight matters:

- `evidence_confidence`: how solid the supporting material is.
- `interpretation_confidence`: how safe the meaning-making is.
- `stability_confidence`: how likely this is to remain true outside the sampled context.

Use `high`, `medium`, or `low` for each. A quote can make evidence confidence high while stability confidence remains low.

## Fact, Interpretation, Name

Separate three layers:

1. `fact`: what the data directly shows.
2. `interpretation`: what the distiller thinks it may mean.
3. `temporary_name`: a short label for the pattern, explicitly allowed to be renamed by the user.

Never let a poetic label outrun the evidence.

## Falsifiability and Counter-Evidence

Every important insight should include what would overturn or weaken it:

- What future evidence would disprove this?
- What user correction would replace it?
- Which context, if removed, would make the pattern disappear?
- What stronger alternative explanation exists?

If there is no imaginable way to overturn an insight, it is probably too vague.

Maintain a counter-evidence index for important insights. Counter-evidence is not a nuisance; it is part of the portrait.

Use IDs like `CE-001` and link them to the insight they challenge:

```markdown
| ID | Challenges | Counter-evidence | Strength | Status | Effect |
|---|---|---|---|---|---|
| CE-001 | INSIGHT-003 | <source/date/artifact or paraphrased quote> | low/medium/high | open/resolved/overridden | weakens / narrows / overturns / creates CONFLICT |
```

Rules:

- Add counter-evidence when the data shows a meaningful exception, reversal, or alternative explanation.
- Do not hide counter-evidence inside prose. Give it an ID.
- If counter-evidence is strong, lower `stability_confidence` or move the insight to `pending_pattern`.
- If counter-evidence is unresolved, link it to `conflicts.md`.
- If the user explains the counter-evidence, update the index instead of deleting it.

## User-Language Priority

When the user has their own wording for a pattern, prefer that wording over external labels. Keep professional or theoretical labels secondary unless the user asks for them.

Bad:

```text
You have avoidant tendencies.
```

Better:

```text
The current evidence supports the user's own phrase "I disappear when I feel cornered"; whether this is a stable attachment pattern remains pending.
```

## Output Forms

Besides the full self portrait, Living Mirror can produce smaller outputs:

- **Short portrait**: 5 to 9 evidence-backed bullets for quick review.
- **Relationship map**: patterns by relationship type or specific consented relationship.
- **Change timeline**: when a pattern appeared, intensified, softened, or was corrected.
- **Validation questions**: concrete questions for the user to confirm, reject, or rename insights.
- **Evidence ledger**: a compact table of insights, supporting evidence, counter-evidence, and current confidence.
- **Context dashboard**: a non-quantified overview of which contexts shape the current portrait most.
- **Repair map**: how the user repairs conflict, restores safety, or decides not to continue a relationship.
- **Naming glossary**: user-owned phrases for recurring patterns, with external labels kept secondary.

## Insight Card Template

Use this compact card inside theme reports or self portraits:

```markdown
### <temporary pattern name>

- Fact: <what the data directly shows>
- Interpretation: <what this may mean>
- Pattern type: stable_trait / stage_state / special_period_response / relationship_triggered / pending_pattern
- Context weight: time=<...>; relationship=<...>; body=<...>; event=<...>; medium=<...>
- Evidence: [verbatim/artifact/impression] <source, date, sender verification, or statistic>
- Confidence: evidence=<high|medium|low>; interpretation=<high|medium|low>; stability=<high|medium|low>
- Falsifiability: <what would overturn or weaken this>
- Counter-evidence index: CE-XXX / none found / pending search
- User language: <user's own wording if available; otherwise "pending user naming">
- Status: [new YYYY-MM] / [revised YYYY-MM] / pending / overturned by CORR-XXX
```
