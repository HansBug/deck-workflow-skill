---
name: deck-workflow
description: Plan, generate, review, and iteratively maintain presentation decks through a guide-first workflow. Use when Codex needs to create or revise slide decks, `.pptx` presentations, pitch decks, training decks, board updates, paper readings, product reviews, or other decks that should remain editable across multiple rounds. Trigger when the task benefits from keeping a source-of-truth `PPT_GUIDE.md`, a committed generator such as `generate_ppt.js` or `generate_ppt.py`, and a render/review loop so human feedback can be routed into guide updates, generator fixes, or both.
---

# Deck Workflow

## Overview

Treat deck work as a managed production loop, not a one-shot export.
Keep a stable source of truth for narrative and structure, a committed generator for implementation, the generated deck file, and rendered review artifacts for QA and incremental fixes.

## Non-Negotiable Contract

Follow these rules whenever the deck is meant to survive more than one quick pass:

- Create the workspace inside the user's repo or another durable project directory, not in a transient scratch directory.
- Keep `PPT_GUIDE.md` as the upstream source of truth for deck intent.
- Keep `generate_ppt.js` or `generate_ppt.py` as the implementation layer.
- Keep the `.pptx` as a generated artifact, not the only source of truth.
- Keep rendered outputs or review notes whenever visual QA matters.
- Route each change into the correct source artifact before regenerating.
- Keep stable slide ids for review and change routing, but do not surface ids such as `s01-cover` on visible slides unless the user explicitly wants them.
- Do not declare success without reviewing rendered output.

If a user asks for an existing deck to be changed and no guide exists, reconstruct a minimal guide first before making substantial changes.

## Standard Production Loop

Follow this loop in order for new decks and most non-trivial revisions:

1. Inspect the request, constraints, source materials, and any existing deck workspace.
2. Create or repair `PPT_GUIDE.md` before implementing the deck.
3. Implement or update `generate_ppt.js` or `generate_ppt.py` to match the guide.
4. Generate the editable deck file.
5. Render the deck to PDF or per-slide images.
6. Review the rendered output and log issues in `review/notes.md`.
7. Decide whether each issue belongs to the guide, the generator, or both.
8. Fix the right source artifact.
9. Rebuild and re-review until the major issues are closed.

Treat the sequence `PPT_GUIDE.md -> generate_ppt.* -> deck file -> rendered review -> source updates -> rerender` as the default contract, not as optional advice.

Read [references/production-loop.md](references/production-loop.md) before handling multi-round work.

## Required Workspace Artifacts

Maintain these artifacts whenever the task is larger than a throwaway draft:

- `PPT_GUIDE.md`: Goal, audience, deck structure, per-slide message, visible text, speaker notes, asset plan, and acceptance checks.
- `generate_ppt.js` or `generate_ppt.py`: Deterministic generator committed with the deck.
- `deck.pptx` or another stable output filename: Generated deck artifact.
- `review/notes.md`: Issue log with stable slide ids and routing decisions.
- Rendered artifacts: PDF or PNG/JPG outputs used for visual inspection.

Use `scripts/init_deck_workspace.py` to scaffold this structure.

Read [references/workspace-persistence.md](references/workspace-persistence.md) before creating a new deck workspace.

## Guide Rules

Write or reconstruct the guide before building unless the task is a tiny disposable mockup.

Keep these guide rules:

- Define one deck-level goal so the whole deck has a single main thread.
- Give every slide a stable slide id once review begins.
- Treat slide ids as internal production metadata; keep them in the guide, generator, comments, and review notes rather than visible slide text unless explicitly requested.
- Give every slide one main message, not a bucket of unrelated content.
- Keep visible text audience-facing; keep presenter instructions in speaker notes or the guide.
- State what visuals are required and where they come from.
- State acceptance checks per slide so later review is concrete.
- When the deck is spoken, make speaker notes direct enough that a presenter can read them aloud with minimal improvisation.
- When the deck will be generated automatically, make slide instructions concrete enough that the generator can implement them without guessing.

Read [references/guide-schema.md](references/guide-schema.md) when drafting or reconstructing the guide.

## Generator Rules

Implement the generator only after the guide is coherent enough to build against.

Keep these generator rules:

- Match the guide's slide order and slide ids.
- Keep internal slide ids in code structure, review notes, or comments instead of audience-facing text unless explicitly requested.
- Keep theme, helper logic, asset prep, and slide builders in source control.
- Prefer editable text, shapes, and charts whenever practical.
- Avoid direct manual-only edits to the exported `.pptx` unless the change is truly urgent and then backport it into source immediately.
- Keep visible text, speaker notes, and deck metadata in sync with the guide.
- Use stable output paths so review commands and CI-like checks stay repeatable.

If the official `$slides` skill is available and the project is not already committed to another stack, prefer its PptxGenJS helpers and validation utilities for low-level authoring.

## Backend Choice

Choose the backend deliberately instead of mixing stacks casually.

Prefer JavaScript when:

- The project is new and no backend is established.
- The official `$slides` skill is available.
- Editable PowerPoint-native authoring and helper utilities matter most.
- The deck is heavy on layout composition, charts, or repeatable component logic.

Prefer Python when:

- The existing project is already Python-based.
- The deck pipeline depends on `python-pptx`, `PyMuPDF`, `Pillow`, or `pdf2image`.
- The work includes PDF cropping, image extraction, or document-side preprocessing that already lives in Python.
- The team is more likely to maintain the generator in Python.
- The repo can reasonably support a local virtual environment even if the current shell is missing deck libraries.

Do not switch a working project from Python to JavaScript or the reverse without a clear reason.
Do not fall back from Python to JavaScript only because `python-pptx` or related packages are missing globally; first try a workspace-local `venv` and install the required Python dependencies.

Read [references/backend-setup.md](references/backend-setup.md) before choosing a backend or setting up dependencies.

## JavaScript Generator Guidance

When using JavaScript:

- Use `generate_ppt.js` as the single entry point.
- Use `PptxGenJS` for deck generation.
- Set slide size, theme fonts, metadata, and output path explicitly.
- Keep reusable layout helpers and constants near the top of the file or in local helper modules.
- Keep one slide builder function per slide or per reusable section.
- Keep stable slide ids in function names, comments, and review notes rather than visible slide text unless explicitly requested.
- Render and re-review after meaningful edits.

Read [references/generator-javascript.md](references/generator-javascript.md) before building or refactoring a JS generator.

## Python Generator Guidance

When using Python:

- Use `generate_ppt.py` as the single entry point.
- Use `python-pptx` for deck generation and `PyMuPDF`/`Pillow` when source cropping or raster prep is needed.
- If deck libraries are missing, try `python3 -m venv .venv` plus `pip install -r requirements.txt` before deciding that Python is not practical.
- Set slide size, fonts, metadata, and output path explicitly.
- Separate asset preparation, helper utilities, and slide builder functions.
- Keep source-of-truth text and notes aligned with the guide after every edit.
- Keep stable slide ids in function names, comments, and review notes rather than visible slide text unless explicitly requested.
- Render and re-review after meaningful edits.

Read [references/generator-python.md](references/generator-python.md) before building or refactoring a Python generator.

## Review Rules

Treat visual review as mandatory for real deck work.

Follow these review rules:

- Prefer the stable review path `.pptx -> PDF -> per-slide PNG`.
- Review rendered output, not only source code or XML.
- Check for overflow, clipping, overlap, awkward wrapping, weak hierarchy, and unreadable charts or tables.
- Check that internal ids, routing labels, and other maker-only metadata did not leak into visible slide content.
- Re-review after fixes because one layout fix often causes another regression.
- Record issues with slide ids and routing decisions in `review/notes.md`.
- Do not hand obvious visual bugs to the user as the first review pass if you can catch them yourself.

Read [references/review-loop.md](references/review-loop.md) before sign-off.

## Editing Existing Decks

When editing an existing deck:

1. Determine whether a maintained guide and generator already exist.
2. If they exist, reuse them rather than inventing parallel sources.
3. If they do not exist, reconstruct a minimal `PPT_GUIDE.md` first.
4. Only then decide whether the requested change belongs to the guide, the generator, or both.
5. Rebuild and re-review before delivering the revision.

Read [references/change-routing.md](references/change-routing.md) whenever the right edit target is unclear.

## Done Criteria

Do not call the deck update complete until:

- The requested changes live in the correct source artifact.
- The deck has been regenerated from source.
- A fresh render has been reviewed.
- Major visual issues are fixed or explicitly deferred.
- The guide, generator, and rendered result do not contradict each other.

## References

- Read [references/workspace-persistence.md](references/workspace-persistence.md) before creating a workspace so source artifacts live in the user's repo.
- Read [references/production-loop.md](references/production-loop.md) for the mandatory end-to-end iteration loop.
- Read [references/guide-schema.md](references/guide-schema.md) when drafting or reconstructing `PPT_GUIDE.md`.
- Read [references/change-routing.md](references/change-routing.md) when deciding whether to edit the guide, the generator, or both.
- Read [references/design-principles.md](references/design-principles.md) for reusable visual and audience-facing slide rules.
- Read [references/deck-types.md](references/deck-types.md) to adapt the workflow to common deck categories.
- Read [references/backend-setup.md](references/backend-setup.md) before choosing a backend or installing dependencies.
- Read [references/generator-javascript.md](references/generator-javascript.md) before using a JS backend.
- Read [references/generator-python.md](references/generator-python.md) before using a Python backend.
- Read [references/review-loop.md](references/review-loop.md) before review, re-review, or sign-off.
- Run `scripts/detect_deck_environment.py` to inspect backend and review-tool readiness in the current environment.
- Run `scripts/render_review.py` when you want a stable `.pptx -> PDF -> PNG` review path.
- Run `scripts/init_deck_workspace.py` to scaffold a new guide-first deck workspace.
