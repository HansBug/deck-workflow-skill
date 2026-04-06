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
4. Implement helper functions and slide builders in guide order.
5. Keep audience-facing text on the slide and presenter-only explanation in notes or in the guide.
6. Build `deck.pptx`, render it, inspect the output, log issues in `review/notes.md`, and rerender after fixes.

## Generator Structure

Keep the generator explicit and reproducible:

1. Paths, constants, and theme values
2. Asset preparation helpers
3. Text and shape helpers
4. One slide builder per slide or repeated section
5. Final `build_presentation()` that writes the deck

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
- Use `PyMuPDF` for precise PDF crops when tables or figures must be sourced from documents.
- Use `Pillow` for image sizing and raster prep.
- Keep helper functions small enough that later layout fixes remain local.
- Populate speaker notes if the backend path supports them; otherwise keep them faithfully in the guide.
- Render code snippets, terminal commands, inline code labels, and other code-like visible text in a monospaced font rather than the normal body font.
- Keep stable slide ids in function names, comments, and review notes rather than visible slide text unless explicitly requested.
- Keep TODOs, routing labels, and other maker-only metadata out of the visible slide.

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
- Claiming review is done after only looking at object trees or logs
- Falling back to JavaScript immediately even though a local `venv` would have been enough
- Code-like visible text silently rendered in the body font, making indentation, punctuation, or examples harder to read
- Internal slide ids such as `s01-cover` leaking onto the visible slide
