# Production Loop

Use this reference whenever the deck is expected to survive more than a single draft.

## Canonical Loop

Treat the following chain as the default production loop:

```text
PPT_GUIDE.md
    ->
generate_ppt.js / generate_ppt.py
    ->
deck.pptx
    ->
rendered PDF / PNG review artifacts
    ->
review/notes.md
    ->
guide updates, generator updates, or both
    ->
rerender
```

Do not skip links in this chain unless the task is explicitly a throwaway mockup.

## Step 1: Inspect And Set Constraints

Start by collecting:

- Audience and objective
- Slide budget or duration
- Style or template constraints
- Source materials
- Existing backend and repo structure
- What counts as done

If the task is a revision, inspect the current guide, generator, deck, and review notes before changing anything.

## Step 2: Write Or Repair `PPT_GUIDE.md`

Use the guide to freeze intent before chasing layout.

At minimum, make the guide answer:

- What is the deck trying to achieve
- What each slide should say
- What belongs on-screen
- What belongs in speaker notes
- What visual evidence or assets are needed
- What acceptance checks must pass

If the deck already exists but the guide does not, reconstruct a minimal guide first.

## Step 3: Implement The Generator

Implement the deck in `generate_ppt.js` or `generate_ppt.py`.

Generator responsibilities:

- Translate the guide into editable slide elements
- Keep slide order and ids aligned with the guide
- Maintain layout and theme consistency
- Populate speaker notes where the backend supports them
- Produce the same deck again on rerun

Do not treat the exported `.pptx` as the primary editing surface.

## Step 4: Generate The Deck

Always regenerate from source after guide or generator changes.

Typical output:

- `deck.pptx`
- Optional cached assets under `assets/`
- Optional intermediate render products

## Step 5: Render For Review

Visual review requires rendered output.

Preferred stable route:

1. Convert `.pptx` to PDF with `soffice --headless --convert-to pdf`
2. Convert the PDF to page images with `pdftoppm`
3. Review the PNGs page by page, or only the specified pages when the fix is local

Use `scripts/render_review.py` when you want this path wrapped in one command.

If the environment already offers a better render path through another skill or toolchain, use it, but still review the rendered result.

## Step 6: Review And Log Issues

Review rendered output with the assumption that problems exist.

Check for:

- Overflow, clipping, collision, or awkward wrapping
- Weak hierarchy or unclear reading order
- Tiny or unreadable charts, tables, and screenshots
- Misaligned spacing and margins
- Incorrect or stale content after edits
- Speaker notes that no longer match the slide

Write findings to `review/notes.md` with slide ids and routing labels.

## Step 7: Route Issues Back To Source

Use this rule:

- Narrative, message, scope, timing, or slide-order problems -> `PPT_GUIDE.md`
- Layout, spacing, cropping, font, and rendering problems -> `generate_ppt.*`
- Issues that change both meaning and implementation -> both

Never close a comment only in the exported deck if the real fix belongs upstream.

## Step 8: Rerender

After changes:

1. Rebuild the deck
2. Render again
3. Re-check the affected slides
4. Close the issue only after the new render passes

Do at least one real fix-and-rerender cycle before claiming the workflow is working.

## Delivery Rule

Before delivery:

- Ensure the guide, generator, and rendered deck agree with each other
- Ensure review notes are either closed or clearly deferred
- Ensure the latest render is the one you actually inspected

If you cannot render the deck in the current environment, say so explicitly and do not pretend that review is complete.
