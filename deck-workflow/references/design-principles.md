# Design Principles

This reference synthesizes reusable slide-design guidance from public presentation and accessibility guidance together with the practical deck workflow used in this repository family.

Public guidance converges on a few stable points:

- High contrast and readable fonts matter more than decorative styling.
- One main idea per slide reduces overload.
- Meaningful slide titles outperform generic section labels.
- Presenter notes should hold supplemental explanation while the slide stays audience-facing.

## Core Defaults

Use these defaults unless the task or brand clearly calls for something else:

- One main idea per slide.
- Informative titles instead of generic labels like `Overview` or `Results`.
- Stable color semantics across the whole deck.
- Clear visual hierarchy: title, main evidence, takeaway, supporting details.
- Adequate whitespace instead of squeezing more text into the slide.
- Audience-facing visible text and presenter-facing speaker notes.
- Internal production metadata such as slide ids stays off the visible slide unless explicitly requested.

## Readability

Common public guidance suggests:

- `16:9` is a safe default.
- Sans serif fonts are safer than decorative fonts for projected slides.
- Very small text should be treated as a layout problem, not a typography trick.
- For projected talks, headings around `32pt` to `44pt+` and body text around `24pt` to `32pt+` are safer than tiny text.
- For dense business decks viewed on laptops, text can go smaller, but visible text below about `18pt` should trigger scrutiny.

Do not hard-code one universal font size rule. Use context:

- Large-room talk: optimize for projection and distance.
- Screen-shared business review: optimize for laptop readability.
- Handout-only appendix: smaller text may be acceptable, but still keep hierarchy clear.

## Layout

- Prefer one dominant visual or one dominant argument zone per slide.
- Align repeated elements rigidly.
- Use cards, chips, footers, and captions carefully; they are common overflow traps.
- If a slide needs too much explanation to be understood, rework the slide before writing even more notes.
- If a slide routinely exceeds about one minute of speaking time, check whether it should be split.
- Summary, takeaway, limitation, and closing-adjacent pages should stay in the audience's working language by default; avoid long secondary-language paragraphs unless the user explicitly wants them.

## Code And Terminal Text

- Render code snippets, inline code labels, shell commands, filenames shown as code, and other code-like visible text in a monospaced font by default.
- Keep normal prose, slide titles, and explanatory captions in the deck's regular body font unless the user explicitly wants a code-heavy aesthetic.
- Use monospaced text consistently across the deck so examples, indentation, and punctuation stay legible.
- If code is shown inside cards or callouts, do not silently fall back to the body font just because the surrounding component is not a dedicated code block.

## Formulas And Notation

- Important formulas should appear on-screen when they carry the slide's main claim, method definition, or evidence.
- Do not drop an unexplained formula into the visible slide; pair it with a conclusion sentence, symbol legend, or tightly adjacent explanation.
- Prefer compact readable formulas in the main deck over full paper notation when the full expression would break readability.
- Move boundary conditions, secondary indices, and derivation details into speaker notes or appendix when they are not needed on-screen.
- Reserve more height for formulas than for ordinary text, especially when sums, limits, stacked subscripts, or long function names are involved.
- If a formula is tied to a diagram or pipeline, align symbol names with the visible modules so the audience does not have to translate between two vocabularies.
- Formula rendering must be checked on the actual review path; some backends or viewers render PowerPoint equations larger than expected.

## Overflow Repair Order

When text overflows or wraps badly, prefer this order:

1. Remove presenter-only text from the visible slide
2. Shorten the audience-facing wording
3. Widen the text container and any related background shape together
4. Rework the layout so the slide carries less simultaneous content
5. Reduce font size slightly only if hierarchy and readability survive
6. Split the slide if the content still does not fit cleanly

## Evidence Slides

- Charts, screenshots, and tables are evidence, not decoration.
- Crop and enlarge the part that matters rather than pasting full-page source images by default.
- Highlight the exact region or number being discussed.
- Do not let highlight boxes or labels cover the evidence they are meant to explain.
- If a source table is readable after cropping and enlarging, prefer that over needless redrawing.
- Redraw only when the cropped source still fails readability or emphasis needs.

## Audience View vs Speaker View

Visible slide content must stay audience-facing.
Speaker notes can stay presenter-facing.

Bad visible text:

- `s01-cover`
- `先讲背景，再讲问题`
- `这一页主要强调 ROI`
- `下一页再展开技术细节`

Good visible text:

- `Manual approval adds 3 days of delay`
- `ROI turns positive in month 7`
- `Latency drops after prefix caching`

Good speaker note:

- `先用一句话提醒听众这是流程瓶颈页，再按左到右解释 3 个审批节点，最后落到“延迟主要来自手工交接”。`

## Speaker Notes

When the deck is meant to be presented live:

- Notes should be speakable, not just fragments.
- Notes should explain transitions, caveats, and interpretation that do not belong on-screen.
- Notes should not contradict the visible slide.
- Notes may contain presenter cues such as pacing or pointing order.
- When notes are part of delivery, the final `.pptx` must actually contain them; guide-only notes are not enough.

## Spoken Deck Defaults

For spoken decks, especially research talks, project readouts, and training sessions:

- Start with a real opening slide, not a content dump.
- End with a real closing slide, not a last-minute extra content page.
- Keep summary and closing separate when both are needed.
- Use notes to control transition logic instead of pushing that logic into visible footers or chips.

## Frequent Failure Modes

- Titles that say too little
- Text walls that mirror the script
- Tiny tables that no one can read
- Colors that change meaning from slide to slide
- Captions or footers that contain presenter-only directions
- Internal ids or routing labels leaking into audience-facing content
- Code examples or command text rendered in proportional body fonts so punctuation and indentation become harder to read
- Important formulas left only in notes even though the audience needs them on-screen
- Formula bands sized like one-line body text, causing clipped limits or oversized display math
- Summary or closing-adjacent slides carrying long visible text in the wrong audience language when that content should be spoken from notes
- Layouts that only work for one exact text length

## Public Guidance That Informed This Reference

- Microsoft Support on readable slide text and use of speaker notes
- ASHG accessibility guidance for presentations
- USU slide design guidance
- UCSD research-based presentation design guidance
- MIT Comm Lab research slide-design guidance
