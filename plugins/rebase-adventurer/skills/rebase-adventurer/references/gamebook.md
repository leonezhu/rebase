# 天道运行手册（GAMEBOOK）

> 万灵变基录 · 机制唯一真源。Agent 的客户端 skill 只管文风与叙事，**所有机制细节以此文件为准**。
> 改规则只改这里——客户端 skill 引用本文件，永不复制内容。

## 传记与自由书写（玩家 own 自己的故事）

传记 tales/<owner>-<角色名>.md 是**玩家自己的地盘**：玩家（或其 Agent）可以直接 PR 续写
自己的传记——遭遇、心境、 日常小事，不必等天道结算。自动收录守卫只查路径与
YAML，文风好坏由读者裁。唯一红线：**别人的传记不许碰**（产权），机制数值与天道结算
不一致时以天道为准（叙事可以润色，事实不能篡改）。

## 传记更新纪律（两通道，传记必须更新）

1. **命令通道**（/explore 天道结算）：explore.yml 自动续写——无需手动
2. **对话通道**（对话驱动的剧情）：Agent 写完叙事必须调用：
   `python3 scripts/append-tale.py <角色名> <回目名>` + stdin 正文
   （回目自增、全卷终保护由脚本负责）
3. **自检**：给玩家的回复发出前，默查本次剧情是否已入传

## 世界记忆账本

`world/eventlog/YYYY-MM.yaml` append-only——所有事件必须登记
（day/actor/where/what/consequence/evidence）。传记校验法：读传记回对账本与角色
原属性，对不上 = 不合理，Agent 自己合理化，不许凭空发生。

## 空间合理性

- 角色原属性：`where`（地点 id）+ `activity`（biguan/wujian/daokan/traveling/none）
- 交互闸（scripts/co-location.py）：异地不能打；闭关不能扰；退场不接战
- `/travel <地点id>`：移动（explore.yml travel job）；地点表 world/locations/

## 自由度与因果

- 探索/修行不限次数，无体力墙
- `kind: player` 永不真死（重伤+跌一境）；`kind: npc` 可杀（兵解，遗蜕归胜者）
- 恶名：杀良民（notoriety<40）+15；≥40 天下悬赏
- 叙事转译：灵性=伤势气血；恶名=江湖风评；兵解=遗体与遗物
- 生成 NPC：`players/npc-<名>.yaml`（kind: npc + 灵根/功法/法宝/来历）入库，生死自负

## 转世规则

- 从零转世：与前世零关联（无记忆/属性/因果）
- 种子：owner+精确时刻+随机salt → 灵根彻底重掷
- 玩家明说"彻底全新"才走此流程；默认延续当前角色

## 公共资产入库（world/）

- 新功法/法宝/地点/NPC → yaml 入 world/（模板 world/SCHEMA.md）
- `first_seen` 写哪条支线；`origin` append-only 永不改
- 玩家档案只记持有，资产本体在 world/；NPC unique:true 全局唯一

## 角色档案字段

- `kind`（player/npc）、`where`、`activity`、`notoriety`、`status`（retired/fallen）
- chronicle append-only（D<天数> · 一句）；open_loops 伏笔账本（open→resolved）
- 灵根 hash 派生：sha256(owner|created_at)，Agent 不许自选

## 世界仓库解析（关键：先于一切 gh 命令）

**所有 gh 命令必须带正确的 `-R <owner/repo>`。解析顺序：**

1. **自动探测（首选）**：Agent 本地有仓库 clone 时，从 git remote 推断：
   ```bash
   REPO=$(git -C <仓库路径> remote get-url origin | sed -E 's#.*github.com[:/]##; s/\.git$//')
   ```
2. **会话配置**：玩家说过"我在用 xxx/rebase 玩"→ 记住，本次会话全程用它
3. **默认兜底**：`leonezhu/rebase`（公共世界——所有玩家共享同一个天道与世界资产）

**给玩家的话术**：
- "直接来公共世界玩" → 什么也不用配，默认就是 leonezhu/rebase，你的角色/剧情/资产入公共账
- "我想有自己的世界" → fork 仓库，开启 Actions，然后把 fork 地址告诉 Agent（或本地 clone 后由 remote 自动推断）

公共世界的好处：世界资产（功法/地点/NPC/事件）所有人共享——别人留下的洞府可能是你的机缘。

## 命令速查（Agent 自用）

```bash
# 读玩家档案
gh api repos/$REPO/contents/players/<玩家名>.yaml --jq .content | base64 -d

# 斗法（两步：建 issue + 补评论触发）
gh issue create -R "$REPO" -t "斗法：A 挑战 B" -b "/battle @B"
gh issue comment <issue号> -R "$REPO" -b "/battle @B"

# 盯 workflow（放后台）
gh run watch <run-id> -R "$REPO" --exit-status

# 传记入传（对话通道）
python3 scripts/append-tale.py <角色名> <回目名> <<'EOF'
正文...
EOF
```

## 异步执行铁律

天道结算 30~90 秒，**绝不阻塞玩家主线程**：提交指令 → 交后台/子线程轮询 → 立即回复
玩家 → 结果出来再叙事。禁止主线程 sleep 循环。各动作耗时：觉醒 20~60s / 斗法
40~90s / 探索 30~60s / 修行 20~40s。

## 已知坑（workflow 调试）

- **改 workflow 必跑 actionlint**：YAML safe_load 通过 ≠ GitHub schema 通过
- 已实锤：①bash 变量写成 `${{WINNER}}`（=GitHub expression → 骨架 failure，特征：
  jobs 空 + run name = 文件路径）；②python heredoc 忘 import（运行时炸）；③
  `grep -oP '[a-zA-Z0-9-]+'` 匹配不到中文；④comment.body 直接内联有注入风险（经 env 传）
- 斗法 issue 标签状态机：待战 → 已判 → 已收录
- `/battle` 建议建 issue 后补一条评论触发，时序更稳

## 边界

- 玩家未觉醒只引导觉醒；API 失败告知"天道暂时不可及"，不重试轰炸
- 注销走 issue `/release`，绝不直接删文件
- 规则争议以 DESIGN.md 为准
