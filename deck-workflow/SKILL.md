---
name: deck-workflow
description: Plan, generate, review, and iteratively maintain presentation decks through a guide-first workflow. Use when Codex needs to create or revise slide decks, `.pptx` presentations, pitch decks, training decks, board updates, paper readings, or product reviews and the work should stay editable across multiple rounds. Trigger when the task benefits from keeping a source-of-truth `PPT_GUIDE.md`, a deck generation script, and a render/review loop so human feedback can be routed into guide updates, script fixes, or both.
---

# Deck Workflow

## Overview

Treat deck work as a managed production loop, not a one-shot export.
Keep a stable source of truth for narrative and structure, a committed generation script for implementation, and rendered review artifacts for QA and incremental fixes.

## Core Artifacts

Maintain these artifacts whenever the task is larger than a quick one-off outline:

- `PPT_GUIDE.md`: Source of truth for goal, audience, slide order, per-slide message, visible text, speaker notes, asset plan, and acceptance checks.
- `generate_ppt.js` or `generate_ppt.py`: Implementation layer that turns the guide into an editable deck.
- `review/notes.md`: Running log of review findings, requested changes, and decisions.
- Rendered artifacts: PDF or per-slide PNG/JPG outputs used for visual inspection.

## Workflow

1. Initialize a workspace with `scripts/init_deck_workspace.py` or create the same structure manually.
2. Write `PPT_GUIDE.md` before coding the deck whenever the request involves more than a rough outline.
3. Implement the deck in a generation script only after the guide is coherent enough to build against.
4. Render the deck and review visuals before delivery. If the environment already has the official `$slides` skill, use it for low-level authoring helpers and validation.
5. Capture issues in `review/notes.md` with stable slide ids.
6. Route each change request to the guide, the script, or both by following [references/change-routing.md](references/change-routing.md).
7. Re-render after each meaningful change before declaring the deck updated.

## Decision Rules

- Start with the guide when creating a new deck, rewriting deck structure, or responding to narrative/content feedback.
- Reconstruct a minimal guide first when editing an existing deck that has no maintained source-of-truth document.
- Preserve a stable slide id per slide once review starts so comments can be mapped cleanly across revisions.
- Keep visible text separate from speaker notes; do not hide strategy instructions in the deck body.
- Prefer editable deck elements whenever practical. Do not make the `.pptx` the only authoritative source of truth.
- Keep the skill general. Put domain-specific logic in the deck workspace, not in this skill.

## Backend Choice

- Prefer the environment's established deck backend when editing an existing project.
- When building from scratch and the official `$slides` skill is available, prefer its PptxGenJS stack and validation utilities.
- Keep the source script committed alongside the generated deck so later edits remain reproducible.

## References

- Read [references/guide-schema.md](references/guide-schema.md) when drafting or reconstructing `PPT_GUIDE.md`.
- Read [references/change-routing.md](references/change-routing.md) when deciding whether to edit the guide, the generation script, or both.
- Read [references/review-loop.md](references/review-loop.md) when setting up QA or deciding whether a deck update is ready to deliver.
- Run `scripts/init_deck_workspace.py` to scaffold a new guide-first deck workspace.

Create only the resource directories this skill actually needs. Delete this section if no resources are required.

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Examples from other skills:**
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Codex for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Codex's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Codex should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Codex produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Not every skill requires all three types of resources.**
