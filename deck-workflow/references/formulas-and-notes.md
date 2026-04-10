# Formulas And Speaker Notes

Use this reference when a deck contains important formulas, mathematical notation, complex symbolic definitions, or when the final `.pptx` must contain speaker notes that a presenter can read directly.

The rules here generalize lessons from real paper-reading deck iterations: important formulas were initially hidden or represented as plain text, `speaker notes` existed in the guide but not in the final deck, and some formula objects rendered differently through LibreOffice than expected from source coordinates.

## Core Contract

- Important formulas that carry the argument should usually be visible in the main deck, not hidden only in narration or notes.
- Not every formula belongs on-screen; formulas that are not needed for the audience's next step can move to notes, appendix, backup, or a verbal explanation.
- Any formula that appears on-screen must have an audience-facing explanation of what it answers, what the key symbols mean, and what changes relative to the baseline or intuitive version.
- `PPT_GUIDE.md` is the authority for notes. The generator should not invent speaker notes unless the guide explicitly allows a notes supplement.
- If the final deck is meant to be speakable, speaker notes are a deliverable, not optional metadata.
- Formula pages and notes-heavy decks require both structural checks and rendered visual review.

## Deciding Whether A Formula Goes On-Screen

Default to putting a formula in the visible deck when it directly defines:

- A paper's or product's central method.
- A training objective, loss, scoring rule, recurrence, update rule, or routing rule.
- A complexity, latency, cost, or scaling relationship that supports the main claim.
- A symbolic contrast between baseline and proposed method.
- A notation system that the audience must understand before later figures, tables, or diagrams make sense.

Default to keeping a formula out of the main deck when:

- It is only a derivation detail.
- It is needed for rigor but not for the audience's mental model.
- The full expression would dominate the slide without changing the takeaway.
- A diagram, table, or short verbal description carries the point better.
- It belongs in backup, appendix, or presenter notes for Q&A.

When uncertain, put the core skeleton on-screen and move boundary conditions, secondary indices, derivation details, and caveats into speaker notes.

## Explaining Formulas

Do not place an isolated formula on a slide without orientation.

For each visible important formula, include enough audience-facing context to answer:

- What question this formula answers.
- Which term is the baseline or old behavior.
- Which term is the new mechanism, constraint, weight, or objective.
- Which symbols are inputs, outputs, learned weights, probabilities, masks, states, or aggregation axes.
- What index ranges or summation/expectation scopes matter for understanding.
- Which part corresponds to the visual diagram, module, data flow, or evidence on the same slide.

Minimum visible explanation for an important formula:

- A conclusion title or short takeaway sentence.
- A compact symbol legend for unfamiliar symbols.
- Optional callouts or color mapping that ties the formula to a diagram or table.

Appropriate notes content:

- Full derivation or exact paper wording.
- Boundary conditions and secondary index definitions.
- Speaking order, pointer cues, and caveats.
- Why a compact main-deck version is equivalent to the fuller expression.

## Formula Layout Rules

Treat formulas as high-risk layout objects.

- Do not estimate formula height like ordinary one-line body text.
- Reserve extra vertical space for summations, limits, stacked fractions, multi-layer subscripts, expectations, and long function names.
- Prefer a dedicated formula band, card, or column when the formula drives the slide.
- For two related formulas, prefer stacked rows with enough leading over cramming both into one line.
- If a display-style formula renders too large, try a compact inline form, split the formula, enlarge the container, or move secondary terms into notes.
- If a formula shares a slide with a figure or table, explicitly align the formula terms with the visual elements.
- Put symbol explanations near the formula when the audience needs them; do not hide every symbol in notes.
- On summary, takeaway, limitation, and closing-adjacent pages, keep visible formula references short. Long secondary-language explanations should move to notes unless the audience expects them.

Rendered review must check:

- Formula not clipped, overlapped, or pushed out of its background shape.
- Subscripts, superscripts, summation limits, and long identifiers remain readable.
- Formula size matches page hierarchy and is not visually louder than the title.
- Formula container has normal inner padding.
- Formula still renders correctly through the actual review path, especially `.pptx -> PDF -> PNG`.

## Guide Requirements

For decks that may be generated automatically, the guide must be detailed enough that the generator does not invent formula placement, wording, or notes policy.

At deck level, record:

- Whether the final `.pptx` must embed speaker notes.
- Whether notes equal only the read-aloud script or the script plus explicitly marked supplements.
- The primary audience language for visible text.
- Any pages where formulas are required, optional, or explicitly deferred to notes/backup.

At slide level, include formula-related fields when relevant:

- `formula_requirements`: The expression, compact-vs-full choice, source, and rendering preference.
- `symbol_explanations`: Which symbols must be visible and which can stay in notes.
- `formula_layout`: Formula band, left column, right column, bottom strip, stacked rows, or appendix.
- `formula_speaking_order`: What the audience should look at first and how the presenter should explain the expression.
- `notes_supplement`: Extra cues that should be appended to notes beyond the read-aloud baseline.
- `acceptance_checks`: Formula rendering and notes checks specific to the slide.

Recommended stable slide block for spoken decks:

```text
### sNN-slide-role

- Target Duration: `...`
- Cumulative Time: `...`
- Title: `...`
- Subtitle: `...`
- Message: `...`
- Visible Text:
  - `...`
- Visuals:
  - `...`
- Formula Requirements:
  - `None` or `...`
- Symbol Explanations:
  - `None` or `...`
- Speaker Notes:
  - `...`
- Notes Supplement:
  - `None` or `...`
- Implementation Notes:
  - `...`
- Generator-Ready Instructions:
  - `...`
- Acceptance Checks:
  - `...`
```

For Chinese paper readings or other Chinese spoken decks, `可直接念的完整台词` should be a stable field name. Use `notes 补充` for additional cues instead of mixing them into unrelated sections.

## Speaker Notes Contract

When the final deck needs embedded notes:

- Every slide must have notes unless the guide explicitly marks the slide as no-notes.
- The note baseline should come from `PPT_GUIDE.md`.
- Notes should be complete, speakable sentences for live presentations.
- Notes may contain presenter-facing cues, pointing order, timing, and caveats.
- Notes must not contradict visible slide content.
- If visible text changes, update the notes or explicitly confirm they still match.
- Slide count, guide notes count, and final notes count must match unless the guide explicitly defines an exception.
- The final `.pptx`, not an intermediate deck, must be validated for notes.

Avoid these failure modes:

- Notes exist only in `PPT_GUIDE.md`, not in the final deck.
- Notes exist in memory during generation but no `ppt/notesSlides/notesSlide*.xml` parts are present after save.
- Only the first few slides have notes.
- Notes are shifted by one page after a slide insertion or deletion.
- The generator invents notes that no longer match the guide.
- A summary or takeaway page uses long visible text that should have been notes.

## Python Generator Guidance

`python-pptx` is useful for Python-based pipelines, but it does not expose a stable high-level equation API. When important formulas need editable PowerPoint-native math, a practical path is to inject Office Math / OMML XML into a paragraph.

Use this pattern carefully:

- Prototype one small formula first and inspect the resulting `.pptx` XML and rendered PDF.
- Encapsulate XML construction in helpers rather than scattering raw XML through slide functions.
- Keep semantic formula helpers separate from low-level XML helpers.
- Escape plain text inserted into XML.
- Keep formula placement dimensions configurable for high-risk formula slides.
- Render after every formula implementation change.

Recommended helper split:

- Low-level fragments: `_m_run(...)`, `_m_sub(...)`, `_m_sup(...)`, `_m_sum(...)`, `_wrap_math(...)`.
- Insertion helper: `add_native_equation(slide, left, top, width, height, expr_xml, ...)`.
- Semantic helpers: `loss_equation_main()`, `problem_equation_one()`, `full_method_equation_two()`.
- Slide builders: call only semantic helpers and insertion helpers, not raw XML literals.

A compact native-equation insertion helper usually follows this shape:

```python
from pptx.oxml import parse_xml

def add_native_equation(slide, left, top, width, height, expr_xml):
    box = slide.shapes.add_textbox(left, top, width, height)
    paragraph = box.text_frame.paragraphs[0]
    paragraph.clear()
    paragraph._p.append(parse_xml(wrap_math(expr_xml)))
```

The exact XML can vary by formula, but the workflow should not vary: build a minimal proof, encapsulate helpers, integrate into page functions, generate, render, review, and fix.

## Python Notes Persistence

For Python-generated decks, do not assume that touching `slide.notes_slide` during initial construction proves notes are persisted in the final `.pptx`.

Use a two-stage save by default for notes-heavy Python decks:

```python
notes = extract_notes_from_guide(PPT_GUIDE)
prs = Presentation()
build_all_slides(prs)
prs.save(OUTPUT)

notes_prs = Presentation(OUTPUT)
apply_speaker_notes(notes_prs, notes)
notes_prs.save(OUTPUT)
```

Then validate at three levels:

- Reopen with `python-pptx`: every expected slide has `has_notes_slide` and non-empty note text.
- Inspect the `.pptx` zip: `ppt/notesSlides/notesSlide*.xml` count matches the slide count.
- Compare notes text against the guide: no missing pages, shifted pages, or unauthorized generator-written additions.

Recommended generator log fields:

- Final deck path.
- Slide count.
- Parsed guide notes count.
- Final `notesSlides` part count.
- First/last or all-page note comparison status.
- Formula pages and other high-risk pages requiring manual visual review.

## JavaScript Generator Guidance

For JavaScript/PptxGenJS decks, keep the same guide and review contract:

- Use `slide.addNotes(...)` or the project's established notes helper when notes matter.
- Keep notes text traceable to `PPT_GUIDE.md`.
- Validate that generated notes still align with slide count and guide content.
- If the chosen JS stack or the official `$slides` skill provides a stable formula/equation path, use it for important formulas.
- If native formula support is not reliable, use a deterministic fallback such as a generated SVG/PNG asset with a recorded source expression and a visible symbol legend.
- Do not use plain proportional text to fake complex formulas when the audience must read subscripts, superscripts, sums, or expectations.

## Review And Sign-Off

For formula or notes changes, review must cover four categories:

- Structure: slide count, output path, deck filename, expected formula pages, and `notesSlides` part count.
- Content: guide, visible slide text, formula expression, symbol explanations, and notes agree.
- Visual: rendered PDF/PNG shows formulas, labels, diagrams, and summary pages correctly.
- Speaking: notes are complete, aligned with slide order, and checked with timing tools when a duration target exists.

Automatic checks can verify structure and note persistence. They cannot replace rendered visual review for formulas.

If any of these conditions fail, the deck is not done:

- Important formula is missing from the slide when the guide requires it.
- Formula is present but unexplained.
- Formula object renders too large, too small, clipped, shifted, or inconsistent with page hierarchy.
- Notes are absent from the final `.pptx`.
- Notes count differs from slide count without an explicit guide exception.
- Notes text contradicts or lags behind the visible slide.
- Summary, takeaway, limitation, or closing-adjacent pages show long secondary-language prose that should be notes.

