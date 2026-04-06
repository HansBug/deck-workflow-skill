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
3. Set metadata, layout, theme, and reusable helpers near the top of `generate_ppt.js`.
4. Implement slide builders in guide order.
5. Keep audience-facing text on the slide and move presenter-only explanation into speaker notes with `slide.addNotes(...)`.
6. Build `deck.pptx`, render it, inspect the output, log issues in `review/notes.md`, and rerender after fixes.

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
- Keep slide ids in comments or function names so review findings map back cleanly.
- Keep internal ids such as `s01-cover` out of visible slide text unless the user explicitly requests them.
- Keep routing labels, TODOs, and other maker-only metadata out of the audience view.
- Add speaker notes through `slide.addNotes(...)` when presenter guidance matters.
- Keep asset paths deterministic and local to the workspace.

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
- No presenter-only text, internal slide ids, or workflow labels visible on the slide
- Slide order and visible text still match `PPT_GUIDE.md`
- Speaker notes still match the implemented slide after edits

## Change Routing

When a human asks for changes:

- Rewrite `PPT_GUIDE.md` first for structure, message, and content changes
- Rewrite `generate_ppt.js` first for layout and rendering fixes
- Rewrite both when the slide's message and implementation both change

## Failure Modes To Watch

- The guide changes but generator text stays stale
- Slide layout is adjusted but no rerender is reviewed
- Visual spacing is tuned for one title length and breaks on a later text change
- Review fixes are applied directly in PowerPoint and not backported into `generate_ppt.js`
- Internal slide ids such as `s01-cover` leak onto the visible slide
- Presenter-only hints or workflow reminders are left in the audience-facing content
