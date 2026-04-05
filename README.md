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

The core idea is:

1. Write `PPT_GUIDE.md` first.
2. Implement the deck in a generation script.
3. Render and review the result visually.
4. Route each change back into the guide, the script, or both.

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

## Installation

To use the skill directly with Codex, copy or symlink `deck-workflow/` into your Codex skills directory:

```bash
cp -R ./deck-workflow "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Or point Codex at the local path if your environment supports explicit skill paths.

## License

This repository is licensed under the MIT License. See [`LICENSE`](./LICENSE).
