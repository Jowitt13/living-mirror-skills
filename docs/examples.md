# Examples

## Example 1: Monthly Self Portrait

User request:

```text
Use self-distillation to analyze my June chat records and update my self portrait.
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
