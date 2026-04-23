# JavaScript Generator Guidance

Use this reference when the deck backend is JavaScript.

## When To Choose JavaScript

Prefer JavaScript when:

- The deck is new and no backend is established
- The official `$slides` skill is available
- The team wants to lean on `PptxGenJS`
- The deck needs editable text, shapes, and charts with a layout-oriented workflow

Do not migrate an established Python generator to JavaScript without a concrete benefit.

Before committing to JavaScript, inspect the environment:

```bash
python path/to/detect_deck_environment.py
```

Use JavaScript as the fallback path when Python is not practical after a real attempt to make the Python path work, or when the project explicitly wants to align with the official `$slides` skill.

## Expected Files

Use a workspace like this:

```text
deck-workspace/
├── PPT_GUIDE.md
├── generate_ppt.js
├── package.json
├── assets/
├── rendered/
└── review/
    └── notes.md
```

## Recommended Dependencies

At minimum:

```bash
npm install pptxgenjs
```

If the official `$slides` skill is available, reuse its helpers and validation utilities instead of rebuilding them locally.

## Practical Workflow

For a real deck, do the implementation in this order:

1. Confirm `PPT_GUIDE.md` is detailed enough to build from.
2. Freeze stable slide ids for review and change routing.
3. Parse or otherwise map guide-backed note content and formula requirements before implementing the affected slides.
4. Set metadata, layout, theme, and reusable helpers near the top of `generate_ppt.js`.
5. Implement slide builders in guide order.
6. Keep audience-facing text on the slide and move presenter-only explanation into speaker notes with `slide.addNotes(...)`.
7. Build `deck.pptx`, render it, inspect the output, log issues in `review/notes.md`, and rerender after fixes.

## Generator Structure

Keep the generator explicit and reviewable:

1. Constants and metadata
2. Theme setup
3. Reusable helpers and component builders
4. One slide builder per slide or per repeated section
5. Final `main()` that writes the deck

Recommended high-level shape:

```js
const pptxgen = require("pptxgenjs");

function buildCover(pptx) {
  const slide = pptx.addSlide();
  // ...
}

async function main() {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE";
  // theme, metadata, helpers
  buildCover(pptx);
  await pptx.writeFile({ fileName: "deck.pptx" });
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
```

## Authoring Rules

- Set layout and theme fonts explicitly.
- Keep the output filename stable.
- Keep text content traceable back to `PPT_GUIDE.md`.
- Prefer native editable slide elements over rasterized text.
- Render code snippets, terminal commands, inline code labels, and other code-like visible text in a monospaced font instead of the main body font.
- Keep slide ids in comments or function names so review findings map back cleanly.
- Keep internal ids such as `s01-cover` out of visible slide text unless the user explicitly requests them.
- Keep routing labels, TODOs, and other maker-only metadata out of the audience view.
- Add speaker notes through `slide.addNotes(...)` when presenter guidance matters, and keep that text aligned with `PPT_GUIDE.md`.
- If an important formula must be visible, do not hide it only in notes; use the stack's best reliable equation path or a deterministic asset fallback with recorded source provenance.
- Keep summary, takeaway, and closing-adjacent visible text in the audience's working language unless the user explicitly requests otherwise.
- Keep asset paths deterministic and local to the workspace.

### Slide Function Purity

Keep per-slide builder functions focused on visible content and layout. Do not parse `PPT_GUIDE.md`, run post-build validators, or regenerate source crops from inside a slide builder. Factor those into guide-parsing helpers, asset-preparation helpers, and `validate_*()` functions called from `main()`.

### Centralize Visible Text At The Top Of Each Slide Function

Collect the visible text for a slide into a single object or struct at the top of the builder, then feed it into helpers. When wording changes, the diff should land in one place and the guide-to-deck correspondence should stay obvious.

### Assets Are Candidates, Not Truth

Images under `assets/` are cached candidates, not authoritative sources. When the guide changes what to crop, highlight, or enlarge, regenerate the asset from the source document rather than reusing a stale file, even if the filename still looks right.

## Speaker Notes And Formula Contract

For the full notes and formula contract (including pitfalls around hidden formulas, guide-as-notes-authority, and rendered review), see [formulas-and-notes.md](formulas-and-notes.md).

For JavaScript decks, keep the same high-level contract as Python decks:

- `PPT_GUIDE.md` is the authority for note baseline text.
- The generator should not invent note text beyond explicit guide supplements.
- Slide count, note count, and guide expectations should remain aligned after insertions or deletions.
- If the chosen JS stack or the official `$slides` skill provides a stable formula or equation helper, use it for audience-visible formulas.
- If native-equation support is not reliable in the chosen stack, use a deterministic fallback such as a generated SVG/PNG asset, and still place visible symbol explanations on the slide.

## Review Commands

Typical commands:

```bash
node generate_ppt.js
soffice --headless --convert-to pdf --outdir rendered deck.pptx
pdftoppm -png rendered/deck.pdf rendered/slide
```

If the official `$slides` skill is available, also use its render and validation scripts.

## Review Checklist

Before sign-off, check at least these items in the rendered output:

- No overflow, collision, clipping, or accidental wrap in titles, chips, captions, or code headers
- Important formulas render cleanly, fit their containers, and still have visible symbol explanations
- No presenter-only text, internal slide ids, or workflow labels visible on the slide
- Slide order and visible text still match `PPT_GUIDE.md`
- Code snippets, inline code labels, and terminal-style strings visibly use a monospaced font
- Speaker notes still match the implemented slide after edits
- Summary and closing-adjacent pages do not drift into long off-audience-language visible prose that should live in notes

## Change Routing

When a human asks for changes:

- Rewrite `PPT_GUIDE.md` first for structure, message, and content changes
- Rewrite `generate_ppt.js` first for layout and rendering fixes
- Rewrite both when the slide's message and implementation both change

For cross-cutting rules that apply to every generator, defer to:

- [text-overflow.md](text-overflow.md) for the overflow triage ladder and high-risk component catalog
- [delivery-checklist.md](delivery-checklist.md) for the handoff contract, including the self-check requirement and what counts as a delivery artifact
- [review-loop.md](review-loop.md) for the rendered-review expectations the JS generator must also meet

## Failure Modes To Watch

- The guide changes but generator text stays stale
- The guide notes change but the JS generator still writes old note text
- Slide layout is adjusted but no rerender is reviewed
- Visual spacing is tuned for one title length and breaks on a later text change
- Review fixes are applied directly in PowerPoint and not backported into `generate_ppt.js`
- Internal slide ids such as `s01-cover` leak onto the visible slide
- Presenter-only hints or workflow reminders are left in the audience-facing content
- Important formulas are reduced to unreadable plain text or hidden entirely in notes
