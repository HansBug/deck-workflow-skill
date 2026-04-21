# Backend Setup

Use this reference when choosing the generator backend and preparing the environment.

## Decision Order

Use this backend order by default:

1. Python if the environment and project support it, or can reasonably be prepared with a workspace-local virtual environment
2. JavaScript only after the Python path is genuinely not practical
3. Another format only if both are unsuitable or the project already has a different stable backend

Also prefer the official `$slides` skill when it is available, especially for PptxGenJS helpers and validation utilities.

## Detect The Environment

Run:

```bash
python path/to/detect_deck_environment.py
```

This inspects:

- Python executable
- Common Python deck libraries
- `node` and `npm`
- `soffice`
- `pdftoppm`

## Python Path

Prefer Python when:

- The repo already uses Python
- `python-pptx` and related libraries are or can be installed
- PDF cropping or image preparation is part of the job
- The deck must embed validated speaker notes and the repo is comfortable maintaining explicit save-and-verify logic
- Important formulas or symbolic notation need a controlled implementation path, even if that means OMML helpers plus extra render validation

Typical setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install python-pptx PyMuPDF Pillow pdf2image
```

Do not treat missing global `python-pptx` imports as an automatic reason to abandon Python.
If the repo is Python-friendly, first try a workspace-local `venv` and install the needed packages there.

Review-path system tools:

```bash
sudo apt-get install libreoffice poppler-utils
```

## JavaScript Path

Use JavaScript when:

- Python is unavailable or remains impractical after trying a workspace-local `venv`
- The project wants to align with the official `$slides` skill
- `node` and `npm` are available

Typical setup:

```bash
npm init -y
npm install pptxgenjs
```

Keep `generate_ppt.js` under source control.

## Review Tools

Regardless of backend, the stable review path is:

1. Generate `.pptx`
2. Convert `.pptx` to PDF with `soffice`
3. Convert PDF to PNG with `pdftoppm`
4. Let the agent inspect those PNGs

If notes are part of delivery, also validate the final `.pptx` itself:

- Notes count matches slide count
- Expected `notesSlides` parts exist
- Sampled or full notes still match `PPT_GUIDE.md`

If formulas are important, expect manual review of the rendered formula pages even after the structural checks pass.

If `soffice` or `pdftoppm` is missing, install them before claiming visual review is complete.

## If Neither Python Nor JavaScript Is Practical

Fallbacks are acceptable, but they are second-class:

- Google Slides or another existing house format
- Manual `.pptx` editing when the source deck already exists
- HTML-to-slides or other custom pipelines

Even then, preserve the same workflow:

- Keep a durable `PPT_GUIDE.md`
- Keep the implementation source in the user's repo
- Keep rendered review artifacts
- Keep change routing explicit
