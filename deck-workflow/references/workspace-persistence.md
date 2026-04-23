# Workspace Persistence

Use this reference when deciding where deck artifacts should live.

## Default Rule

Create the deck workspace inside the user's repo or another durable project directory.

Do not treat temp directories as the primary home of:

- `PPT_GUIDE.md`
- `generate_ppt.js` or `generate_ppt.py`
- `deck.pptx`
- `assets/`
- `review/notes.md`

Temp directories are acceptable only for:

- Scratch renders
- Throwaway experiments
- One-off conversions that are immediately copied back into the real workspace

## Why This Matters

The workflow only becomes maintainable if the source artifacts persist after the agent session ends.

If the guide and generator live only in a transient agent directory:

- Later revisions start from scratch
- Human feedback cannot be routed cleanly
- The `.pptx` becomes the accidental source of truth
- Review notes and asset provenance are lost

## Preferred Layout In A User Repo

For a dedicated deck repo:

```text
repo/
└── deck-name/
    ├── PPT_GUIDE.md
    ├── generate_ppt.py
    ├── deck.pptx
    ├── assets/
    ├── rendered/
    └── review/
        ├── notes.md
        └── commands.md
```

For an existing product or research repo:

```text
repo/
└── presentations/
    └── q2-qbr/
        ├── PPT_GUIDE.md
        ├── generate_ppt.js
        ├── deck.pptx
        ├── assets/
        ├── rendered/
        └── review/
```

## Placement Rules

- If the user already has a repo for the project, put the deck workspace there.
- If the user already has a maintained deck workspace, modify it in place.
- If the task belongs to one source artifact or one paper/project, keep the guide and generator beside that artifact rather than in a global `tools/` folder.
- Put only cross-project helpers in shared tooling directories.

## Review Artifact Policy

Rendered outputs can be kept under the workspace if they are part of the ongoing review loop.
If they are too large or too noisy for version control, keep the commands and paths stable even if the PNGs themselves are not committed.

## Validator Placement

Keep the `scripts/validate_deck.py` command pattern discoverable from the workspace's `review/commands.md`. The validator is cheap to run, catches the common handoff failures (wrong slide count, missing `notesSlides` parts, empty notes), and complements the visual review path rather than replacing it.
