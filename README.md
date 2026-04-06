# deck-workflow-skill

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
- A helper script that renders `.pptx -> PDF -> PNG` review artifacts

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

Render a deck into reviewable PDF/PNG artifacts:

```bash
python ./deck-workflow/scripts/render_review.py ./tmp/example-deck/deck.pptx --output-dir ./tmp/example-deck/rendered
```

## Installation

To use the skill directly with Codex, copy or symlink `deck-workflow/` into your Codex skills directory:

```bash
cp -R ./deck-workflow "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Or point Codex at the local path if your environment supports explicit skill paths.

## License

This repository is licensed under the MIT License. See [`LICENSE`](./LICENSE).
