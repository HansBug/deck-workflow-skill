# deck-workflow-skill

[English README](./README.md)

`deck-workflow-skill` 是一个 Codex 兼容 skill 的源码仓库。它的目标不是“一次性生成一个 PPT”，而是把 PPT 制作变成一条可反复迭代的生产流程。

真正可安装的 skill 位于 [`deck-workflow/`](./deck-workflow)。仓库根目录补充了 repo 级说明、维护约定和版本管理文件。

## 这个 Skill 解决什么问题

适用于下面这类需要持续迭代的 deck 工作：

- 新建一套演示文稿
- 重构已有 deck 的结构和叙事
- 根据人类反馈做多轮修改
- 反复进行视觉验收和增量修复
- 希望把“内容意图”和“实现代码”拆开维护的场景

这套 skill 的核心工作流是一个标准闭环：

1. 先写 `PPT_GUIDE.md`
2. 再写 `generate_ppt.*`
3. 生成可编辑的 `.pptx`
4. 把结果渲染出来做视觉检查
5. 后续修改时，把改动明确路由到 guide、脚本或两者
6. 重新生成并复检，直到主要问题关闭

## 仓库结构

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

## Skill 能力

- 面向多轮迭代的 guide-first deck 工作流
- 明确区分 `PPT_GUIDE.md` 和 `generate_ppt.*` 的职责
- 基于渲染结果而不是仅看源码的 review loop
- 提供一个脚手架脚本，用于初始化新的 deck 工作区
- 同时给出 JavaScript 和 Python 两类 generator 的制作规范
- 明确要求代码片段、行内代码标签、终端命令等代码相关可见文本默认使用等宽字体
- 明确要求像 `s01-cover` 这样的 slide id 只用于源码和 review，不应直接出现在观众可见页面里
- 提供一个稳定的 `pptx -> pdf -> png` 视觉检查脚本
- 补充了项目汇报、paper reading、培训、board review、proposal、sales、investor pitch、postmortem 等常见 deck 类型的制作要点

## 快速开始

校验 skill 结构：

```bash
python /home/hansbug/.codex/skills/.system/skill-creator/scripts/quick_validate.py ./deck-workflow
```

初始化一个新的 deck 工作区：

```bash
python ./deck-workflow/scripts/init_deck_workspace.py ./tmp/example-deck \
  --title "Quarterly Business Review" \
  --author "HansBug" \
  --audience "Leadership team" \
  --duration-minutes 15 \
  --slides 12
```

初始化一个 Python 后端的 deck 工作区：

```bash
python ./deck-workflow/scripts/init_deck_workspace.py ./tmp/example-deck-python \
  --title "Quarterly Business Review" \
  --author "HansBug" \
  --audience "Leadership team" \
  --duration-minutes 15 \
  --slides 12 \
  --backend python
```

如果当前 Python 缺少 deck 依赖，先尝试在工作区里准备本地虚拟环境：

```bash
python3 -m venv ./tmp/example-deck-python/.venv
source ./tmp/example-deck-python/.venv/bin/activate
pip install -r ./tmp/example-deck-python/requirements.txt
```

检测当前环境里有哪些后端和 review 工具：

```bash
python ./deck-workflow/scripts/detect_deck_environment.py
```

把 deck 渲染成可供视觉检查的 PDF / PNG：

```bash
python ./deck-workflow/scripts/render_review.py ./tmp/example-deck/deck.pptx --output-dir ./tmp/example-deck/rendered
```

## Backend 策略

- 默认优先 Python。
- 如果缺的是 Python 依赖，先尝试工作区本地 `venv` 和 `requirements.txt`，不要一看到 import 缺失就直接退到 JavaScript。
- 如果 Python 路径仍然不现实，再退到 JavaScript。
- 如果两者都不合适，也应该保留同样的 guide-first 工作流，而不是直接丢掉上游规范。

## 面向观众的内容规则

- `s01-cover` 这类稳定 slide id 只用于 guide、代码、review note 和提交记录。
- 除非用户明确要求，否则不要把这些内部 id 直接放到页面可见区。
- 代码片段、行内代码标签、终端命令等代码相关可见文本默认应使用等宽字体。

## 持久化要求

deck 工作区应放在用户自己的 repo 或其他持久目录里。
如果后续还要继续改，就不要把 `PPT_GUIDE.md`、`generate_ppt.*` 和 `deck.pptx` 只放在临时 agent 目录里。

## 推荐搭配

这个 skill 很适合和 OpenAI 官方 `$slides` skill 配合使用：

- `$deck-workflow` 负责高层流程、guide、改动路由和 review 闭环
- `$slides` 负责底层 PptxGenJS helper、render 工具和 deck 校验

## 安装方式

如果要直接给 Codex 使用，可以把 `deck-workflow/` 复制或软链接到 Codex 的 skills 目录：

```bash
cp -R ./deck-workflow "${CODEX_HOME:-$HOME/.codex}/skills/"
```

如果你的环境支持显式 path，也可以直接引用本地 skill 路径。

## 许可证

本仓库使用 MIT License，详见 [`LICENSE`](./LICENSE)。
