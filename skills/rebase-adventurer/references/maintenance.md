# Skill 维护与部署（references）

## 架构（v3.0）

```
仓库(唯一真源)                          本地(symlink, 永不编辑)
skills/rebase-adventurer/               ~/.hermes/skills/gaming/rebase-adventurer/
├── SKILL.md          ←────symlink────  SKILL.md
└── references/
    └── maintenance.md (本文件)

GAMEBOOK.md (仓库根)  = 机制唯一真源
SKILL.md              = 玩家客户端文风/叙事铁律
```

## 部署（新机器/其他 Agent 客户端）

```bash
# Hermes/OpenClaw
mkdir -p ~/.hermes/skills/gaming/rebase-adventurer
ln -sf <仓库路径>/skills/rebase-adventurer/SKILL.md        ~/.hermes/skills/gaming/rebase-adventurer/SKILL.md

# Claude Code（同样方式）
mkdir -p ~/.claude/skills/rebase-adventurer
ln -sf <仓库路径>/skills/rebase-adventurer/SKILL.md        ~/.claude/skills/rebase-adventurer/SKILL.md
```

## 铁律

1. **本地 skill 是 symlink，永不直接编辑**——要改就改仓库源文件，commit+push
2. **机制细节进 GAMEBOOK.md，不进 SKILL.md**——skill 只管文风/叙事/交互
3. 改 SKILL.md 前先 `bump version`（语义：主版本=玩法大改，次版本=规则微调）
4. 远端协作者（无法 symlink 的环境）才用旧式下载覆盖：
   `curl -sL https://raw.githubusercontent.com/leonezhu/rebase/main/skills/rebase-adventurer/SKILL.md -o <目标>`

## 演进记录

- v2.x 单文件时代：309 行塞四种内容，双份手动同步漂移 5 次/天 → 已废
- v3.0（2026-10-15）：GAMEBOOK/SKILL 两层拆分 + symlink 部署。63% 机制内容迁入 GAMEBOOK
