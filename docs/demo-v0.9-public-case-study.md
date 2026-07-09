# Demo v0.9 Public Case Study

> Synthetic example. No real private records are included.

## Pain Point

The user wants to understand why they disappear during tense conversations, but they do not want to expose raw chat logs publicly.

## Input Mode

- Mode: `standard`
- Sources: synthetic chat fragments + synthetic notes
- Privacy level: `public`
- Sensitive theme 16: skipped

## Data Diagnosis

- Usable text records: 1,240
- Sender coverage: 98%
- Conversation coverage: 90%
- Main risk: tense periods are clustered around deadlines, so stability confidence should stay low until more contexts are checked.

## Insight Card

### INSIGHT-003: "I need a little time"

- Fact: In several tense threads, the user paused before returning with a more careful reply.
- Interpretation: This may be a regulation step before repair, not simple avoidance.
- Pattern type: relationship_triggered / pending_pattern
- Context weight: time=deadline-heavy months; relationship=close relationships; body=unknown; event=conflict; medium=text
- Evidence: [artifact] reply timing changed in marked conflict threads; [impression] supported by synthetic notes
- Confidence: evidence=medium; interpretation=medium; stability=low
- Falsifiability: If the same pattern appears outside conflict, or the user says the pauses were logistical, revise.
- Counter-evidence index: CE-001
- User language: "I need a little time"
- Review state: needs_more_evidence
- Privacy level: public

## Counter-Evidence

| ID | Challenges | Counter-evidence | Strength | Status | Effect |
|---|---|---|---|---|---|
| CE-001 | INSIGHT-003 | In one synthetic family thread, the user repaired immediately without pausing. | medium | open | narrows |

## Review Queue

1. Does "I need a little time" sound like the user's own language?
2. Is this pattern specific to close relationships?
3. Was the deadline period amplifying the pause?
4. Should this be an action experiment or stay as observation?

## 7-Day Experiment

- Tiny action: In one low-stakes tense moment, say "I want to answer this well. I need an hour."
- What to observe: relief, anxiety, repair quality, whether the pause becomes avoidance.
- Stop condition: stop if it increases pressure, fear, or conflict.

## Public-Safe Notes

- No raw chat quotes.
- No real names.
- No local paths.
- No identifiable third-party material.
- Pattern is presented as pending, not as a fixed personality label.

