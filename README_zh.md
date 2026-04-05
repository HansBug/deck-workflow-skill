# deck-workflow-skill

`deck-workflow-skill` 是一个 Codex 兼容 skill 的源码仓库。它的目标不是“一次性生成一个 PPT”，而是把 PPT 制作变成一条可反复迭代的生产流程。

真正可安装的 skill 位于 [`deck-workflow/`](./deck-workflow)。仓库根目录补充了 repo 级说明、维护约定和版本管理文件。

## 这个 Skill 解决什么问题

适用于下面这类需要持续迭代的 deck 工作：

- 新建一套演示文稿
- 重构已有 deck 的结构和叙事
- 根据人类反馈做多轮修改
- 反复进行视觉验收和增量修复
- 希望把“内容意图”和“实现代码”拆开维护的场景

这套 skill 的核心工作流是：

1. 先写 `PPT_GUIDE.md`
2. 再写 `generate_ppt.*`
3. 把结果渲染出来做视觉检查
4. 后续修改时，把改动明确路由到 guide、脚本或两者

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

## 安装方式

如果要直接给 Codex 使用，可以把 `deck-workflow/` 复制或软链接到 Codex 的 skills 目录：

```bash
cp -R ./deck-workflow "${CODEX_HOME:-$HOME/.codex}/skills/"
```

如果你的环境支持显式 path，也可以直接引用本地 skill 路径。

## 许可证

本仓库使用 MIT License，详见 [`LICENSE`](./LICENSE)。
