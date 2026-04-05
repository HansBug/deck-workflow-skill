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


def english_guide(title: str, audience: str, duration: int, slides: int, author: str) -> str:
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
        - Update `generate_ppt.js` for layout and implementation changes.
        - Re-render after every meaningful edit.

        ## Slide Plan
        """
    ).rstrip()
    return header + "\n\n" + "\n\n".join(sections) + "\n"


def chinese_guide(title: str, audience: str, duration: int, slides: int, author: str) -> str:
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
        - 改布局、裁图、字号、配色、遮挡，先改 `generate_ppt.js`。
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
    parser.add_argument("--language", choices=("en", "zh"), default="en", help="Language for the guide template.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files in the workspace.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    workspace.mkdir(parents=True, exist_ok=True)

    guide = english_guide(args.title, args.audience, args.duration_minutes, args.slides, args.author)
    if args.language == "zh":
        guide = chinese_guide(args.title, args.audience, args.duration_minutes, args.slides, args.author)

    write_text(workspace / "PPT_GUIDE.md", guide, args.force)
    write_text(workspace / "generate_ppt.js", js_template(args.title, args.author), args.force)
    write_text(workspace / "review" / "notes.md", review_template(), args.force)
    touch_keep(workspace / "assets" / ".gitkeep")
    touch_keep(workspace / "rendered" / ".gitkeep")

    print(f"Initialized deck workspace at {workspace}")
    print("Created:")
    for item in [
        workspace / "PPT_GUIDE.md",
        workspace / "generate_ppt.js",
        workspace / "review" / "notes.md",
        workspace / "assets" / ".gitkeep",
        workspace / "rendered" / ".gitkeep",
    ]:
        print(f"  - {item}")


if __name__ == "__main__":
    main()
