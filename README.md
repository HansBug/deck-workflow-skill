# deck-workflow-skill

[中文说明 / Chinese README](./README_zh.md)

`deck-workflow-skill` is a repository for a Codex-compatible skill that treats presentation work as an iterative production loop instead of a one-shot deck export.

The installable skill lives in [`deck-workflow/`](./deck-workflow). The repository adds repo-level documentation, maintenance guidance, and version control around that skill.

## What This Skill Is For

Use this skill when deck work needs to stay editable and reviewable across multiple rounds:

- New presentation creation
- Existing deck restructuring
- Human feedback driven revisions
- Repeated visual QA and incremental fixes
- Workflows that benefit from separating content intent from implementation

The core idea is a standard loop:

1. Write `PPT_GUIDE.md` first.
2. Implement the deck in a generation script.
3. Generate the editable `.pptx`.
4. Render and review the result visually.
5. Route each change back into the guide, the script, or both.
6. Rebuild and rerender until the main issues are closed.

## Repository Layout

```text
.
├── AGENTS.md
├── LICENSE
├── README.md
├── README_zh.md
└── deck-workflow/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── references/
    └── scripts/
```

## Skill Highlights

- A guide-first workflow for decks that will be revised more than once
- Explicit change routing between `PPT_GUIDE.md` and `generate_ppt.*`
- A review loop based on rendered output rather than source inspection alone
- A helper script that scaffolds a new deck workspace
- Backend-specific guidance for both JavaScript and Python generators
- An explicit rule that code snippets, inline code labels, and terminal-style text should use monospaced fonts
- Rules that keep internal slide ids such as `s01-cover` in source and review artifacts instead of visible slide text
- A helper script that renders `.pptx -> PDF -> PNG` review artifacts
- Design guidance for common deck categories such as project updates, paper readings, training, board reviews, proposals, sales decks, investor pitches, and postmortems

## Quick Start

Validate the skill:

```bash
python /home/hansbug/.codex/skills/.system/skill-creator/scripts/quick_validate.py ./deck-workflow
```

Create a starter deck workspace:

```bash
python ./deck-workflow/scripts/init_deck_workspace.py ./tmp/example-deck \
  --title "Quarterly Business Review" \
  --author "HansBug" \
  --audience "Leadership team" \
  --duration-minutes 15 \
  --slides 12
```

Create a Python-based starter deck workspace:

```bash
python ./deck-workflow/scripts/init_deck_workspace.py ./tmp/example-deck-python \
  --title "Quarterly Business Review" \
  --author "HansBug" \
  --audience "Leadership team" \
  --duration-minutes 15 \
  --slides 12 \
  --backend python
```

Prepare a local Python environment before deciding that Python is unavailable:

```bash
python3 -m venv ./tmp/example-deck-python/.venv
source ./tmp/example-deck-python/.venv/bin/activate
pip install -r ./tmp/example-deck-python/requirements.txt
```

Detect which backend and review tools are available:

```bash
python ./deck-workflow/scripts/detect_deck_environment.py
```

Render a deck into reviewable PDF/PNG artifacts:

```bash
python ./deck-workflow/scripts/render_review.py ./tmp/example-deck/deck.pptx --output-dir ./tmp/example-deck/rendered
```

## Backend Policy

- Prefer Python first when the repo and environment support it.
- If Python deck packages are missing, first try a workspace-local `venv` and install `requirements.txt`.
- Fall back to JavaScript only when Python is still not practical or when you want to align with the official `$slides` skill.
- If both are unsuitable, preserve the same guide-first workflow in another stable format rather than abandoning the workflow.

## Audience-Facing Rule

- Stable slide ids such as `s01-cover` are for guides, code, review notes, and commit history.
- Do not place those ids on visible slides unless the user explicitly requests them.
- Render code snippets, inline code labels, shell commands, and similar code-like visible text in a monospaced font by default.

## Notes On Persistence

The deck workspace should live inside the user's repo or another durable project directory.
Do not keep `PPT_GUIDE.md`, `generate_ppt.*`, and `deck.pptx` only in transient agent directories if the deck is expected to be revised later.

## Recommended Pairing

This skill works well together with the official OpenAI `$slides` skill:

- Use `$deck-workflow` for the high-level production contract, guide writing, change routing, and review loop.
- Use `$slides` for low-level PptxGenJS helpers, rendering utilities, and deck validation when available.

## Installation

To use the skill directly with Codex, copy or symlink `deck-workflow/` into your Codex skills directory:

```bash
cp -R ./deck-workflow "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Or point Codex at the local path if your environment supports explicit skill paths.

## License

This repository is licensed under the MIT License. See [`LICENSE`](./LICENSE).
