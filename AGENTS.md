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
7. Keep the standard production loop explicit and hard to skip:
   - `PPT_GUIDE.md`
   - `generate_ppt.js` or `generate_ppt.py`
   - generated `.pptx`
   - rendered review artifacts
   - routed fixes
   - rerender
8. Keep both JavaScript and Python generator guidance maintained. Do not let one backend silently become second-class if the skill claims to support both.
9. Keep `.pptx -> PDF -> per-slide PNG` as the default stable review path unless a better environment-specific path is clearly available.
10. Keep workspace persistence explicit: the intended home of `PPT_GUIDE.md`, `generate_ppt.*`, and `deck.pptx` is the user's repo, not a transient scratch directory.
11. Keep the audience-facing vs speaker-facing distinction explicit in the docs and templates:
   - visible slide text is for the audience
   - notes are for the presenter
12. Keep the guidance broad enough to cover common deck categories, not only academic talks.

## Preferred Maintenance Direction

- Improve change routing, guide schema, and review-loop quality before adding flashy design advice.
- Prefer durable workflow improvements over one-off prompt tricks.
- Prefer reusable scaffolding and validation over large static examples.
- If the workflow grows, push details into `references/` while keeping `SKILL.md` as a strong but readable operating contract.
