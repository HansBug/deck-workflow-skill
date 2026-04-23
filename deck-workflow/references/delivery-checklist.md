# Delivery Checklist

Use this reference right before you tell the user "the deck is ready" or "the revision is done".

The goal is to prevent the two most common failures at handoff:

- Obvious visual or content bugs being first discovered by the user
- A file that looks finished but is missing speaker notes, cached figures that no longer match the guide, or an unverified render

## Delivery Artifact

Only the final, fully post-processed `.pptx` counts as the delivery artifact.

For Python pipelines that use the two-stage save pattern for speaker notes, that means the `.pptx` file **after** the second save. The intermediate file from the first save - which may have slides but no `ppt/notesSlides` parts - is not acceptable as the delivery file.

Before handoff:

- Confirm the file the user will open is the same file your validator and renderer inspected.
- Do not attach, link, or refer to a temporary, pre-notes, or pre-render intermediate as "the deck".

## Self-Check Before User Review

Obvious bugs should not be the first review material the user sees. Before handing a deck off, run at least one pass of self-review on the rendered output.

The self-check covers four layers:

1. Structure: slide count, file name, existence of `ppt/notesSlides/notesSlide*.xml` parts when notes are required, presence of expected assets.
2. Content: guide and visible slide text agree; formulas the guide marked as on-screen are actually on-screen; pages the guide marked as primary-audience-language are not polluted by long secondary-language prose.
3. Visual: rendered PDF or per-slide PNG shows no overflow, clipping, occlusion, or unreadable tables, figures, and formulas.
4. Speaking: if the deck is spoken, notes exist on every expected slide, match the guide baseline, and the pacing tool agrees with the duration target.

The "3-second rule" is a useful visual heuristic per page:

- Can an audience member tell the main point in about 3 seconds?
- Do they know where to look first?
- Are the key numbers and labels readable at a normal projection scale?

If any answer is no on a content page, the page needs rework, not just a font bump.

## What Counts As "Checked"

A slide is considered visually checked only after it has been rendered to PDF or PNG and inspected. Slide-tree dumps, shape counts, XML traversal, or log lines alone do not count.

A speaker-note deliverable is considered checked only after the final `.pptx` has been reopened and confirmed to:

- Have a notes slide for each expected slide
- Contain the expected `ppt/notesSlides/notesSlide*.xml` parts in the zip
- Match the `PPT_GUIDE.md` notes baseline for at least sampled pages, or fully match when automation is in place

The generator script exiting successfully is not sufficient evidence that the deck is correct.

## Mandatory Fix Targets Before Handoff

Fix these before asking the user to review, instead of surfacing them as "known issues":

- Any visible overflow, clipping, or bleed-out on titles, chips, captions, number cards, KV cards, summary cards, or footer strips
- Highlight boxes or labels covering the content they are meant to emphasize
- Presenter-only hints, slide ids, routing labels, or review metadata still visible on a slide
- Summary, takeaway, limitation, or closing-adjacent slides containing long secondary-language prose that should live in speaker notes
- Required formulas that are missing from the slide, unreadable, or rendered at the wrong visual scale
- Notes that are missing from the final `.pptx` even though the contract said they would be embedded
- Tables that cannot be read at projection scale, especially when the crop came from a cached asset instead of the authoritative source document

If any of these remain, the deck is not ready for handoff.

## Known Failure Modes To Rule Out

Before calling the deck done, confirm none of these apply:

- Stale cached asset: an `assets/` image is reused even though the guide changed what to highlight or crop.
- One-page notes ghost: the first slide has notes but the rest do not; this can happen when a loop short-circuits or a copy-paste leaves stale data.
- First-save handoff: the delivery file is the pre-notes intermediate, not the post-notes `.pptx`.
- Guide-only notes: notes live in `PPT_GUIDE.md` only; the final `.pptx` does not contain `notesSlides` parts.
- Text fits only because autofit collapsed hierarchy: titles and chips have silently dropped below the body font size.
- Obvious language pollution: a Chinese-primary deck's summary or closing slide contains a paragraph of English that was meant to be speaker notes.
- Unverified render: a render was generated but never actually opened for review.
- Formula rendered at display scale: a sum with limits or a long function name is visually louder than the page title after `.pptx -> PDF -> PNG` rendering.

## Recommended Automated Checks

Run the supplied validator or an equivalent before handoff when the deck is more than a throwaway draft:

```bash
python path/to/scripts/validate_deck.py path/to/deck.pptx \
    --guide path/to/PPT_GUIDE.md \
    --expect-notes \
    --expect-slides 17
```

The validator performs a structural and partial-content pass. It confirms, at minimum:

- The `.pptx` opens as a valid zip archive.
- Slide count matches `--expect-slides` when provided.
- With `--expect-notes`, the zip contains one `ppt/notesSlides/notesSlide*.xml` per slide, each slide's `.rels` file points at a notes slide, and no notes text is empty.
- Visible slide XML does not contain production-only ids such as `s01-cover` unless `--allow-visible-ids` is passed.

When a guide path is provided and the guide uses the skill's recommended `### sNN-...` schema, the validator additionally:

- Requires a 1:1 mapping between guide slide blocks and deck slides.
- Samples each guide block for read-aloud text and flags any slide where the guide's read-aloud line is not contained in the deck's notes.
- Reports which guide blocks lacked a recognizable read-aloud field so the reviewer can follow up manually.

The validator deliberately does not attempt to verify slide-to-notes ordering beyond the `.rels` check, nor does it parse custom guide schemas. Treat a clean run as necessary but not sufficient. Rendered PDF or PNG review remains the authoritative check for formula pages, tables, highlight-heavy figures, summary and closing slides, and any case where the guide does not use the default schema.

## Handoff Message Contract

When you report "done" to the user, the message should make clear:

- Which `.pptx` is the final file
- That the final file was rendered and inspected
- That notes (when required) are present in that file, not only in the guide
- Any deferred issues with an explicit note, rather than silent omission
- If the environment could not render the deck, say so plainly and do not claim visual review is complete
