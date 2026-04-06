#!/usr/bin/env python3
"""Scaffold a guide-first deck workspace."""

from __future__ import annotations

import argparse
import textwrap
from pathlib import Path


def slide_id(index: int, total: int) -> str:
    if index == 1:
        suffix = "cover"
    elif index == total:
        suffix = "closing"
    elif index == total - 1 and total >= 3:
        suffix = "summary"
    else:
        suffix = f"content-{index:02d}"
    return f"s{index:02d}-{suffix}"


def english_guide(title: str, audience: str, duration: int, slides: int, author: str, generator_name: str) -> str:
    sections = []
    for idx in range(1, slides + 1):
        sid = slide_id(idx, slides)
        sections.append(
            textwrap.dedent(
                f"""\
                ### {sid}

                - Target Duration: `TODO`
                - Title: `TODO`
                - Message: `TODO`
                - Visible Text:
                  - `TODO`
                - Visuals:
                  - `TODO`
                - Speaker Notes:
                  - `TODO`
                - Implementation Notes:
                  - `TODO`
                - Acceptance Checks:
                  - `TODO`
                """
            ).rstrip()
        )

    header = textwrap.dedent(
        f"""\
        # PPT_GUIDE

        ## Deck Brief

        - Title: `{title}`
        - Goal: `TODO`
        - Audience: `{audience}`
        - Duration: `{duration} minutes`
        - Slide Budget: `{slides}`
        - Presenter: `{author}`
        - Aspect Ratio: `16:9`
        - Tooling Backend: `TODO`
        - Source Materials:
          - `TODO`
        - Style Constraints:
          - `TODO`
        - Acceptance Criteria:
          - `Rendered deck has no obvious overflow, collision, or clipping`
          - `The final deck matches the slide messages below`

        ## Workflow Notes

        - Update this guide first for narrative, scope, timing, and slide-order changes.
        - Update `{generator_name}` for layout and implementation changes.
        - Re-render after every meaningful edit.

        ## Slide Plan
        """
    ).rstrip()
    return header + "\n\n" + "\n\n".join(sections) + "\n"


def chinese_guide(title: str, audience: str, duration: int, slides: int, author: str, generator_name: str) -> str:
    sections = []
    for idx in range(1, slides + 1):
        sid = slide_id(idx, slides)
        sections.append(
            textwrap.dedent(
                f"""\
                ### {sid}

                - 目标时长：`TODO`
                - 页面标题：`TODO`
                - 页面核心信息：`TODO`
                - 页面上直接放的字：
                  - `TODO`
                - 图片 / 图表要求：
                  - `TODO`
                - 讲稿：
                  - `TODO`
                - 实现备注：
                  - `TODO`
                - 检查重点：
                  - `TODO`
                """
            ).rstrip()
        )

    header = textwrap.dedent(
        f"""\
        # PPT_GUIDE

        ## 默认假设

        - 标题：`{title}`
        - 听众：`{audience}`
        - 总时长：`{duration} 分钟`
        - 页数：`{slides}`
        - 汇报人：`{author}`
        - 画布：`16:9`
        - 生成后端：`TODO`

        ## 使用方式

        - 改主线、结构、页数、讲稿，先改这份 guide。
        - 改布局、裁图、字号、配色、遮挡，先改 `{generator_name}`。
        - 每次实质修改后都重新渲染检查。

        ## 逐页规划
        """
    ).rstrip()
    return header + "\n\n" + "\n\n".join(sections) + "\n"


def js_template(title: str, author: str) -> str:
    return textwrap.dedent(
        f"""\
        const pptxgen = require("pptxgenjs");

        async function main() {{
          const pptx = new pptxgen();
          pptx.layout = "LAYOUT_WIDE";
          pptx.author = "{author}";
          pptx.company = "{author}";
          pptx.subject = "{title}";
          pptx.title = "{title}";
          pptx.lang = "en-US";
          pptx.theme = {{
            headFontFace: "Aptos Display",
            bodyFontFace: "Aptos",
            lang: "en-US",
          }};

          const slide = pptx.addSlide();
          slide.background = {{ color: "F7F5F1" }};
          slide.addText("{title}", {{
            x: 0.7,
            y: 0.8,
            w: 10.5,
            h: 0.6,
            fontFace: "Aptos Display",
            fontSize: 24,
            bold: true,
            color: "1F2937",
            margin: 0,
          }});
          slide.addText("Implement slides from PPT_GUIDE.md. Keep guide changes and layout changes separate.", {{
            x: 0.75,
            y: 1.6,
            w: 11.4,
            h: 0.8,
            fontFace: "Aptos",
            fontSize: 14,
            color: "4B5563",
            margin: 0,
          }});

          await pptx.writeFile({{ fileName: "deck.pptx" }});
        }}

        main().catch((error) => {{
          console.error(error);
          process.exitCode = 1;
        }});
        """
    )


def python_template(title: str, author: str) -> str:
    return textwrap.dedent(
        f"""\
        from pathlib import Path

        from pptx import Presentation
        from pptx.dml.color import RGBColor
        from pptx.util import Inches, Pt

        OUTPUT = Path(__file__).with_name("deck.pptx")


        def add_notes(slide, text: str) -> None:
            try:
                notes_frame = slide.notes_slide.notes_text_frame
                notes_frame.clear()
                notes_frame.text = text
            except Exception:
                pass


        def build_cover(prs: Presentation) -> None:
            slide = prs.slides.add_slide(prs.slide_layouts[6])
            slide.background.fill.solid()
            slide.background.fill.fore_color.rgb = RGBColor(247, 245, 241)
            title_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.8), Inches(11.2), Inches(0.8))
            title_frame = title_box.text_frame
            title_frame.text = "{title}"
            run = title_frame.paragraphs[0].runs[0]
            run.font.size = Pt(24)
            run.font.bold = True
            subtitle_box = slide.shapes.add_textbox(Inches(0.75), Inches(1.6), Inches(11.4), Inches(0.8))
            subtitle_box.text_frame.text = "Implement slides from PPT_GUIDE.md. Keep guide changes and layout changes separate."
            add_notes(slide, "Backfill presenter notes from PPT_GUIDE.md after implementing the real slides.")


        def build_presentation() -> Path:
            prs = Presentation()
            prs.slide_width = Inches(13.333333)
            prs.slide_height = Inches(7.5)
            prs.core_properties.author = "{author}"
            prs.core_properties.title = "{title}"
            prs.core_properties.subject = "{title}"
            build_cover(prs)
            prs.save(str(OUTPUT))
            return OUTPUT


        if __name__ == "__main__":
            print(build_presentation())
        """
    )


def js_package_json() -> str:
    return textwrap.dedent(
        """\
        {
          "name": "deck-workspace",
          "private": true,
          "type": "commonjs",
          "scripts": {
            "build": "node generate_ppt.js"
          },
          "dependencies": {
            "pptxgenjs": "^3.13.0"
          }
        }
        """
    )


def python_requirements() -> str:
    return textwrap.dedent(
        """\
        python-pptx>=0.6.23
        PyMuPDF>=1.24.0
        Pillow>=10.0.0
        pdf2image>=1.16.0
        """
    )


def review_commands(generator_name: str, build_command: str) -> str:
    return textwrap.dedent(
        f"""\
        # Review Commands

        ## Build

        ```bash
        {build_command}
        ```

        ## Render To PDF

        ```bash
        soffice --headless --convert-to pdf --outdir rendered deck.pptx
        ```

        ## Render PDF To PNG

        ```bash
        pdftoppm -png rendered/deck.pdf rendered/slide
        ```

        ## Workflow Reminder

        - Change structure, message, timing, or slide order in `PPT_GUIDE.md`.
        - Change layout, spacing, cropping, fonts, or visual fixes in `{generator_name}`.
        - Rebuild and rerender after every meaningful edit.
        """
    )


def review_template() -> str:
    return textwrap.dedent(
        """\
        # Review Notes

        ## Current Round

        - Scope: `TODO`
        - Reviewer: `TODO`
        - Render Used: `TODO`

        ## Open Issues

        - [ ] `slide-id` - `Describe the issue and route: guide/script/both`

        ## Closed Issues

        - None yet.

        ## Deferred

        - None.
        """
    )


def write_text(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists; use --force to overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def touch_keep(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize a guide-first deck workspace.")
    parser.add_argument("workspace", help="Path to the workspace directory to create.")
    parser.add_argument("--title", default="New Deck", help="Working title for the deck.")
    parser.add_argument("--author", default="Your Name", help="Presenter or owner name.")
    parser.add_argument("--audience", default="General audience", help="Intended audience.")
    parser.add_argument("--duration-minutes", type=int, default=20, help="Target duration in minutes.")
    parser.add_argument("--slides", type=int, default=10, help="Planned slide count.")
    parser.add_argument("--backend", choices=("js", "python"), default="js", help="Generator backend to scaffold.")
    parser.add_argument("--language", choices=("en", "zh"), default="en", help="Language for the guide template.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files in the workspace.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    workspace.mkdir(parents=True, exist_ok=True)

    generator_name = "generate_ppt.js" if args.backend == "js" else "generate_ppt.py"
    build_command = "node generate_ppt.js" if args.backend == "js" else "python generate_ppt.py"

    guide = english_guide(args.title, args.audience, args.duration_minutes, args.slides, args.author, generator_name)
    if args.language == "zh":
        guide = chinese_guide(args.title, args.audience, args.duration_minutes, args.slides, args.author, generator_name)

    write_text(workspace / "PPT_GUIDE.md", guide, args.force)
    if args.backend == "js":
        write_text(workspace / "generate_ppt.js", js_template(args.title, args.author), args.force)
        write_text(workspace / "package.json", js_package_json(), args.force)
    else:
        write_text(workspace / "generate_ppt.py", python_template(args.title, args.author), args.force)
        write_text(workspace / "requirements.txt", python_requirements(), args.force)
    write_text(workspace / "review" / "notes.md", review_template(), args.force)
    write_text(workspace / "review" / "commands.md", review_commands(generator_name, build_command), args.force)
    touch_keep(workspace / "assets" / ".gitkeep")
    touch_keep(workspace / "rendered" / ".gitkeep")

    print(f"Initialized deck workspace at {workspace}")
    print("Created:")
    items = [workspace / "PPT_GUIDE.md"]
    if args.backend == "js":
        items.extend([workspace / "generate_ppt.js", workspace / "package.json"])
    else:
        items.extend([workspace / "generate_ppt.py", workspace / "requirements.txt"])
    items.extend(
        [
            workspace / "review" / "notes.md",
            workspace / "review" / "commands.md",
            workspace / "assets" / ".gitkeep",
            workspace / "rendered" / ".gitkeep",
        ]
    )
    for item in items:
        print(f"  - {item}")


if __name__ == "__main__":
    main()
