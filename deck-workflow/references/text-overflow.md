# Text Overflow And Container Bleed

Use this reference whenever visible slide text risks wrapping unnaturally, escaping a background shape, hugging a container edge, or being shrunk until the hierarchy collapses.

Real-world deck work shows that "text doesn't quite fit" is rarely a single symptom. It is a family of failures that need disciplined triage instead of ad-hoc font shrinking.

## High-Risk Components

Treat these as overflow-risk by default whenever they hold visible text:

- Slide titles, especially with mixed Chinese-English words or long system/model names
- Kicker or subtitle strips directly under a title
- Top conclusion bars or one-line banners
- Fixed-width chips, pills, badges, labels, status tags
- Number cards, KV cards, mini-summary cards
- Image captions and figure annotation strips
- Footer bars, watermark strips, pagination lines, any bottom micro-bar
- Right-column summary cards inside two-column layouts
- Table callouts, comparison-row headers, color-coded legend tags

Fixed-width components that must hold long English words, acronyms, hyphenated phrases, or mixed Chinese-English text are the highest-risk of all. Do not assume a width that "usually worked" will keep working after a text change.

## Failure Definitions

When inspecting a rendered slide, treat any of the following as a real overflow failure, not a cosmetic nit:

- A title, chip, strip, or card heading that was meant to be one line renders on two lines
- Text bleeds outside its background rectangle, card, tag, caption strip, or table cell
- Text stays inside the container but hugs an edge, corner, shadow, or border with almost no padding
- Auto-wrapping breaks a phrase, number with unit, model name, benchmark name, or a conclusion at an unnatural point
- Text fits only because font size was dropped below the page hierarchy (title smaller than body, body smaller than chips, chips smaller than the footer, etc.)
- Text fits only because a designer disabled wrapping and let the tail silently clip
- Two adjacent cards or chips look legible individually but their text lengths make them visually misaligned or crowd each other

If any of these is true, the page is not ready to ship, even when the generator script exits cleanly.

## Triage Ladder

When overflow appears, fix in this order. Do not jump to font-shrink first.

1. Check whether the text is presenter-facing. Lines like "先讲 X，再讲 Y", "后面再展开", "下一页再解释", internal slide ids, routing labels, or review-only hints should be removed from the visible slide and moved to speaker notes or the guide.
2. Shorten the audience-facing wording. Keep the conclusion, key number, or key noun; drop hedging, modifiers, and restatements.
3. Enlarge the text container **together with its background shape**. If you only widen the text frame but leave the colored rectangle, card, chip, or caption strip unchanged, the text will look detached or the background will still clip it.
4. Rework the local layout. Options: let the title be shorter and let the right column be wider; swap a side-by-side layout for a stacked one; reduce the number of KV cards; change three small chips into two medium chips.
5. Only now consider a small font reduction, and only if page hierarchy (title > body > chip > footer) still holds. Do not silently enable autofit that pushes text below readable floor sizes.
6. If steps 1-5 cannot keep the content readable and on-hierarchy, split the slide, move the overflow part to a backup slide, or push the excess into speaker notes.

Treat this as an ordered ladder. Steps that touch layout and wording are almost always cheaper than steps that touch typography.

## Component-Specific Fix Preferences

Different components fail and fix differently. When in doubt, pick the first fix that preserves hierarchy.

- Titles, chips, kickers, one-line bars: prefer keeping one line. Shorten the wording first, then widen the container, then split. Font reduction is a last resort because these components define the slide's visual hierarchy.
- Number cards, summary cards, KV cards: prefer enlarging the card and keeping stable inner padding. Do not let the big number and its label size collapse together.
- Captions and figure-annotation strips: prefer shortening sentences and removing modifiers. If still too long, widen the caption band; do not let it tail against the figure edge.
- Right-column summary cards in two-column layouts: prefer reducing line count. Three short bullets that read is better than three full sentences that look compressed. Split into two cards before accepting microscopic text.
- Footer bars, pagination strips: keep them short and audience-facing. Never let presenter cues migrate into the footer just because it has empty space.

## Default Visible-Text Size Floor

Unless the user explicitly wants something smaller, visible text controlled by the generator should not go below roughly `12pt` except for pure page-number style marks or very lightweight footer labels. Titles, body text, chips, captions, number cards, summary cards, and callouts should all sit above that floor.

This is a floor, not a target. Large-room talks usually need considerably larger text than `12pt`.

## Highlight, Mask, And Label Occlusion

Highlight boxes, soft masks, translucent color panels, and emphasis labels ("ours", "best", "key result", "new", "SOTA") must not cover the thing they are meant to emphasize.

Default fixes when a highlight currently occludes important content:

- Switch a filled rectangle to an outline box so the underlying content stays readable.
- Use a thin border or a colored corner tab instead of a full overlay.
- Move the label outside the highlighted region (above, to the side, or into a caption strip) when the interior has no safe empty area.
- Change the z-order so the label sits over the background but below critical numbers or axis labels.
- Reduce overlay opacity only when an outline is not feasible, and still verify the rendered PDF/PNG.

Verify occlusion after every rerender, especially when a label moved automatically because the underlying figure changed size.

## Verification Path

Text overflow cannot be confirmed from source coordinates. A container that looks safe in code often breaks after `.pptx -> PDF -> PNG` rendering, particularly when:

- LibreOffice/`soffice` is the renderer and fonts differ from the deck's declared fonts
- A chip or strip contains a long English word, hyphenated compound, or mixed-language phrase
- A title or summary line was edited since the last render
- A card or column was resized but its siblings were not

Always verify on the actual review path described in `review-loop.md`. Source-side shape inspection does not count as a pass.

## When Overflow Means The Slide Is Wrong

Some overflow problems are really content problems in disguise. Escalate from layout fixes to slide redesign when:

- The slide tries to make more than one main point
- The slide requires heavy narration to be understood
- Bullets are effectively scripts and the script belongs in speaker notes
- Many chips or cards exist to preserve content that nobody will read at projection scale

In these cases, shrinking fonts and widening containers postpones the real fix.
