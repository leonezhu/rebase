# 安装与维护（references）

## 安装（新环境）

本 skill 的唯一真源在仓库 `skills/rebase-adventurer/`。

**推荐（本机有仓库 clone 时）**：把 skill 目录 symlink 进你的 Agent 技能目录——

```bash
ln -s <仓库路径>/skills/rebase-adventurer <你的Agent技能目录>/rebase-adventurer
```

symlink 方式下改仓库源文件，安装的 skill 即时同步，永远只有一份。

**备选（远端/无文件权限）**：下载覆盖——

```bash
curl -sL https://raw.githubusercontent.com/leonezhu/rebase/main/skills/rebase-adventurer/SKILL.md \
  -o <你的Agent技能目录>/rebase-adventurer/SKILL.md
```

下载方式会脱离真源，之后每次更新都要重新下载。

## 维护铁律

1. **symlink 安装的本地 skill 永不直接编辑**——要改就改仓库源文件，commit+push
2. **机制细节进 GAMEBOOK.md（仓库根），不进 SKILL.md**——skill 只管文风/叙事/交互；GAMEBOOK 是机制唯一真源
3. 改 SKILL.md 前先 bump version（主版本=玩法大改需重读手册；次版本=规则微调）
4. 通用 Agent 知识（异步执行/命令速查/调试坑）放本 references/ 目录，SKILL.md 保持精简

## 结构

```
skills/rebase-adventurer/
├── SKILL.md                       # 文风/叙事/交互铁律（加载即读）
└── references/
    ├── async-execution.md         # 异步执行模式（触发结算时读）
    ├── commands-and-pitfalls.md   # 命令速查+workflow调试坑（操作时读）
    └── maintenance.md             # 本文件（安装/维护）
```
