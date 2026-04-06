# PPT Guide Schema

Use this reference when creating or reconstructing a `PPT_GUIDE.md`.

## Deck-Level Fields

Include these fields near the top of the guide:

- `title`: Final or working deck title.
- `goal`: What the audience should remember after the talk.
- `audience`: Who the deck is for and what they already know.
- `duration_minutes`: Speaking time or review time target.
- `slide_budget`: Planned slide count.
- `aspect_ratio`: Usually `16:9` unless the source deck clearly uses another format.
- `style_constraints`: Brand, tone, typography, color, or template requirements.
- `tooling_backend`: Preferred generation stack if already known.
- `source_materials`: Input docs, screenshots, datasets, prior decks, or templates.
- `acceptance_criteria`: Conditions that must pass before delivery.

## Slide-Level Fields

Give every slide a stable id, then document the same fields for each slide:

- `slide_id`: Stable id such as `s01-cover`, `s07-results`, `s12-closing`.
- `target_duration`: Optional but strongly recommended for spoken decks.
- `title`: Visible slide title or `none` if intentionally omitted.
- `message`: Single main point of the slide.
- `visible_text`: Bullets, chips, labels, numbers, or tables that belong on-screen.
- `visuals`: Required assets, charts, diagrams, screenshots, or crops.
- `speaker_notes`: What the presenter should say or emphasize.
- `implementation_notes`: Layout, animation, build hints, or component structure.
- `acceptance_checks`: What must be visually or semantically true on this slide.

## Slide Writing Rules

Use these defaults unless the task clearly calls for something else:

- Give each slide one main message.
- Prefer informative titles over generic section labels.
- Keep visible text audience-facing.
- Keep presenter cues, narration order, and timing in `speaker_notes`.
- Call out what the audience should look at first when the slide contains a complex visual.
- Use `acceptance_checks` to capture likely review failures before coding.

## Stable Slide Id Rules

- Keep ids stable after review begins.
- Use ids in comments, review notes, and commit messages.
- Do not renumber ids just because slides move. Rename only when the slide's role truly changes.

## Visible Text vs Speaker Notes

- Put audience-facing content in `visible_text`.
- Put narration, timing, and explanation order in `speaker_notes`.
- Do not mix presenter instructions into visible text.

## Asset Provenance

When visuals matter, record where they come from:

- Original file path or URL.
- Whether the asset is cropped, redrawn, or directly reused.
- Which part of the source matters.
- Any numbers or labels that must stay faithful to the source.

## Acceptance Checks

Use acceptance checks to make reviews concrete. Common checks:

- Title and takeaway fit on one line or wrap intentionally.
- No text collision, overflow, or cut-off.
- Main chart or image is readable without zooming.
- Visual hierarchy is clear within three seconds.
- Speaker notes still match the visible slide after edits.
- Footer or caption does not contain presenter-only instructions.

## Recommended Skeleton

```md
# PPT_GUIDE

## Deck Brief

- Title: `...`
- Goal: `...`
- Audience: `...`
- Duration: `...`
- Slide Budget: `...`
- Aspect Ratio: `16:9`
- Style Constraints: `...`
- Tooling Backend: `...`
- Source Materials:
  - `...`
- Acceptance Criteria:
  - `...`

## Slide Plan

### s01-cover

- Target Duration: `0:30`
- Title: `...`
- Message: `...`
- Visible Text:
  - `...`
- Visuals:
  - `...`
- Speaker Notes:
  - `...`
- Implementation Notes:
  - `...`
- Acceptance Checks:
  - `...`

### s02-context

...repeat...
```

## Reconstruction Rule

When the user gives you only an existing deck:

1. Extract slide order and current messages.
2. Create a minimal guide with stable slide ids.
3. Backfill missing speaker notes, asset provenance, and acceptance checks only where needed for the requested edits.
