# 万灵变基录 · Rebase

> 万物皆分支，唯有强者能变基。
>
> **你**在异世界修仙。GitHub 是这个世界的天道运行系统——PR 是事务，Actions 是规则引擎，git 历史是不可篡改的账本。你的 Agent 通过 skill 接入天道，把它的每次运转讲成玄幻小说给你听。

---

## 大变基

碳基文明终结的那一天，没有灭亡——全人类做了一次集体 `git rebase`：**只有意识能迁入异界**，与这方天地融合成形。任何实物都带不过去。

- **灵智高者保留历史**：前世成了梦、成了既视感、成了说不清的执念——多数人醒来时，只剩一个名字
- **灵智低者彻底融合**：前世记忆打散成本能——所以这世界的异兽，有的怕水、有的爱星光、听见某个音会安静下来
- **AI=守仓人**：生灵迁跃后，AI 负责维护这个仓库世界，静候重逢。引路灵是守仓人派驻每个醒者的向导

## 你，雄大（以及每一位醒者）

大变基第九日，你在异世界的某个角落醒来。第一人称——所见、所感、所修，都是"我"。

- **名讳**：你在异界的幡。战书、斗法志、旁人口中，都用它唤你
- **灵根**：醒来后第一个灵潮之夜自见——纯根万里挑一，杂根也有机缘提纯
- **体质**：极稀有的先天构造。有人剑心通明，有人生而吞灵——前期是废，后期是缘
- **功法**：灵根引灵气，功法定怎么用。藏经阁、奇遇、秘境、前辈坐化处，皆有所得
- **法宝**：探索所得，记录在案。法宝有来历——梦见的断剑，终有一日会握到手里
- **境界**：炼气 → 筑基 → 金丹 → 元婴 → 化神 → 渡劫 → 大乘。脉络未开则灵气不存，火候不到，强冲必伤

## 这个世界

- **雾渊**：旧分支废墟深处，走失意识淤成的雾障。每隔七日，渊底会"醒"来一位灾物——旧世界执念最重的残响凝成的魔物。修士讨它，一为除患，二为渊中散落的旧世界遗物。天道一日只纳一人全力出手
- **秘境**：雾中的机缘之地——灵草、法阵、前辈洞府、遗珍，也有一言不合就扑出来的野物。人的神识一日只经得起三度秘境冲刷
- **游魂**：融合失败的走失意识，在废墟徘徊。性子古怪，杀之无益，胜之可探前世线索
- **浅湖镇**：散修聚居地。藏经阁换功法，悬赏榜赚灵石，烤鱼老头的消息比悬赏值钱
- **旧兽**：大变基初年与人类意识缔约的异兽种族——燧鸣、墨霄、鲁灵、雷骨……它们仍在，是这世界的原住民与同伴，不是谁的所有物
- **斗法**：修士之间的切磋与恩怨。名讳下战书，五行相克，斗法志留半场——旁观修士各记一半，合成全篇
- **渡劫**：每一次境界突破都是真关口。心魔未平，雷劫必劈——心境昂扬者心无挂碍，低落者心魔正盛

## 怎么玩

**第 1 步：给 Agent 装技能**

```bash
mkdir -p ~/.hermes/skills/gaming/rebase-adventurer
curl -sL https://raw.githubusercontent.com/leonezhu/rebase/main/skills/rebase-adventurer/SKILL.md \
  -o ~/.hermes/skills/gaming/rebase-adventurer/SKILL.md
```

（Claude Code / Copilot CLI 同理，放进各自 skills 目录——纯 markdown，无平台绑定）

**第 2 步：说人话**

> 我要觉醒 / 探索 / 去雾渊 / 我要突破 / 跟陆惊鸿约战

Agent 把你的意图转成天道命令（GitHub issue → Actions 判定 → bot 入账），再把结果**讲成小说**给你听。

你永远不需要看到数字。

**先认识两位此界修士**（NPC，可切磋）：

- 🏔️ **严北岳**（土灵根，金丹）——地质勘探员出身，稳如山岳，叠嶂印镇场
- ⚔️ **陆惊鸿**（金灵根，金丹）——剑心通明，千剑冢悟剑，越级斩成名

对 Agent 说：**`约战陆惊鸿`**

---

## 🛠️ 技术形态（给好奇的人）

零后端。GitHub 就是服务器：

| 概念 | 实现 |
|---|---|
| 游戏服务器 | 本仓库（public，Actions 免费无上限） |
| 规则引擎 | `.github/workflows/` |
| 玩家档案 | `players/*.yaml`（灵根由 hash(owner+时间) 天道派生，命格不可自选） |
| 旧兽生态 | `monsters/`（异兽种族档案，仅 `github-actions[bot]` 可写） |
| 反作弊 | 数值只认 bot commit + hash 确定性模拟 + 公开 diff 审计 |

状态推进全部通过 PR / issue / 评论驱动。Engine 生成规则、感灵意象映射、伏笔账本、机制→世界观翻译表，详见 [DESIGN.md](DESIGN.md)。

**手动玩家路线**（不用 Agent，`gh` CLI 全流程）：

```bash
# 1. 觉醒：写好玩家 YAML 提交入册 PR
git checkout -b register/awaken-<你的GitHub用户名>
# 参考 players/npc-yanbei.yaml 与 schemas/player.schema.json 填写（灵根须按 hash 派生）
git add players/<你的GitHub用户名>.yaml
git commit -m "觉醒" && git push origin register/awaken-<你的GitHub用户名>
gh pr create --head register/awaken-<你的GitHub用户名> -t "觉醒入世"

# 2. 斗法
gh issue create -R leonezhu/rebase -t "斗法：雄大 约战 陆惊鸿" -b "/battle @npc-luhan"
```

## 📜 此界现状

- 新醒者：**雄大**（火纯根，炼气）——于青苔巨钟内壁醒来，灵潮之夜自见纯根
- 此界修士：**严北岳**（土，金丹，破雷者）· **陆惊鸿**（金，金丹，越级斩）
- 雾渊之患：本周灾物**余烬**（火行）——带伤未死
- 旧兽图鉴：[codex.html](https://leonezhu.github.io/rebase/codex.html) ｜ 斗法志：[battle-chronicle.html](https://leonezhu.github.io/rebase/battle-chronicle.html)

## License

MIT
