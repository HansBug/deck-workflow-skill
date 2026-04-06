#!/usr/bin/env python3
"""Render a deck or PDF into reviewable PDF/PNG artifacts."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


def require_command(name: str) -> None:
    if shutil.which(name) is None:
        raise RuntimeError(f"Required command not found: {name}")


def parse_pages(spec: str | None) -> list[int] | None:
    if not spec:
        return None

    pages: set[int] = set()
    for chunk in spec.split(","):
        part = chunk.strip()
        if not part:
            continue
        if "-" in part:
            start_text, end_text = part.split("-", 1)
            start = int(start_text)
            end = int(end_text)
            if start <= 0 or end <= 0 or end < start:
                raise ValueError(f"Invalid page range: {part}")
            for page in range(start, end + 1):
                pages.add(page)
        else:
            page = int(part)
            if page <= 0:
                raise ValueError(f"Invalid page number: {part}")
            pages.add(page)
    return sorted(pages)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def convert_pptx_to_pdf(input_path: Path, output_dir: Path) -> Path:
    require_command("soffice")
    output_dir.mkdir(parents=True, exist_ok=True)
    run(
        [
            "soffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(output_dir),
            str(input_path),
        ]
    )
    pdf_path = output_dir / f"{input_path.stem}.pdf"
    if not pdf_path.exists():
        raise RuntimeError(f"Expected PDF was not created: {pdf_path}")
    return pdf_path


def normalize_slide_names(output_dir: Path) -> list[Path]:
    pattern = re.compile(r"slide-(\d+)\.png$")
    renamed: list[Path] = []
    candidates = sorted(output_dir.glob("slide-*.png"))
    for path in candidates:
        match = pattern.match(path.name)
        if not match:
            renamed.append(path)
            continue
        page = int(match.group(1))
        final_path = output_dir / f"slide-{page:03d}.png"
        if path != final_path:
            if final_path.exists():
                final_path.unlink()
            path.rename(final_path)
        renamed.append(final_path)
    return sorted(renamed)


def render_all_pages(pdf_path: Path, output_dir: Path, dpi: int) -> list[Path]:
    require_command("pdftoppm")
    prefix = output_dir / "slide"
    run(["pdftoppm", "-png", "-r", str(dpi), str(pdf_path), str(prefix)])
    return normalize_slide_names(output_dir)


def render_selected_pages(pdf_path: Path, output_dir: Path, pages: list[int], dpi: int) -> list[Path]:
    require_command("pdftoppm")
    rendered: list[Path] = []
    for page in pages:
        tmp_prefix = output_dir / f".tmp-slide-{page:03d}"
        run(
            [
                "pdftoppm",
                "-png",
                "-r",
                str(dpi),
                "-f",
                str(page),
                "-l",
                str(page),
                "-singlefile",
                str(pdf_path),
                str(tmp_prefix),
            ]
        )
        tmp_output = output_dir / f".tmp-slide-{page:03d}.png"
        final_output = output_dir / f"slide-{page:03d}.png"
        if final_output.exists():
            final_output.unlink()
        tmp_output.rename(final_output)
        rendered.append(final_output)
    return rendered


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render deck review artifacts.")
    parser.add_argument("input", help="Path to a .pptx or .pdf file.")
    parser.add_argument("--output-dir", required=True, help="Directory for review artifacts.")
    parser.add_argument("--pages", help="Optional pages such as '1,3-5'.")
    parser.add_argument("--dpi", type=int, default=160, help="PNG render DPI. Default: 160.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        pages = parse_pages(args.pages)
        if input_path.suffix.lower() == ".pptx":
            pdf_path = convert_pptx_to_pdf(input_path, output_dir)
        elif input_path.suffix.lower() == ".pdf":
            pdf_path = input_path
        else:
            raise RuntimeError("Input must be a .pptx or .pdf file")

        if pages is None:
            pngs = render_all_pages(pdf_path, output_dir, args.dpi)
        else:
            pngs = render_selected_pages(pdf_path, output_dir, pages, args.dpi)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"PDF: {pdf_path}")
    for png in pngs:
        print(f"PNG: {png}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
