# PPT Guide Schema

Use this reference when creating or reconstructing a `PPT_GUIDE.md`.

For spoken or high-stakes decks, the guide should be specific enough that:

- the generator can implement each page without guessing what belongs on-screen
- the presenter can read the notes aloud with only light improvisation

This is stricter than a normal outline.

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
- `notes_policy`: Whether the final deck must embed notes, and whether notes equal the read-aloud script only or script plus explicit supplements.
- `audience_language`: Primary language expected in visible text.
- `source_materials`: Input docs, screenshots, datasets, prior decks, or templates.
- `acceptance_criteria`: Conditions that must pass before delivery.

## Recommended Top-Level Sections

For most maintained decks, prefer these sections in order:

1. Working assumptions
2. Document purpose and how to use the guide
3. Timing or pacing plan when the deck is spoken
4. Global production principles
5. Slide-by-slide production and notes

This structure is especially useful for talks, paper readings, training decks, workshops, and executive presentations that will be revised later.

## Spoken-Deck Defaults

If the deck is meant to be spoken live and the user does not specify otherwise:

- Include a cover slide
- Include a takeaway or summary slide near the end
- Include a separate closing slide
- Keep timing in the guide rather than guessing from slide body length
- Treat `PPT_GUIDE.md` as the source of truth for speaker notes when the final deck must embed them

### Cover And Closing Content Contracts

When the deck is spoken live, the guide should lock in concrete content for the first and last slides instead of leaving them as generic placeholders:

- Cover slide: working or final title, subtitle or framing line when appropriate, presentation date or period, and the presenter's name. If the deck expects a bilingual presenter name (e.g. Chinese plus English), the guide should record both forms so the generator does not have to guess.
- Summary slide: sits immediately before the closing slide when both exist. It carries the takeaways the audience should remember; it does not introduce new technical content that was not supported earlier.
- Closing slide: reserved for `Q&A`, thanks, or a short wrap-up phrase. It does not carry new claims, new numbers, or new experiments. Long secondary-language prose on this slide is a sign the content belongs in speaker notes or in an earlier slide.

### Per-Page Audience-Language Purity

For spoken decks with a dominant audience language, mark any pages where visible text must stay primarily in that language. Summary, takeaway, limitation, and closing-adjacent pages almost always qualify. Short proper nouns - paper titles, system names, benchmark names, model names - may stay in their original language even on these pages, but long secondary-language paragraphs should route into speaker notes.

When creating the guide, record the page's primary-language requirement alongside its other slide-level fields rather than leaving it implicit, so a later generator cannot accidentally fill the summary slide with long English prose on a Chinese talk or long Chinese prose on an English talk.

## Slide-Level Fields

Give every slide a stable id, then document the same fields for each slide:

- `slide_id`: Stable id such as `s01-cover`, `s07-results`, `s12-closing`. This is internal production metadata, not default visible slide text.
- `target_duration`: Optional but strongly recommended for spoken decks.
- `cumulative_time`: Optional but recommended for spoken decks that are tightly timed.
- `title`: Visible slide title or `none` if intentionally omitted.
- `subtitle`: Optional subtitle, kicker, or framing line.
- `message`: Single main point of the slide.
- `visible_text`: Bullets, chips, labels, numbers, or tables that belong on-screen.
- `visuals`: Required assets, charts, diagrams, screenshots, or crops.
- `formula_requirements`: Optional but strongly recommended when a slide contains important formulas, notation, loss functions, or complexity expressions.
- `symbol_explanations`: Optional visible or note-only symbol meanings for important formulas.
- `speaker_notes`: What the presenter should say or emphasize.
- `notes_supplement`: Optional additional cues that should be appended to the read-aloud baseline when the final deck embeds notes.
- `implementation_notes`: Layout, animation, build hints, or component structure.
- `acceptance_checks`: What must be visually or semantically true on this slide.
- `generator_ready_instructions`: Optional but recommended when the slide is complex; state what the generator should actually build.
- `presenter_ready_notes`: Optional but recommended when the slide is spoken live; write notes as complete lines a presenter can say.

## Slide Writing Rules

Use these defaults unless the task clearly calls for something else:

- Give each slide one main message.
- Prefer informative titles over generic section labels.
- Keep visible text audience-facing.
- Keep internal slide ids such as `s01-cover` in the guide, code, and review notes rather than on the visible slide unless explicitly requested.
- Keep presenter cues, narration order, and timing in `speaker_notes`.
- When the final deck must embed notes, treat `speaker_notes` as the minimum baseline and put extra cues in `notes_supplement` rather than inventing them in code.
- Call out what the audience should look at first when the slide contains a complex visual.
- Use `acceptance_checks` to capture likely review failures before coding.
- If a slide is intended for live presentation, write `speaker_notes` in direct, speakable sentences instead of bullet fragments.
- If a slide contains an important formula, explain which symbols must be visible, which details can stay in notes, and whether the main deck should use a compact or full form.
- If a slide is complex, make `implementation_notes` and `generator_ready_instructions` concrete enough that the generator can follow them without inventing missing structure.

## Formula Guidance In The Guide

When a slide contains formulas or non-trivial notation:

- State whether the formula must appear on-screen or may stay in notes/appendix.
- Record whether the slide should use a compact main-deck form or a fuller expression.
- Identify which symbols must be explained on-screen.
- Identify which terms or indices can remain in notes.
- Tie the formula to the slide's diagram, figure, table, or spoken explanation order.
- Add acceptance checks for formula fit, readability, and alignment with neighboring content.

Do not leave formula handling implicit if another agent or generator will implement the deck.

## Visible Text vs Speaker Notes

Visible text must stay audience-facing.
Speaker notes can stay presenter-facing.

Bad visible text:

- `s01-cover`
- `先讲背景，再讲方法`
- `这一页重点强调我们比 baseline 快`
- `后面一页再解释这里的风险`

Good visible text:

- `Current approval flow adds 3 handoffs`
- `Our system reaches break-even in month 7`
- `Latency falls after prefix caching`

Good speaker note:

- `先提醒听众这是流程瓶颈页，再按左到右解释 3 个 handoff，最后落到“时间损耗主要来自人工交接”。`

## Speaker Notes As A Deliverable

When the final deck must contain speaker notes:

- `PPT_GUIDE.md` is the authority for the note baseline.
- Every slide should have a note entry unless the guide explicitly says otherwise.
- `notes_supplement` is for presenter cues, pauses, pointing order, or hidden reminders that are still intentionally part of deck notes.
- The generator should not invent note text outside that contract.
- Slide count, guide note count, and final note count should match.
- Update notes when visible text changes or explicitly confirm the notes still match.

## Generator-Ready Guidance

If another agent or script will implement the deck, slide instructions should answer concrete build questions such as:

- Which visual asset should be used
- Whether the asset should be cropped, redrawn, or highlighted
- Which text belongs in the title, body, footer, chip, or caption
- Which numbers or labels must be emphasized
- Whether the slide should be one-column, two-column, card-based, or chart-led
- Whether the slide should reveal content in steps

Avoid vague directions like:

- `make this slide cleaner`
- `put the method here`
- `show the experiment result`

Prefer directions like:

- `Use the product screenshot on the left at roughly 55% slide width; place three audience-facing proof points on the right; highlight the approval banner with a thin outline box; keep the footer as a one-line takeaway.`

- `Crop Table 2 from the source PDF, enlarge the right half, highlight the best value with an outline box, and put a three-line takeaway card on the right.`

## Presenter-Ready Notes

When the deck is meant to be spoken live:

- Notes should be complete enough to read aloud.
- Notes should explain transitions, caveats, and interpretation.
- Notes should not simply repeat the visible text.
- Notes can contain timing and pointing cues.

Weak note:

- `背景 -> 问题 -> 方法`

Strong note:

- `这一页先用 10 秒说明现有流程为什么慢，再指左侧流程图的 3 个审批节点，最后用一句话过渡到“所以我们需要自动化方案”。`

## Stable Slide Id Rules

- Keep ids stable after review begins.
- Use ids in comments, review notes, and commit messages.
- Treat ids as production-only labels unless the user explicitly wants them shown on the slide.
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
- Important formulas render cleanly and have enough space for limits, subscripts, and neighboring explanations.
- Visual hierarchy is clear within three seconds.
- Speaker notes still match the visible slide after edits.
- Required notes are present in the final deck rather than only in the guide.
- Footer or caption does not contain presenter-only instructions.
- Internal slide ids and workflow labels do not appear on the visible slide unless explicitly requested.
- The slide can be implemented from the guide without inventing missing structure.
- The spoken note still sounds natural if read aloud.

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
- Notes Policy: `...`
- Audience Language: `...`
- Source Materials:
  - `...`
- Acceptance Criteria:
  - `...`

## Document Purpose And Usage

- This guide is the source of truth for deck intent.
- Revise this guide first for narrative, audience, timing, and slide-order changes.
- Revise the generator first for layout, crop, font, and styling changes.

## Timing Plan

- `s01-cover`: `0:30`
- `s02-context`: `1:00`

## Slide Plan

### s01-cover

- Target Duration: `0:30`
- Cumulative Time: `0:30`
- Title: `...`
- Subtitle: `...`
- Message: `...`
- Visible Text:
  - `...`
- Visuals:
  - `...`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `...`
- Notes Supplement:
  - `None`
- Implementation Notes:
  - `...`
- Generator-Ready Instructions:
  - `...`
- Presenter-Ready Notes:
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
