# Privacy, Consent, and Redaction v0.7

Use this reference before handling private records, relationship material, sensitive themes, or anything the user wants to publish.

Living Mirror should make people feel more in control of their records, not more exposed.

## Consent Scope

Before deep work, identify the active scope:

| Scope | Meaning |
|---|---|
| `source_scope` | Which files, folders, apps, or exports may be used. |
| `time_scope` | Which dates or life periods may be analyzed. |
| `relationship_scope` | Which people or relationship categories may be included. |
| `theme_scope` | Which themes may be analyzed. Sensitive theme 16 is off unless explicitly allowed. |
| `output_scope` | Private, shareable, or public output. |

If the user is unsure, choose the narrower scope and mark exclusions clearly.

## Output Privacy Levels

| Level | Use for | Rules |
|---|---|---|
| `private` | Personal local review. | Evidence may include short verified quotes, local source IDs, and relationship-specific detail. |
| `shareable` | Sharing with a coach, partner, collaborator, or trusted person. | Remove names and local paths; keep paraphrased evidence; include only consented relationships. |
| `public` | GitHub, social media, examples, blog posts, talks. | No real names, no raw chat quotes by default, no local paths, no private relationship identifiers, no source files. |

Use `scripts/redact_public_artifact.py` before publishing.

## Redaction Rules

Redact or generalize:

- Real names, nicknames, usernames, handles, group names.
- Phone numbers, emails, addresses, IDs, order numbers, account numbers.
- Local filesystem paths.
- Workplace, school, family, medical, sexual, or financial details when not essential.
- Quotes that expose a non-consenting third party.

Prefer:

- "a close friend" instead of a real name.
- "a family conversation" instead of a group name.
- "a repeated deadline period" instead of a specific employer/project.
- Paraphrase instead of direct quote.

## Relationship Consent

When analyzing a relationship:

- Analyze the user's pattern, not the other person's inner state.
- Do not diagnose the other person.
- Do not publish identifiable third-party material.
- For a specific partner/family/friend map, ask whether the user wants names anonymized even in the private artifact.
- If the relationship is ongoing and high-stakes, include a "what this portrait should not be used for" note.

## Sensitive Theme 16

The intimacy/sexuality expression theme is opt-in.

Rules:

- Do not infer or ask follow-up questions unless the user explicitly enables the theme.
- If enabled, keep quotes minimal and prefer paraphrase.
- Do not moralize, pathologize, or label the user.
- Allow "skip this permanently" without reducing the quality of the rest of the portrait.

## Forgetting and Deletion

The user can remove a source, person, period, or theme from future analysis.

When deletion is requested:

1. Remove the source from active manifests.
2. Mark derived insights as `needs_recheck` if they depended on that source.
3. Do not silently keep the deleted material in examples, demos, or public artifacts.
4. Keep a minimal changelog entry such as "source removed by user request" without reproducing the content.

## Public Artifact Checklist

Before posting or committing:

- [ ] No raw private logs.
- [ ] No local paths.
- [ ] No real names or group names.
- [ ] No non-consenting third-party quotes.
- [ ] Sensitive theme omitted unless explicitly allowed.
- [ ] Output marked as `public`.
- [ ] Evidence preserved as generalized support, not exposed source text.

