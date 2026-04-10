# Python Generator Guidance

Use this reference when the deck backend is Python.

## When To Choose Python

Prefer Python when:

- The deck project already uses Python
- The workflow depends on `python-pptx`
- The task includes PDF cropping, screenshot prep, or image manipulation with `PyMuPDF` or `Pillow`
- The team is more likely to maintain a Python generator than a JavaScript one

Do not switch a stable JavaScript deck stack to Python without a clear maintenance reason.

Before committing to Python, inspect the environment:

```bash
python path/to/detect_deck_environment.py
```

Python is the preferred default path when the repo can support it.
Do not switch to JavaScript only because the current shell is missing deck packages; try a local virtual environment first.

## Expected Files

Use a workspace like this:

```text
deck-workspace/
├── PPT_GUIDE.md
├── generate_ppt.py
├── requirements.txt
├── assets/
├── rendered/
└── review/
    └── notes.md
```

## Recommended Dependencies

For a practical Python deck workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install python-pptx PyMuPDF Pillow pdf2image
```

If `python-pptx` or related libraries are missing, treat this local `venv` path as the first repair step.
Only move to JavaScript after the Python path is genuinely not practical for the repo.

System tools for real review:

- `soffice`
- `pdftoppm`
- Required fonts for the deck

## Practical Workflow

For a real deck, do the implementation in this order:

1. Confirm `PPT_GUIDE.md` is detailed enough to build from.
2. Create a workspace-local `venv` and install `requirements.txt` if Python deck libraries are missing.
3. Freeze stable slide ids for review and change routing.
4. Parse guide-backed notes and formula requirements before implementing slides that depend on them.
5. Implement helper functions and slide builders in guide order.
6. Keep audience-facing text on the slide and presenter-only explanation in notes or in the guide.
7. If notes must be embedded, save once, reopen the deck, apply notes, save again, and validate the final `.pptx`.
8. Build `deck.pptx`, render it, inspect the output, log issues in `review/notes.md`, and rerender after fixes.

## Generator Structure

Keep the generator explicit and reproducible:

1. Paths, constants, and theme values
2. Guide and notes parsing helpers
3. Asset preparation helpers
4. Text, shape, and formula helpers
5. One slide builder per slide or repeated section
6. Final `build_presentation()` plus validation helpers

Recommended high-level shape:

```python
from pathlib import Path
from pptx import Presentation

OUTPUT = Path(__file__).with_name("deck.pptx")

def build_cover(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    # ...

def build_presentation() -> Path:
    prs = Presentation()
    build_cover(prs)
    prs.save(str(OUTPUT))
    return OUTPUT

if __name__ == "__main__":
    print(build_presentation())
```

## Authoring Rules

- Set slide size explicitly when the default is not safe.
- Keep output filenames stable.
- Keep source text traceable back to `PPT_GUIDE.md`.
- Treat `PPT_GUIDE.md` as the authority for notes policy, formula choice, and audience-facing wording.
- Use `PyMuPDF` for precise PDF crops when tables or figures must be sourced from documents.
- Use `Pillow` for image sizing and raster prep.
- Keep helper functions small enough that later layout fixes remain local.
- Populate speaker notes when the deck contract requires them, and validate the final `.pptx` rather than only the in-memory object.
- Render code snippets, terminal commands, inline code labels, and other code-like visible text in a monospaced font rather than the normal body font.
- Keep stable slide ids in function names, comments, and review notes rather than visible slide text unless explicitly requested.
- Keep TODOs, routing labels, and other maker-only metadata out of the visible slide.
- If an important formula must be on-screen, do not fake it with plain proportional text when readable subscripts, superscripts, sums, or expectations matter.

## Speaker Notes Contract

When the final deck must embed speaker notes:

- Extract notes from `PPT_GUIDE.md` rather than rewriting them ad hoc in slide builders.
- Treat the guide's read-aloud text as the minimum note baseline.
- Add extra cues only when the guide explicitly allows a `notes_supplement` or equivalent field.
- Keep slide count, guide note count, and final note count aligned.
- Re-run notes validation whenever slide order, page count, or script text changes.

Recommended helper shape:

```python
def extract_notes_from_guide(guide_path: Path) -> list[str]:
    ...

def apply_speaker_notes(prs: Presentation, notes: list[str]) -> None:
    ...

def validate_notes_written(output: Path, expected_count: int) -> None:
    ...

def validate_notes_against_guide(output: Path, notes: list[str]) -> None:
    ...
```

Do not scatter note-writing logic across every `slide_*` function.

## Two-Stage Save Pattern For Notes

Do not assume that touching `slide.notes_slide` during initial generation proves notes will persist in the saved file.

For Python-generated decks, default to this pattern:

```python
notes = extract_notes_from_guide(PPT_GUIDE)

prs = Presentation()
build_all_slides(prs)
prs.save(OUTPUT)

notes_prs = Presentation(OUTPUT)
apply_speaker_notes(notes_prs, notes)
notes_prs.save(OUTPUT)

validate_notes_written(OUTPUT, len(notes))
validate_notes_against_guide(OUTPUT, notes)
```

At minimum, validate three things:

- Reopening the final deck shows notes on the expected slides.
- The `.pptx` zip actually contains `ppt/notesSlides/notesSlide*.xml`.
- Note text still matches the guide and has not shifted by one page after edits.

## Native Formula Guidance

`python-pptx` does not provide a stable public high-level equation API. If the deck needs PowerPoint-native equations, a practical Python path is to inject Office Math / OMML XML into a paragraph.

Keep the implementation layered:

- Low-level XML helpers such as `_m_run(...)`, `_m_sub(...)`, `_m_sup(...)`, `_m_sum(...)`, and `_wrap_math(...)`.
- An insertion helper such as `add_native_equation(...)`.
- Semantic helpers such as `problem_equation_one()` or `loss_equation_main()`.
- Slide builders that call only the semantic helpers and insertion helper.

Recommended insertion shape:

```python
from pptx.oxml import parse_xml

def add_native_equation(slide, left, top, width, height, expr_xml):
    box = slide.shapes.add_textbox(left, top, width, height)
    paragraph = box.text_frame.paragraphs[0]
    paragraph.clear()
    paragraph._p.append(parse_xml(wrap_math(expr_xml)))
```

Use a minimal prototype before integrating a new formula family into the real generator. Then generate and render the full deck again. Formula support is not done until the rendered result passes review.

## Formula Layout And Render Risks

Treat formula pages as special review targets.

- Reserve more vertical space than a normal body-text strip would suggest.
- Expect `soffice` or LibreOffice to render some PowerPoint equations larger than PowerPoint itself would.
- Prefer compact inline forms or stacked two-line formulas when display math becomes oversized.
- Parameterize formula-band height and neighboring card heights on formula-heavy slides.
- Keep symbol explanations near the formula when the audience must read them.
- Re-render after every formula edit, even if the XML diff looks small.

## Validation Helpers

Real deck generators should expose explicit validations rather than relying on "script exited successfully".

Useful checks include:

- `validate_slide_count(...)`
- `validate_required_assets(...)`
- `validate_notes_written(...)`
- `validate_notes_against_guide(...)`
- `validate_formula_pages_declared(...)` or another helper that lists formula pages requiring manual visual review

Generator logs should make review easier by printing:

- Final deck path
- Slide count
- Parsed guide-notes count
- Notes-slide count
- Pages that contain formulas or other high-risk layout objects
- Any pages requiring manual render review because of formula density, long secondary-language visible text, or summary/closing risk

## Review Commands

Typical commands:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python generate_ppt.py
soffice --headless --convert-to pdf --outdir rendered deck.pptx
pdftoppm -png rendered/deck.pdf rendered/slide
```

If the environment has another approved render path, use it, but still review the rendered output.

## Change Routing

When a human asks for changes:

- Rewrite `PPT_GUIDE.md` first for narrative, content, structure, and timing changes
- Rewrite `generate_ppt.py` first for layout, crop, font, and spacing fixes
- Rewrite both when the requested change affects both slide meaning and implementation

## Failure Modes To Watch

- Reusing cached asset crops after the guide changes what needs to be highlighted
- Fixing layout by shrinking fonts too far instead of revising the slide
- Updating visible text in code while leaving stale speaker notes in the guide
- Guide notes changed but the final `.pptx` still contains stale notes from a previous run
- Assuming `slide.notes_slide` access means notes were persisted even though no `notesSlides` parts exist in the saved deck
- Using plain text to mimic a formula that the audience actually needs to read
- PowerPoint-native formulas that render acceptably in source coordinates but blow up after `.pptx -> PDF -> PNG`
- Summary or takeaway pages that quietly accumulate long secondary-language visible text that belongs in notes
- Claiming review is done after only looking at object trees or logs
- Falling back to JavaScript immediately even though a local `venv` would have been enough
- Code-like visible text silently rendered in the body font, making indentation, punctuation, or examples harder to read
- Internal slide ids such as `s01-cover` leaking onto the visible slide
