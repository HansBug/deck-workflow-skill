# AGENTS.md

This repository hosts a Codex-compatible skill for iterative deck production.

## Repository Intent

- Keep the core skill general across presentation types.
- Treat deck work as a workflow problem, not only a slide rendering problem.
- Preserve a clean split between repo-level documentation and the installable skill.

## Structure

- Repo-level docs live at the repository root: `README.md`, `README_zh.md`, `LICENSE`, `AGENTS.md`.
- The installable skill lives in `deck-workflow/`.
- Keep `deck-workflow/SKILL.md` concise. Put detailed procedures in `deck-workflow/references/`.
- Put executable helpers in `deck-workflow/scripts/`.

## Editing Rules

1. Do not let the skill drift into an academic-only workflow. Keep domain-specific examples secondary.
2. When workflow semantics change, update:
   - `deck-workflow/SKILL.md`
   - the relevant file under `deck-workflow/references/`
   - `README.md` and `README_zh.md` if user-facing behavior changed
3. When the skill trigger surface or UI-facing summary changes, review `deck-workflow/agents/openai.yaml` and regenerate or edit it as needed.
4. When adding or editing scripts under `deck-workflow/scripts/`, run a real smoke test.
5. After skill changes, run:

```bash
python /home/hansbug/.codex/skills/.system/skill-creator/scripts/quick_validate.py ./deck-workflow
```

6. Do not add repo-level clutter inside `deck-workflow/`. Keep the installable skill minimal.

## Preferred Maintenance Direction

- Improve change routing, guide schema, and review-loop quality before adding flashy design advice.
- Prefer durable workflow improvements over one-off prompt tricks.
- Prefer reusable scaffolding and validation over large static examples.
