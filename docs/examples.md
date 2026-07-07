# Examples

## Example 1: Monthly Self Portrait

User request:

```text
Use living-mirror to analyze my June chat records and update my self portrait.
```

Expected flow:

1. Initialize or open `distillation/`.
2. Merge new raw data.
3. Read existing `conflicts.md` and `corrections.md`.
4. Generate a batch report for June.
5. Generate theme reports for relevant themes.
6. Verify sender for every direct quote.
7. Ask the user to review the findings.
8. Update `self-portrait-YYYY-MM.md`.

## Example 2: Relationship Pattern Analysis

User request:

```text
Analyze my long-term conversation with my partner. I want evidence, not vague labels.
```

Good output:

- Uses direct quotes only after sender verification.
- Separates stable patterns from special-period reactions.
- Avoids diagnosing or labeling the relationship from keyword frequency.
- Records contradictions in `conflicts.md`.
- Marks low-confidence observations as pending.

Bad output:

- "You are anxious attachment because the word 'afraid' appears 300 times."
- "Your partner is avoidant" without reading context.
- "The relationship declined" based only on vacation or exam-week data.

## Example 3: Sender Verification

Before writing:

```markdown
The user said "my only happiness is this relationship".
```

Run:

```bash
python scripts/verify_sender.py --input raw/merged.jsonl --keyword "唯一" --context 3
```

Then write only if the original message confirms the speaker:

```markdown
- Evidence: [verbatim] 2024-12-11 | sender=me(verified) | "..."
```

## Example 4: Correction

If the user says:

```text
This is wrong. That was exam week, not my normal attitude.
```

Update `corrections.md`:

```markdown
## CORR-001  YYYY-MM-DD
- Overturned insight: ...
- Reason: exam week was a special period.
- Corrected wording: ...
- Synced to: self-portrait-YYYY-MM.md
- Distiller reflection: special-period data should not become a stable trait.
```

## Example 5: Dynamic Mirror Rules

User request:

```text
Help me understand whether this is really my personality or just a stressful period.
```

Good output:

```markdown
### "Disappearing when cornered" (temporary name)

- Fact: During two deadline-heavy periods, the user sent fewer replies and used shorter sentences in conflict threads.
- Interpretation: This may be a self-protection pattern under pressure, not necessarily a stable interpersonal trait.
- Pattern type: special_period_response / pending_pattern
- Context weight: time=deadline periods; relationship=partner and work chats; body=unknown; event=high workload; medium=text
- Evidence: [artifact] reply density changed in two marked periods; [verbatim] only after sender verification
- Confidence: evidence=medium; interpretation=medium; stability=low
- Falsifiability: If the same pattern appears outside stress periods across multiple relationships, stability confidence rises; if the user says they were deliberately unavailable for logistical reasons, revise.
- User language: pending user naming
```

Bad output:

```text
You are avoidant.
```

## Example 6: Counter-Evidence Index

When an insight has exceptions, do not bury them in prose. Give the exception an ID and show how it changes confidence.

```markdown
### INSIGHT-003 "Needs distance before repair" (temporary name)

- Fact: In three conflict threads, the user stopped replying for several hours before returning with a calmer explanation.
- Interpretation: Distance may be a regulation step before repair.
- Pattern type: relationship_triggered / pending_pattern
- Confidence: evidence=medium; interpretation=medium; stability=low
- Counter-evidence index: CE-001

| ID | Challenges | Counter-evidence | Strength | Status | Effect |
|---|---|---|---|---|---|
| CE-001 | INSIGHT-003 | In one family thread, the user repaired immediately without withdrawing. | medium | open | narrows this pattern to some relationship contexts |
```

