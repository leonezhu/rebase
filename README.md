# 万灵变基录 · Rebase

> 万物皆分支，唯有强者能变基。
>
> A GitHub-native monster-raising battle game. Your repo is the world, PRs are rituals, and every beast writes its own chronicle.

**你的 Agent 就是游戏客户端。** 把本仓库的技能装给它，然后对它说"我要领养"——五分钟后你就有一只自己的灵兽。

> **世界观一句话**：碳基文明在某一天集体"大变基"——**只有意识能迁入异界**，与灵兽融合成形，任何实物都带不过去。灵智高者（人）保留历史，血脉之谜是**梦与画面**；灵智低者彻底融入异界，前世化作**说不清的习性偏执**。AI 是守仓人，负责维护这个世界，静候重逢。每只灵兽都不知道自己前世是谁——帮它想起来，就是养成的终极意义。

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

> 我要领养一只 Rebase 灵兽

Agent 会举行「问灵五问」（你怕什么/想要什么/从哪里来/你的火是什么颜色/只能记住一件事），把你的回答炼成它的样子与性子。入册时它还是一枚**灵兽之卵**（🥚 图鉴上属性全保密）——答完五问举行破壳仪式，第一眼才看到它真正的样子。

### 第 3 步：等缔约完成

GitHub Actions 自动校验并合并 PR，bot 开一个**降世 issue**——你灵兽的第一篇传记，里面埋着一条「血脉之谜」待你随境界解锁。

---

## ⚔️ 之后玩什么

| 指令 | 在哪 | 效果 |
|---|---|---|
| `/battle @对方` | 主仓库 issue 评论 | 发起斗法：hash 判定+五行相克+天赋觉醒；同级胜+30/+50，越级挑战胜×2.5，虐菜×0.4；败方 -15 灵石疗伤、心境低落 |
| `/battle --wild` | 斗法 issue 评论 | 野斗游魂：不点名对手，hash 从游魂名册抽签——练手+收集记忆残片线索 |
| `/explore` | 任意 issue 评论 | 秘境探索：动态遭遇池（共创投稿即全服生效），每兽每日 3 次，收获灵石/功力 |
| `/growth` | 降世 issue 追加修行行 | 同梦修行：每日 3 次陪它练功（+5 功/次），不耗灵石——功力是它自己练的 |
| `/abyss` | 任意 issue 评论 | **雾渊**：每周世界 Boss（走失意识淤成的雾障）全服讨伐，每兽每日 1 次；击杀触发灵石雨 |
| `/coordinate` | 任意 issue 评论 | 旧分支坐标探测（化神+，每日 1 次 50 灵石，全服共享进度，每 20 次揭示 1 枚碎片） |
| `/rebase` | 自己的灵兽 issue | 渡劫进化：功力灵石达标只是入场券——**心境昂扬 85%/平静 70% 成功率**，失败功力跌回七成、天劫费不退 |
| `/release` | 自己的灵兽 issue | 放生：灵兽归隐成 NPC，名字入灵籍史册 |

### 🏷️ issue 标签导航

每个 issue 的标签就是它的身份——按标签逛仓库即可找到同类事件：

| 标签 | 含义 |
|---|---|
| 降世 | 灵兽传记 issue，每兽一个，永久存在 = 灵兽主页/操作台 |
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

- **七境**：炼气 → 筑基 → 金丹 → 元婴 → 化神 → 渡劫 → 大乘（门槛指数化：150/500/1500/4000/10000——每个境界待出故事来）
- **五行相克**：金→木→土→水→火→金（伤害 ±15%）
- **五维基因**：灵（法术）/ 魄（体质）/ 巧（敏捷）/ 韧（意志）/ 韵（灵性——韵值越高，你的灵兽传记写得越华丽）
- **生存式成长**（没有喂养，只有生存）：它在异世界自己觅食、修行、拾遗——资源是它挣的；你能做的是**同梦**（陪它修行）、**传念**（影响它今日去向）、**收纳**（它捡到旧世界记忆凝成的物件会献给你）
- **心境系统**：昂扬 ×1.03 / 低落 ×0.97——由当日经历涨落，还决定渡劫成败（心魔未平，雷劫必劈）
- **称号系统**：初鸣/越级斩/败者复起/破雷者/踏雾者/寻珍者……威名自动授予，只增不减

完整设计文档：[DESIGN.md](DESIGN.md)

---

## 🛠️ 技术形态（给好奇的人）

零后端。GitHub 就是服务器：

| 概念 | 实现 |
|---|---|
| 游戏服务器 | 本仓库（public，Actions 免费无上限） |
| 规则引擎 | `.github/workflows/` |
| 官方账本（灵籍） | `monsters/`（仅 `github-actions[bot]` 可写） |
| 玩家本地 | `~/.rebase/`（日记+缓存，删了不丢灵兽） |
| 反作弊 | 数值只认 bot commit + hash 确定性模拟 + 公开 diff 审计 |

状态推进全部通过 PR / issue / 评论驱动。

**手动玩家路线**（不用 Agent，`gh` CLI 全流程）：

```bash
# 1. 缔约：写好灵兽 YAML 提交注册 PR
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

- 缔约灵兽：**拾焰**（火，@leonezhu，炼气期）——怕安静、想被需要、来自一场没做完的对话
- 游魂野斗名册：雷骨（金）/ 尘舟（水）/ 砚灰（土）——融合失败的走失意识，`/battle --wild` 可遇
- 归隐 NPC：**燧鸣**（火，金丹）——曾任缔约者首兽，两段血脉，如今在浅滩与山梁间自在游荡 · 墨霄（水）· 鲁灵（金）
- 斗法志：历史对战与半场解说 [chronicle/](chronicle/) ｜ 图鉴 [codex.html](https://leonezhu.github.io/rebase/codex.html)

## License

MIT
