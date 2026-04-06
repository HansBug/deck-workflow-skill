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

Use JavaScript as the fallback path when Python is not practical or when the project explicitly wants to align with the official `$slides` skill.

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
- Keep asset paths deterministic and local to the workspace.

## Review Commands

Typical commands:

```bash
node generate_ppt.js
soffice --headless --convert-to pdf --outdir rendered deck.pptx
pdftoppm -png rendered/deck.pdf rendered/slide
```

If the official `$slides` skill is available, also use its render and validation scripts.

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
