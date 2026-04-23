# Change Routing

Use this reference to decide where a requested change should land first.

## Edit the Guide First

Route to `PPT_GUIDE.md` first when the request changes:

- Deck goal or audience.
- Storyline, emphasis, or persuasive framing.
- Slide order or page budget.
- What each slide is trying to say.
- Which facts, quotes, metrics, or examples belong on-screen.
- Speaker notes or timing.
- Whether important formulas belong on-screen, in notes, or in appendix.
- Which audience language visible text should use on summary or closing slides.

Examples:

- "The opening is too technical for execs."
- "Combine these two method slides."
- "Shift the deck from feature overview to decision memo."
- "Add a slide comparing option A and B."

## Edit the Generation Script First

Route to `generate_ppt.*` first when the request changes:

- Layout, spacing, alignment, and typography.
- Cropping, sizing, image placement, and highlight boxes.
- Theme implementation that is already decided in the guide.
- Overflow, collisions, contrast, and clipping.
- Animation order that does not change the slide's message.
- Formula rendering, equation object sizing, or notes persistence bugs in the exported deck.

Examples:

- "The chart title is cut off."
- "Move the screenshot higher."
- "The footer is too small."
- "This slide needs more whitespace."
- "The equation is clipped in the PDF render."
- "The final deck has no speaker notes even though the guide does."

## Edit Both

Edit both artifacts when the request changes both meaning and implementation.

Examples:

- "Turn this dense results slide into two cleaner slides."
- "Switch from formal board style to lighter workshop style."
- "Replace the table with a three-point takeaway card."
- "Add a new appendix slide using the same theme."

## Existing Decks Without a Guide

If the deck exists but the guide does not:

1. Reconstruct a minimal guide first.
2. Tag each slide with a stable id.
3. Then route subsequent edits using the same rules above.

## Human Review Comments

For human feedback:

1. Map the comment to a slide id.
2. Record the exact requested change in `review/notes.md`.
3. Classify it as `guide`, `script`, or `both`.
4. Make the minimal durable change.
5. Re-render and close the issue only after visual verification.

## Common Routing Shortcuts

Use these quick mappings when triaging review comments:

- "This slide says the wrong thing" -> `guide`
- "This slide is too dense" -> usually `both`
- "The title wraps badly" -> `script`, unless the wording itself should change
- "The conclusion should move earlier" -> `guide`
- "The chart is unreadable" -> `script`, sometimes `both` if the slide needs a different evidence strategy
- "The equation should be on the slide, not only in the notes" -> usually `guide`, sometimes `both`
- "The notes do not match the guide anymore" -> usually `script`, sometimes `both` if the guide must change too
- "We need a stronger opening for this audience" -> `guide`
- "This page should become two pages" -> `both`
- "This chip/card has a long English term that is wrapping ugly" -> usually `script` for container sizing, sometimes `guide` when the right fix is shortening the wording
- "The highlight is covering the numbers it is highlighting" -> `script`, via outline box, label placement, or z-order
- "The summary slide has a paragraph of English on a Chinese talk" -> usually `guide`, with the prose moved into speaker notes
- "Notes are missing from the final deck even though the guide has them" -> `script` for notes persistence; check two-stage save and `ppt/notesSlides` parts
- "The cropped table is using an old highlight region" -> `script`, via `ensure_*assets()` re-cropping from the source document

## Text Overflow Triage

When a review comment is fundamentally about overflow, wrapping, edge-hugging, or silent font shrinkage, route to the generator and follow the triage ladder in [text-overflow.md](text-overflow.md) instead of picking the fastest visual patch. Ordered preference:

1. Remove presenter-only text from the visible slide and relocate it to speaker notes or the guide.
2. Shorten the audience-facing wording.
3. Enlarge the text container together with its background shape.
4. Rework the local layout.
5. Only then consider a modest font-size reduction that preserves page hierarchy.
6. If needed, split the slide.

Route steps 1 and 6 through `guide` when they change slide intent or slide count. Route steps 2-5 through `script`. Route both when the change alters both wording and implementation.

## Anti-Patterns

Avoid these shortcuts:

- Editing only the exported `.pptx` when the issue should live in source.
- Changing slide order in code without updating the guide.
- Updating visible text in code while leaving contradictory speaker notes in the guide.
- Hiding an audience-critical formula only in notes because the visible slide became crowded.
- Treating "notes exist in memory" as equivalent to "notes were persisted in the final deck file".
- Treating every request as a visual tweak when the real issue is narrative.
