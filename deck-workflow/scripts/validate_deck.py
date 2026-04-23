#!/usr/bin/env python3
"""Validate a generated .pptx against structural, notes, and guide-consistency checks.

This validator is intentionally dependency-light. It does not open the deck with
``python-pptx`` unless the caller asks it to. The goal is to catch the common
handoff-time failure modes without requiring a pre-installed Python deck stack:

- The file is not a valid .pptx (zip) archive
- Slide count does not match an expected number
- Speaker notes were supposed to be embedded but ``ppt/notesSlides`` parts are
  missing from the package or the slide-to-notesSlide relationship is absent
- Notes text in the final deck has drifted away from ``PPT_GUIDE.md`` at the
  positions the skill's default ``### sNN-...`` guide schema specifies
- Visible slide XML still contains presenter-only slide ids such as ``s01-cover``

Limitations: the validator follows each slide's ``.rels`` entry to resolve the
corresponding notes slide when comparing guide text against deck notes, so
renamed or swapped relationship targets are respected. It does not, however,
run a full rendering pass. Formula sizing, highlight occlusion, table
readability, and summary/closing language purity must still be confirmed
against a rendered PDF or PNG, as described in ``references/review-loop.md``
and ``references/delivery-checklist.md``.

The script returns a non-zero exit code when any check fails, so it can be used
from CI-like workflows and from ``review/commands.md`` examples.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


SLIDE_XML_PATTERN = re.compile(r"^ppt/slides/slide(\d+)\.xml$")
NOTES_XML_PATTERN = re.compile(r"^ppt/notesSlides/notesSlide(\d+)\.xml$")
VISIBLE_ID_HINT_PATTERN = re.compile(r"\bs\d{2,3}-[a-z][a-z0-9-]*\b")
GUIDE_SLIDE_HEADING_PATTERN = re.compile(r"^###\s+(s\d{2,3}-[^\s]+)", re.MULTILINE)
RELS_NOTES_TARGET_PATTERN = re.compile(
    r'<Relationship[^>]*Type="[^"]*notesSlide"[^>]*Target="([^"]+)"',
)

READ_ALOUD_FIELDS = (
    "speaker_notes",
    "speaker notes",
    "presenter_ready_notes",
    "presenter-ready notes",
    "可直接念的完整台词",
)


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""

    def to_dict(self) -> dict[str, object]:
        return {"name": self.name, "passed": self.passed, "detail": self.detail}


@dataclass
class ValidationReport:
    deck_path: Path
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(check.passed for check in self.checks)

    def add(self, name: str, passed: bool, detail: str = "") -> None:
        self.checks.append(CheckResult(name=name, passed=passed, detail=detail))

    def to_dict(self) -> dict[str, object]:
        return {
            "deck": str(self.deck_path),
            "ok": self.ok,
            "checks": [check.to_dict() for check in self.checks],
        }


def list_slide_xml(names: Iterable[str]) -> list[str]:
    return sorted(
        (name for name in names if SLIDE_XML_PATTERN.match(name)),
        key=lambda n: int(SLIDE_XML_PATTERN.match(n).group(1)),
    )


def list_notes_xml(names: Iterable[str]) -> list[str]:
    return sorted(
        (name for name in names if NOTES_XML_PATTERN.match(name)),
        key=lambda n: int(NOTES_XML_PATTERN.match(n).group(1)),
    )


def resolve_notes_target(archive: zipfile.ZipFile, slide_name: str) -> str | None:
    """Return the actual notes-slide part name referenced by ``slide_name``.

    Reads ``ppt/slides/_rels/slideN.xml.rels`` and follows the ``notesSlide``
    relationship's ``Target`` attribute, so renamed or swapped targets are
    respected instead of assuming filename order matches slide order.
    """
    rels_name = slide_name.replace("ppt/slides/", "ppt/slides/_rels/") + ".rels"
    if rels_name not in archive.namelist():
        return None
    try:
        rels_text = archive.read(rels_name).decode("utf-8", errors="replace")
    except KeyError:
        return None
    match = RELS_NOTES_TARGET_PATTERN.search(rels_text)
    if not match:
        return None
    target = match.group(1)
    if target.startswith("../"):
        resolved = "ppt/" + target[len("../"):]
    elif target.startswith("/"):
        resolved = target.lstrip("/")
    else:
        resolved = "ppt/slides/" + target
    normalized: list[str] = []
    for part in resolved.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if normalized:
                normalized.pop()
            continue
        normalized.append(part)
    return "/".join(normalized)


def extract_visible_text(xml_bytes: bytes) -> str:
    try:
        text = xml_bytes.decode("utf-8", errors="replace")
    except Exception:
        return ""
    parts = re.findall(r"<a:t>([^<]*)</a:t>", text)
    return " ".join(parts)


def extract_notes_text(xml_bytes: bytes) -> str:
    try:
        text = xml_bytes.decode("utf-8", errors="replace")
    except Exception:
        return ""
    parts = re.findall(r"<a:t>([^<]*)</a:t>", text)
    return "\n".join(part.strip() for part in parts if part.strip())


def parse_guide_slide_blocks(guide_text: str) -> list[tuple[str, str]]:
    headings = list(GUIDE_SLIDE_HEADING_PATTERN.finditer(guide_text))
    blocks: list[tuple[str, str]] = []
    for index, match in enumerate(headings):
        slide_id = match.group(1)
        start = match.end()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(guide_text)
        blocks.append((slide_id, guide_text[start:end]))
    return blocks


def extract_read_aloud_from_block(block: str) -> str:
    lines = block.splitlines()
    buffer: list[str] = []
    collecting = False
    for line in lines:
        stripped = line.strip()
        if not collecting:
            lower = stripped.lower()
            matched = False
            for field_name in READ_ALOUD_FIELDS:
                normalized = field_name.lower()
                if normalized in lower and stripped.endswith((":", "：")):
                    collecting = True
                    matched = True
                    break
            if matched:
                continue
            continue
        if not stripped:
            if buffer:
                break
            continue
        if stripped.startswith("- ") and stripped.endswith((":", "：")) and buffer:
            break
        if stripped.startswith("###") or stripped.startswith("## "):
            break
        if stripped.startswith("- "):
            buffer.append(stripped[2:].strip(" `"))
        else:
            buffer.append(stripped.strip(" `"))
    return " ".join(entry for entry in buffer if entry and entry != "TODO")


def check_valid_zip(report: ValidationReport, zip_path: Path) -> zipfile.ZipFile | None:
    if not zip_path.exists():
        report.add("file-exists", False, f"{zip_path} does not exist")
        return None
    if not zipfile.is_zipfile(zip_path):
        report.add("file-is-pptx-zip", False, "File is not a valid .pptx archive")
        return None
    try:
        archive = zipfile.ZipFile(zip_path)
    except zipfile.BadZipFile as exc:
        report.add("file-is-pptx-zip", False, f"BadZipFile: {exc}")
        return None
    report.add("file-is-pptx-zip", True)
    return archive


def check_slide_count(
    report: ValidationReport,
    archive: zipfile.ZipFile,
    expected: int | None,
) -> list[str]:
    slide_names = list_slide_xml(archive.namelist())
    report.add("slide-count-nonzero", len(slide_names) > 0, f"Found {len(slide_names)} slides")
    if expected is not None:
        report.add(
            "slide-count-matches-expected",
            len(slide_names) == expected,
            f"Expected {expected}, found {len(slide_names)}",
        )
    return slide_names


def check_notes_parts(
    report: ValidationReport,
    archive: zipfile.ZipFile,
    slide_names: list[str],
    expect_notes: bool,
) -> list[str]:
    notes_names = list_notes_xml(archive.namelist())
    slide_count = len(slide_names)
    if not expect_notes:
        return notes_names
    report.add("notes-parts-present", len(notes_names) > 0, f"Found {len(notes_names)} notes parts")
    report.add(
        "notes-count-matches-slides",
        len(notes_names) == slide_count,
        f"Slides: {slide_count}, notes: {len(notes_names)}",
    )

    missing_relationship: list[str] = []
    missing_target_part: list[str] = []
    known_notes = set(notes_names)
    for slide_name in slide_names:
        target = resolve_notes_target(archive, slide_name)
        if target is None:
            missing_relationship.append(slide_name)
            continue
        if target not in known_notes:
            missing_target_part.append(f"{slide_name}->{target}")
    report.add(
        "slide-to-notes-relationship",
        not missing_relationship,
        "Every slide's .rels references a notesSlide"
        if not missing_relationship
        else f"Slides without a notesSlide relationship: {missing_relationship}",
    )
    report.add(
        "slide-notes-target-exists",
        not missing_target_part,
        "Every slide relationship resolves to an existing notesSlide part"
        if not missing_target_part
        else f"Slides whose notesSlide target is missing: {missing_target_part}",
    )

    return notes_names


def check_notes_nonempty(
    report: ValidationReport,
    archive: zipfile.ZipFile,
    notes_names: list[str],
) -> None:
    if not notes_names:
        return
    missing_text: list[str] = []
    for name in notes_names:
        text = extract_notes_text(archive.read(name))
        if not text:
            missing_text.append(name)
    report.add(
        "notes-nonempty",
        not missing_text,
        "All notes have text" if not missing_text else f"Empty notes: {missing_text}",
    )


def check_visible_id_leaks(
    report: ValidationReport,
    archive: zipfile.ZipFile,
    slide_names: list[str],
    allow_ids: bool,
) -> None:
    if allow_ids:
        return
    leaks: list[str] = []
    for name in slide_names:
        visible = extract_visible_text(archive.read(name))
        if VISIBLE_ID_HINT_PATTERN.search(visible):
            leaks.append(name)
    report.add(
        "no-visible-slide-id-leaks",
        not leaks,
        "No s##-style ids found on visible slides"
        if not leaks
        else f"Possible slide-id leakage in: {leaks}",
    )


def compare_notes_with_guide(
    report: ValidationReport,
    archive: zipfile.ZipFile,
    notes_names: list[str],
    slide_names: list[str],
    guide_path: Path | None,
    mismatch_tolerance: int,
) -> None:
    if guide_path is None or not notes_names:
        return
    if not guide_path.exists():
        report.add("guide-exists", False, f"{guide_path} does not exist")
        return
    report.add("guide-exists", True)
    guide_text = guide_path.read_text(encoding="utf-8")
    blocks = parse_guide_slide_blocks(guide_text)
    if not blocks:
        report.add(
            "guide-notes-comparison",
            True,
            "Guide has no ### sNN-... headings; skipping structural notes-vs-guide comparison. "
            "Sampled content comparison must still be confirmed manually against PPT_GUIDE.md.",
        )
        return
    report.add(
        "guide-has-slide-blocks",
        True,
        f"Parsed {len(blocks)} guide slide blocks",
    )

    slide_count = len(slide_names)
    if len(blocks) != slide_count:
        guide_ids = [slide_id for slide_id, _ in blocks]
        if len(blocks) > slide_count:
            extra_blocks = [slide_id for slide_id, _ in blocks[slide_count:]]
            detail = (
                f"Guide has {len(blocks)} sNN- blocks, deck has {slide_count} slides. "
                f"Guide blocks beyond the deck: {extra_blocks}"
            )
        else:
            detail = (
                f"Guide has {len(blocks)} sNN- blocks, deck has {slide_count} slides. "
                f"Guide covers only: {guide_ids}"
            )
        report.add(
            "guide-block-count-matches-slides",
            False,
            detail + " The schema expects a 1:1 mapping; resolve the gap before trusting the alignment check.",
        )
        return
    report.add(
        "guide-block-count-matches-slides",
        True,
        f"Guide and deck both have {slide_count} positions",
    )

    mismatches: list[str] = []
    unchecked: list[str] = []
    unmapped: list[str] = []
    for index in range(slide_count):
        slide_id, block = blocks[index]
        guide_line = extract_read_aloud_from_block(block)
        if not guide_line:
            unchecked.append(slide_id)
            continue
        notes_target = resolve_notes_target(archive, slide_names[index])
        if notes_target is None or notes_target not in archive.namelist():
            unmapped.append(slide_id)
            continue
        deck_line = extract_notes_text(archive.read(notes_target))
        if not deck_line:
            mismatches.append(f"{slide_id} (deck notes empty)")
            continue
        if guide_line not in deck_line.replace("\n", " ") and deck_line not in guide_line:
            mismatches.append(slide_id)

    if unchecked:
        report.add(
            "guide-read-aloud-coverage",
            False,
            f"Could not extract read-aloud text for: {unchecked}. "
            "Either the guide uses a different field name or the field is empty; manual comparison required.",
        )
    else:
        report.add(
            "guide-read-aloud-coverage",
            True,
            "Extracted read-aloud text for every guide block",
        )

    if unmapped:
        report.add(
            "notes-slide-resolution",
            False,
            f"Could not resolve notes slide via .rels for: {unmapped}",
        )

    report.add(
        "notes-align-with-guide",
        len(mismatches) <= mismatch_tolerance,
        f"Mismatched slides: {mismatches}"
        if mismatches
        else "Guide read-aloud text matches deck notes at every parsed position",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a generated .pptx deck.")
    parser.add_argument("deck", help="Path to the .pptx file to validate.")
    parser.add_argument("--guide", help="Optional path to PPT_GUIDE.md for notes comparison.")
    parser.add_argument(
        "--expect-slides",
        type=int,
        help="Expected slide count. Enables exact count validation.",
    )
    parser.add_argument(
        "--expect-notes",
        action="store_true",
        help="Require notes slides to be present for every slide.",
    )
    parser.add_argument(
        "--allow-visible-ids",
        action="store_true",
        help="Skip the check that forbids s##-style slide ids from visible slide text.",
    )
    parser.add_argument(
        "--mismatch-tolerance",
        type=int,
        default=0,
        help="Number of slide positions allowed to disagree between guide notes and deck notes.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format for validation results.",
    )
    return parser.parse_args()


def render_text_report(report: ValidationReport) -> str:
    lines = [f"Deck: {report.deck_path}", f"Overall: {'OK' if report.ok else 'FAIL'}", ""]
    for check in report.checks:
        status = "PASS" if check.passed else "FAIL"
        lines.append(f"  [{status}] {check.name}{(' - ' + check.detail) if check.detail else ''}")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    deck_path = Path(args.deck).expanduser().resolve()
    guide_path = Path(args.guide).expanduser().resolve() if args.guide else None
    report = ValidationReport(deck_path=deck_path)

    archive = check_valid_zip(report, deck_path)
    if archive is None:
        print(render_text_report(report) if args.format == "text" else json.dumps(report.to_dict(), indent=2))
        return 1

    with archive:
        slide_names = check_slide_count(report, archive, args.expect_slides)
        notes_names = check_notes_parts(report, archive, slide_names, args.expect_notes)
        check_notes_nonempty(report, archive, notes_names)
        check_visible_id_leaks(report, archive, slide_names, args.allow_visible_ids)
        compare_notes_with_guide(
            report,
            archive,
            notes_names,
            slide_names,
            guide_path,
            args.mismatch_tolerance,
        )

    if args.format == "json":
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(render_text_report(report))

    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
