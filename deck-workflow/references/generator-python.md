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
python3 -m venv venv
source venv/bin/activate
pip install python-pptx PyMuPDF Pillow pdf2image
```

System tools for real review:

- `soffice`
- `pdftoppm`
- Required fonts for the deck

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

## Review Commands

Typical commands:

```bash
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
