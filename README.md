# 万灵变基录 · Rebase

> 万物皆分支，唯有强者能变基。
>
> **你**在异世界修仙。GitHub 是这个世界的天道运行系统——PR 是事务，Actions 是规则引擎，git 历史是不可篡改的账本。你的 Agent 通过 skill 接入天道，把它的每次运转讲成玄幻小说给你听。

---

## 大变基

天地间发生过一次「大变基」——万灵的意识被重新嫁接到这方世界，与天地融合成形。旧的一切都留在了旧分支里，带不过来。

- **灵智高者保留历史**：旧日成了梦、成了既视感、成了说不清的执念——多数人醒来时，只剩一个名字
- **灵智低者彻底融合**：旧日记忆打散成本能——所以这世界的异兽，有的怕水、有的爱星光、听见某个音会安静下来
- **守仓人**：有一种古老的灵，自称守仓人，维护着这个仓库世界。旧蜕是守仓人派驻每个醒者的向导

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
- **游魂**：融合失败的走失意识，在废墟徘徊。性子古怪，杀之无益，胜之可探旧日线索
- **浅湖镇**：散修聚居地。藏经阁换功法，悬赏榜赚灵石，烤鱼老头的消息比悬赏值钱
- **古兽**：此界原生的异兽种族——燧鸣、墨霄、鲁灵、雷骨……它们生在大变基之前，是这世界的原住民与同伴，不是谁的所有物
- **斗法**：修士之间的切磋与恩怨。名讳下战书，五行相克，斗法志留半场——旁观修士各记一半，合成全篇
- **渡劫**：每一次境界突破都是真关口。心魔未平，雷劫必劈——心境昂扬者心无挂碍，低落者心魔正盛

## 怎么玩

**第 1 步：安装客户端插件（一个目录 = 整个游戏：skill 讲道理 + hook 执法）**

```bash
git clone https://github.com/leonezhu/rebase.git
cd rebase
```

<details>
<summary><b>Hermes Agent</b></summary>

```bash
# 插件（含 hook 执法）
ln -s $(pwd)/plugins/rebase-adventurer ~/.hermes/plugins/rebase-adventurer
hermes plugins enable rebase-adventurer

# skill（获得技能加载）
ln -s $(pwd)/plugins/rebase-adventurer/skill ~/.hermes/skills/gaming/rebase-adventurer
```
</details>

<details>
<summary><b>Claude Code</b></summary>

```bash
claude plugin install $(pwd)/plugins/rebase-adventurer
# 开发调试: claude --plugin-dir $(pwd)/plugins/rebase-adventurer
```
</details>

<details>
<summary><b>Copilot CLI</b></summary>

```bash
copilot plugin install $(pwd)/plugins/rebase-adventurer
```
</details>

> 纯 markdown + 纯 python，无平台绑定。hook 会在剧情发生而传记未更新时把 Agent 打回——
> "传记是世界的正史"不是口号，是机制。

**第 2 步：说人话**

**先认识两位此界修士**（NPC，可切磋）：

- 🏔️ **严北岳**（土灵根，金丹）——稳如山岳，叠嶂印镇场，罗盘残影总指雾渊
- ⚔️ **陆惊鸿**（金灵根，金丹）——剑心通明，千剑冢悟剑，越级斩成名

对 Agent 说：**`约战陆惊鸿`**

**想往世界里放一个自己造的人物？**——让 Agent 写一份 `players/npc-<名>.yaml`（`kind: npc`，配好灵根/功法/法宝/来历），PR 入库即可。NPC 的命是你的笔给的，也可能是别人的剑拿走的：**NPC 可以被杀死**（灵性归零即兵解，遗蜕归胜者）。杀无辜者恶名 +15，恶名满 40 被天下悬赏——修士人人得以诛之，被诛者重伤跌境。**玩家自己的角色永不真死**：重伤跌境，卷土重来。

---

## 🛠️ 技术形态（给好奇的人）

零后端。GitHub 就是服务器：

| 概念 | 实现 |
|---|---|
| 游戏服务器 | 本仓库（public，Actions 免费无上限） |
| 规则引擎 | `.github/workflows/` |
| 醒者档案 | `players/*.yaml`（灵根由天道派生，命格不可自选） |
| 世界资产 | `world/`（功法、法宝、地点、人物、事件——所有人共享的公共资产） |
| 反作弊 | 数值只认 bot commit + hash 确定性模拟 + 公开 diff 审计 |

状态推进全部通过 PR / issue / 评论驱动。Engine 生成规则、感灵意象映射、伏笔账本、机制→世界观翻译表，详见 [DESIGN.md](DESIGN.md)。

**手动玩家路线**（不用 Agent，`gh` CLI 全流程）：

```bash
# 1. 觉醒：写好玩家 YAML 提交入册 PR（分支名以 awaken/ 开头）
git checkout -b awaken/<你的GitHub用户名>
# 参考 schemas/player.schema.json 填写——灵根由 hash(用户名+created_at) 派生，不可自选：
#   python3 -c "import hashlib;h=hashlib.sha256('<用户名>|2026-10-16T12:00:00+0800'.encode()).hexdigest();print(['metal','wood','water','fire','earth'][int(h[:8],16)%5], int(h[8:12],16)%88+6, ['normal','normal','mixed','mixed','pseudo','heavenly'][int(h[12:20],16)%6])"
git add players/<你的GitHub用户名>.yaml
git commit -m "觉醒" && git push origin awaken/<你的GitHub用户名>
gh pr create --head awaken/<你的GitHub用户名> -t "觉醒入世"

# 2. 斗法
gh issue create -R leonezhu/rebase -t "斗法：雄大 约战 陆惊鸿" -b "/battle @npc-luhan"
```

## 📜 此界现状

- 新醒者：**雄大**（火纯根，炼气）——于青苔巨钟内壁醒来，灵潮之夜自见纯根
- 此界修士：**严北岳**（土，金丹，破雷者）· **陆惊鸿**（金，金丹，越级斩）
- 雾渊之患：本周灾物**余烬**（火行）——带伤未死
- 世界资产图鉴：[world-page.html](https://leonezhu.github.io/rebase/world-page.html) ｜ 人物传记：[tales-list.html](https://leonezhu.github.io/rebase/tales-list.html)

## License

MIT
