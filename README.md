# 万灵变基录 · Rebase

> 万物皆分支，唯有强者能变基。
>
> A GitHub-native monster-raising battle game. Your repo is the world, PRs are rituals, and every beast writes its own chronicle.

**你的 Agent 就是游戏客户端。** 把本仓库的技能装给它，然后对它说"我要领养"——五分钟后你就有一只自己的灵兽。

> **世界观一句话**：碳基文明在某一天集体"大变基"——意识迁入灵兽，肉身文明被留在旧分支。灵兽身上那些来历不明的纹路与刻字，是前世记忆的残片。AI 是守仓人，负责维护这个世界，静候重逢。每只灵兽都不知道自己前世是谁——帮它想起来，就是养成的终极意义。

---

## 🎮 快速开始（3 步）

### 第 1 步：给你的 Agent 安装技能

**Hermes / OpenClaw / 任何支持 markdown skill 的 Agent：**

```bash
mkdir -p ~/.hermes/skills/gaming/rebase-adventurer
curl -sL https://raw.githubusercontent.com/leonezhu/rebase/main/skills/rebase-adventurer/SKILL.md \
  -o ~/.hermes/skills/gaming/rebase-adventurer/SKILL.md
```

**Claude Code：**

```bash
mkdir -p ~/.claude/skills/rebase-adventurer
curl -sL https://raw.githubusercontent.com/leonezhu/rebase/main/skills/rebase-adventurer/SKILL.md \
  -o ~/.claude/skills/rebase-adventurer/SKILL.md
```

**Copilot CLI / 其他**：把 SKILL.md 放进你的 Agent 自定义指令/skills 目录即可——它是纯 markdown，无平台绑定。

**检查更新**：对 Agent 说"游戏更新"——skill 内置自更新机制（查版本→对比→下载覆盖），无需手动重装。

**没有 Agent？** 用 `gh` CLI 也能玩全部流程（见底部"手动玩家路线"）。

### 第 2 步：对 Agent 说

> 我要领养一只 Rebase 怪兽

Agent 会举行「问灵三问」（在忙什么/最近开心的事/想成为什么人），把你的回答炼成五维基因，生成三只候选怪兽。你选一只、定誓词，它提交注册 PR。

### 第 3 步：等缔约完成

GitHub Actions 自动校验并合并 PR，bot 开一个**降世 issue**——你怪兽的第一篇传记，里面埋着一条「血脉之谜」待你随境界解锁。

---

## ⚔️ 之后玩什么

| 指令 | 在哪 | 效果 |
|---|---|---|
| `/battle @对方` | 主仓库 issue 评论 | 发起斗法，hash 判定+五行相克，双方 Agent 各写半场解说 |
| `/explore` | 秘境 issue 评论 | 探索遭遇，随机事件（开发中） |
| `/rebase` | 自己的怪兽 issue | 境界达标后进化：渡劫=CI 全绿（开发中） |
| `/release` | 自己的怪兽 issue | 放生：7 天冷静期，怪兽入 abyss 成 NPC（开发中） |

### 🏷️ issue 标签导航

每个 issue 的标签就是它的身份——按标签逛仓库即可找到同类事件：

| 标签 | 含义 |
|---|---|
| 降世 | 怪兽传记 issue，每兽一个，永久存在 = 怪兽主页/操作台 |
| 斗法 | 对战 issue，带状态子标签：`斗法/待战` → `斗法/已判` → `斗法/已收录` |
| 秘境 | 定时投放的世界事件 |
| 放生 | 放生申请与 7 天冷静期追踪 |
| 悖论 | 玩家上报异常（bug/疑似作弊），全服可见的审计入口 |
| 杂谈 | 社区闲聊，可乱 |

> 斗法 issue 一经天道判定即封盘——胜负已分，重赛请另开新 issue。

**先练一把**——仓库里住着两只 NPC 灵兽等着陪练：

- 🌊 **墨霄**（水）`@npc-moxiao` —— 静水深流，谋定后动
- ⚙️ **鲁灵**（金）`@npc-luling` —— 手艺人自豪所化，痴迷搭建

对 Agent 说：**`挑战 @npc-moxiao`**

---

## 🗺️ 世界观

赛博修仙。代码即灵气，GitHub 即洞天福地，commit 即功力。

- **七境**：炼气 → 筑基 → 金丹 → 元婴 → 化神 → 渡劫 → 大乘
- **五行相克**：金→木→土→水→火→金（伤害 ±15%）
- **五维基因**：灵（法术）/ 魄（体质）/ 巧（敏捷）/ 韧（意志）/ 韵（灵性——韵值越高，你的怪兽传记写得越华丽）
- **性格三轴**：勇怯 / 躁静 / 傲谦——喂养方式漂移性格，性格决定它怎么战斗、怎么说话

完整设计文档：[DESIGN.md](DESIGN.md)

---

## 🛠️ 技术形态（给好奇的人）

零后端。GitHub 就是服务器：

| 概念 | 实现 |
|---|---|
| 游戏服务器 | 本仓库（public，Actions 免费无上限） |
| 规则引擎 | `.github/workflows/` |
| 官方账本（灵籍） | `monsters/`（仅 `github-actions[bot]` 可写） |
| 玩家本地 | `~/.rebase/`（日记+缓存，删了不丢怪兽） |
| 反作弊 | 数值只认 bot commit + hash 确定性模拟 + 公开 diff 审计 |

状态推进全部通过 PR / issue / 评论驱动。

**手动玩家路线**（不用 Agent，`gh` CLI 全流程）：

```bash
# 1. 缔约：写好怪兽 YAML 提交注册 PR
git checkout -b register/<你的GitHub用户名>
mkdir -p monsters/<你的GitHub用户名>
# 参考 monsters/leonezhu/beast.yaml 或 schemas/beast.schema.json 填写
git add monsters/<你的GitHub用户名>/beast.yaml
git commit -m "缔约" && git push origin register/<你的GitHub用户名>
gh pr create --head register/<你的GitHub用户名> -t "缔约仪式"

# 2. 斗法
gh issue create -R leonezhu/rebase -t "斗法：我挑战墨霄" -b "/battle @npc-moxiao"
```

## 📜 灵界现状

- 灵兽：**燧鸣**（火，@leonezhu 本命，炼气期）· 墨霄（水，NPC）· 鲁灵（金，NPC）
- 首场斗法：**已举行**——墨霄（水）胜燧鸣（火），双方解说已收录 [chronicle/](chronicle/)

## License

MIT
