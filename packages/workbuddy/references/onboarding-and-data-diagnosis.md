# Onboarding and Data Diagnosis v0.7

Use this reference when the user wants to start Living Mirror but does not yet have a clean data pipeline, has only a small amount of data, or feels unsure about what to import first.

The goal of v0.7 is to make Living Mirror usable before the user has a perfect archive.

## Start Modes

Choose the smallest mode that can answer the user's real question.

| Mode | Use when | Output |
|---|---|---|
| `light_start` | The user has little or no prepared data. | Starter portrait from guided interview, with all claims marked low stability until evidence arrives. |
| `standard` | The user has one or two data sources, such as WeChat export + notes. | Monthly or quarterly portrait with evidence ledger and review queue. |
| `deep` | The user has years of records, voice transcripts, or multiple relationships to compare. | Two-pass distillation: time batches + theme reports + merged portrait. |
| `repair_only` | The user wants to examine one conflict or relationship pattern. | Relationship map, repair map, and validation questions. |
| `public_share` | The user wants to publish or present results. | Redacted public artifact, no raw private quotes by default. |

Do not push the user into `deep` mode when the real pain is "I need one clear starting point."

## Cold-Start Interview

If data is missing, ask for a short interview instead of blocking.

Use 8 to 20 questions from this pool:

1. What kind of pattern do you most want to understand right now?
2. Which period of your life feels most relevant?
3. Which relationships should be included or excluded?
4. What should this mirror never infer without asking you first?
5. What are three sentences you often use to describe yourself?
6. What are three sentences other people often use to describe you?
7. What do you repeatedly want but struggle to act on?
8. When stressed, do you move toward people, away from people, into work, into control, or into numbness?
9. What gives you energy quickly?
10. What drains you even when nothing "bad" happened?
11. What kind of environment makes you feel like yourself?
12. What do you want the portrait to help with in the next seven days?

Rules:

- Mark interview-derived insights as `impression` or `user_self_report`, not as verified longitudinal evidence.
- Use `pending_pattern` unless the user provides repeated examples.
- Write "needs later evidence" for anything that should be checked against records.

## Data Diagnosis Checklist

Before distillation, inspect the data and produce a short diagnosis:

- Source types: chat, voice transcript, note, diary, screenshot-derived text, artifact.
- Format: jsonl, json, csv, txt, md, audio.
- Count: approximate number of records and usable text rows.
- Time span: earliest and latest timestamp if available.
- Sender quality: whether `sender`, `is_self`, `talker`, or equivalent fields exist.
- Conversation quality: whether relationship or room fields exist.
- Text quality: empty rows, OCR noise, transcript confidence, duplicate messages.
- Sensitive areas: relationship names, family records, sexuality/intimacy, health, workplace, minors.
- Recommended mode: `light_start`, `standard`, `deep`, `repair_only`, or `public_share`.

Use `scripts/diagnose_distillation_inputs.py` when local files are available.

## Minimum Useful Input

Living Mirror can start with any of these:

- 20 to 50 interview answers for a starter portrait.
- One month of messages for a narrow current-state portrait.
- One relationship export for a relationship map.
- A note archive for values, goals, taste, and thinking style.
- Voice transcripts for emotional cadence and recurring themes.

Always state the limit of the data. A small dataset can be useful, but it should not pretend to be a full self portrait.

## Import Field Map

Normalize source records into this loose shape when possible:

```json
{
  "timestamp": "2026-07-09 20:30:00",
  "sender": "me",
  "is_self": true,
  "conversation": "friend_group_or_private_chat",
  "text": "message content",
  "source": "wechat_export",
  "source_file": "raw/messages.jsonl",
  "medium": "text"
}
```

For voice transcripts, add:

```json
{
  "medium": "voice",
  "audio_file": "raw/audio/example.m4a",
  "transcript_confidence": "unknown|low|medium|high",
  "asr_model": "user-provided-local-model"
}
```

Do not hardcode the speech model name in the skill. The user configures it at runtime.

## Diagnosis Report Template

```markdown
# Living Mirror Data Diagnosis

- Recommended mode: <light_start|standard|deep|repair_only|public_share>
- Usable text records: <N>
- Audio files needing transcription: <N>
- Time span: <earliest> to <latest>
- Sender fields: <good|partial|missing>
- Conversation fields: <good|partial|missing>
- Main risks: <sender ambiguity / missing dates / sensitive relationships / transcript noise>

## Next Step

1. <one concrete next command or interview step>
2. <privacy or consent step if needed>
3. <first distillation output to create>
```

