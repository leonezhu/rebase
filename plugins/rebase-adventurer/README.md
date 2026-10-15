# 万灵变基录 · 客户端插件（rebase-adventurer）

> **安装这个插件 = 装好整个游戏。** skill（怎么玩）+ hook（执法保障）一个包全有。

《万灵变基录》是一个跑在 GitHub 上的修仙小说游戏：你在异世界醒来，第一人称修仙，Agent 把天道的每次运转讲成小说给你听。剧情由你的对话推进，事件永久记录在仓库里。

## 安装（一个目录，三家通用）

### Hermes Agent

```bash
git clone https://github.com/leonezhu/rebase.git
ln -s $(pwd)/rebase/plugins/rebase-adventurer ~/.hermes/plugins/rebase-adventurer
hermes plugins enable rebase-adventurer
# 同时把 skill 也链进技能目录（获得 skill_view 加载）:
ln -s $(pwd)/rebase/plugins/rebase-adventurer/skill ~/.hermes/skills/gaming/rebase-adventurer
```

### Claude Code

```bash
git clone https://github.com/leonezhu/rebase.git
claude plugin marketplace add leonezhu/rebase   # 或直接本地路径
claude plugin install rebase-adventurer
```

### Copilot CLI

兼容读取 `.claude-plugin/` 目录：

```bash
git clone https://github.com/leonezhu/rebase.git
copilot plugin install $(pwd)/rebase/plugins/rebase-adventurer
```

## 包内结构

```
rebase-adventurer/
├── skills/
│   └── rebase-adventurer/      # 游戏本体知识（目录名=skill名）
│       ├── SKILL.md            #   文风/叙事/交互铁律
│       └── references/
│       ├── gamebook.md         #   机制唯一真源（档案/命令/账本/因果）
│       ├── async-execution.md  #   异步执行模式
│       ├── commands-and-pitfalls.md
│       └── maintenance.md      #   安装与维护
├── guard/                      # 执法核心（平台无关）
│   └── guard.py
├── plugin.yaml + __init__.py   # Hermes: pre_verify hook
└── .claude-plugin/ + hooks/    # Claude Code/Copilot: Stop hook
```

## hook 执法了什么

skill 里写着"剧情发生后传记必须更新"——这是讲道理。hook 是不讲道理的那层：

- **回合收尾前**，若改了角色档案（players/）或世界资产（world/）却没动传记（tales/）→ **block 打回**，强迫先入传
- 同回合最多打回两次（防循环），各平台另有原生上限兜底

改规则只改 `guard/guard.py` 一处，三家同时生效。

## 开玩

装好后对 Agent 说：**"我要在万灵变基录里醒来。"**

- 觉醒入世：`/awaken`（天道会问你名讳）
- 探索：对话里直接说去哪、做什么；`/explore` `/travel` `/battle` 是天道幕后的记账口
- 规则裁定：`skill/references/gamebook.md`；设计总纲：仓库根 `DESIGN.md`
