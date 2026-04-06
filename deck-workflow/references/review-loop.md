# Review Loop

Use this reference whenever the deck has moved beyond outline-only work.

## Mandatory Review Sequence

Run this sequence for every substantial iteration:

1. Update `PPT_GUIDE.md`, `generate_ppt.*`, or both.
2. Regenerate the deck file from source.
3. Render the deck to PDF or per-slide images.
4. Inspect the rendered output.
5. Record findings in `review/notes.md` with slide ids and routing labels.
6. Fix the right source artifact.
7. Re-render.
8. Re-check the affected slides and any nearby slides likely to regress.

Do not skip directly from source edits to "done".

## What Counts As Real Review

A real review inspects rendered output, not just source code.

Acceptable review artifacts:

- PDF exported from the deck
- Per-slide PNG or JPG renders
- A contact sheet or montage built from those renders

Weak substitutes:

- Shape trees or XML only
- Raw markdown extracted from a deck
- Console logs without visual review
- Looking only at `PPT_GUIDE.md` or `generate_ppt.*`

## Recommended Commands

Preferred stable review path:

```bash
python path/to/render_review.py deck.pptx --output-dir rendered
```

This path converts `.pptx` to PDF first, then rasterizes the PDF to per-slide PNG files. Review those images directly. When only a few slides changed, render only the affected pages.

Manual equivalent:

```bash
# 1. Build the deck
node generate_ppt.js
# or
python generate_ppt.py

# 2. Render the PPTX to PDF
soffice --headless --convert-to pdf --outdir rendered deck.pptx

# 3. Convert PDF pages to PNG
pdftoppm -png rendered/deck.pdf rendered/slide
```

If the official `$slides` skill is available, also use its render and validation utilities.

## Minimum Visual Checklist

Check at least these items:

- No unintended overlap, clipping, or out-of-bounds content
- No awkward wrapping in titles, chips, callouts, captions, or footers
- Enough margin from slide edges
- Consistent alignment and spacing
- Sufficient contrast for text and key visuals
- Main chart, table, or screenshot is readable without zooming
- Highlights or labels are not covering the thing they are meant to explain
- Speaker notes still match the implemented slide

## Minimum Content Checklist

Check at least these items:

- Slide order still matches the guide
- Visible text still matches the intended message
- Key numbers, names, labels, and claims are accurate
- Human feedback has actually been incorporated
- The generator did not silently drift away from the guide

## Review Logging

Record findings in `review/notes.md` using stable slide ids.

For each issue, capture:

- Slide id
- Short description
- Severity or urgency if relevant
- Routing label: `guide`, `script`, or `both`
- Status: `open`, `closed`, or `deferred`

## Exit Rule

Do not call the deck done until:

- The requested changes are implemented in the right source artifact
- A fresh render has been reviewed
- The new render does not show obvious regressions
- Open review issues are either closed or explicitly deferred
- You have completed at least one real fix-and-rerender cycle for non-trivial work
