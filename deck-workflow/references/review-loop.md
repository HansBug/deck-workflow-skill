# Review Loop

Use this reference whenever the deck has moved beyond outline-only work.

## Standard Loop

1. Update `PPT_GUIDE.md`, `generate_ppt.*`, or both.
2. Rebuild the deck.
3. Render the deck to reviewable output.
4. Inspect slide images or PDF pages.
5. Record findings in `review/notes.md`.
6. Fix issues.
7. Re-render affected slides or the full deck.
8. Deliver only after the new render passes.

## What Counts as a Real Review

A real review inspects rendered output, not just source code.

Acceptable review artifacts:

- PDF exported from the deck.
- Per-slide PNG or JPG renders.
- A contact sheet or montage built from those renders.

Weak substitutes:

- Shape trees or XML only.
- Raw markdown extracted from a deck.
- Console logs without visual review.

## Minimum Visual Checklist

Check at least these items:

- No unintended overlap or clipping.
- No awkward wrapping in titles, chips, or callouts.
- Enough margin from slide edges.
- Consistent alignment and spacing.
- Sufficient contrast for text and key visuals.
- Main chart, table, or screenshot is readable.
- Speaker notes still match the implemented slide.

## Content Checklist

Check at least these items:

- Slide order still matches the guide.
- Visible text matches the intended message.
- Key numbers, names, and labels are accurate.
- New feedback has actually been incorporated.

## Tooling Notes

- If the official `$slides` skill is available, use its render and validation utilities.
- Otherwise use the existing local toolchain for the deck backend in use.
- Keep review commands and assumptions in the workspace so later iterations are repeatable.

## Exit Rule

Do not call the deck done until:

- The requested changes are implemented in the right source artifact.
- A fresh render has been reviewed.
- The new render does not show obvious regressions.
- Open review issues are either closed or explicitly deferred.
