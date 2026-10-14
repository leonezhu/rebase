# 迭代日志（ITERATION）

> 夜间 cron 每轮迭代在此记录。设计定案由主会话写入，施工项完成后打勾。

## 施工清单（cron 按序取项，每轮一项）

- [x] 1. 修 register.yml 的 YAML 解析 bug：awk 提取 origin 对多行不健壮 → 改 python yaml 库解析；顺带修复降世 issue 正文漏 YAML 原文问题（根因同一个）✅ 2026-10-14（origin/mystery 全文入正文，GITHUB_ENV heredoc 传变量，本地对真实灵籍演练断言通过）
- [x] 2. explore.yml 秘境探索 workflow：issue 评论 `/explore` 触发 → hash 定遭遇表 → bot 贴事件故事 → 灵石/经验入账 bot commit ✅ 2026-10-14（8 种遭遇加权随机，种子=评论者+评论id+当日次数可复现不可操控；每兽每日限 3 次按 bot commit 记录查重；败遭遇灵石保底不为负；本地演练权重分布+保底+语法断言全过）
- [x] 3. catalog.yml + Pages 图鉴：main push 时扫描 monsters/*.yaml 生成玄幻暗色静态 HTML → GitHub Pages ✅ 2026-10-14（3 册灵籍本地渲染断言通过；Pages 已于同日用 API 启用 build_type=workflow，首次部署成功，线上 https://leonezhu.github.io/rebase/ 已含 3 册灵籍）
- [x] 4. PR 双轨制（v0.6 设计定案，见下）✅ 2026-10-14（register.yml 双轨分流：主人=自动合并/其他玩家=止步 player/待审 禁止自动合并；降世 issue 统一移到 merged 后开（双通道通用+幂等防重+打「降世」标签）；新增 labels.yml=meta/规则 自动打标；CODEOWNERS=* @leonezhu；battle/explore 的 bot PR 打 game/bot；9 个游戏标签已用 API 建入仓库；本地 24 项断言全过）
  - ⚠️ 遗留：CODEOWNERS 的强制 review 需仓库 Settings → Branch protection 开启 "Require review from Code Owners"，workflow 层无法代设，待主人在网页端开启
- [x] 5. issue 标签体系（v0.6 设计定案，见下）✅ 2026-10-14（9 个游戏标签已提前用 API 建入仓库；battle.yml：/battle 触发打「斗法」+「斗法/待战」，结算贴结果前打「斗法/已判」；labels.yml 新增 ensure-labels push 兜底 job 幂等补建全部游戏标签（含斗法三态子标签）；README 增「issue 标签导航」表；本地 YAML+断言校验全过；push 后线上 ensure-labels 实跑 success，斗法三态子标签已在仓库生效）

- [x] 6. 守仓人低语（T2-2，v0.11）✅ 2026-10-14（schema 先行=schemas/whisper.schema.json 纯叙事硬边界：≤200字/零数值字段/占位符≤2——铁律"叙事归玩家数值归系统"由 schema 落地；文案池 lore/whispers.yaml 8条+whisper-pick.py 本地6断言全过（其间修掉一个断言自写错的假红灯A5）；whisper.yml 每周一确定性投递；e2e 三跑实锤：首跑投递步骤恒 skip → 根因 hashFiles() 不支持 /tmp 绝对路径（只认 workspace 相对模式），修复后真实投递 issue#62 ✓ + 同周重跑幂等跳过 ✓；观察项：wild-* 三兽由并发 cron 绕过 register 直接入库导致无降世 issue，低语机制"无锚即缄默"正确兜底，但降世 issue 缺失本身是 register 流程纪律问题，留给后续轮次定夺）

## 已知 bug

- [x] issue body 里的 `/battle` 不触发 issue_comment 事件——✅ 2026-10-14 修复：battle.yml 增加 `issues: [opened]` 触发，job if 双事件分流，CMD_BODY/CHALLENGER 用 `comment.x || issue.x` 兜底统一取值；模拟种子改用 `github.event.id`（comment.id 在 issues 事件下为空，会导致 issues 入口的种子后缀恒空，属顺带修掉的隐性 bug）。本地断言+模拟脚本注入双事件变量独立执行通过
- [x] 降世 issue 正文漏 YAML 原文（issue#2 已手动修复正文；workflow 根因在清单第 1 项一并修）
- [x] schema 缺 `spirit_recovered_at` 字段——battle.yml 灵性惰性恢复机制（ad69861 实装）会向灵籍写入该字段，但 schema `additionalProperties: False` 未声明，导致任何带此字段的灵籍过不了校验 PR。✅ 2026-10-14 修复：schema 补录该字段（type: string, format: date），3 册真实灵籍本地校验全过

## 设计定案 v0.6（2026-10-14，主会话）

### PR 双轨制（施工项 4）

| 通道 | 来源 | 合并策略 |
|---|---|---|
| game/bot | github-actions[bot] 生成的 PR（battle-log 入账、chronicle 解说） | workflow 尾部 auto-merge，打标签 `game/bot` |
| player | 人类玩家 register/growth/battle 分支 | 校验通过只打标签 `player/待审` + 评论"校验通过，等待驯兽师长老过目"，**禁止自动合并** |
| meta | 任何人改 workflow/schema/README | CODEOWNERS 强制 leonezhu review，标签 `meta/规则` |

实现要点：
- register.yml 的 auto-merge 步骤加条件：`github.actor == 'leonezhu'` 的 PR 且走 register 流程 → 自动合；其他玩家 → 止步于"校验通过"
- 新建 CODEOWNERS：`*.yml` `*.json` `.github/` 全部 `@leonezhu`

### issue 标签体系（施工项 5）

| 标签 | 用途 |
|---|---|
| 降世 | 怪兽降世传记 issue（每兽一个，永久存在 = 怪兽主页/操作台） |
| 斗法 | 对战 issue（状态子标签：待战 / 已判 / 已收录） |
| 秘境 | 定时投放的世界事件 |
| 放生 | 放生申请与冷静期追踪 |
| 悖论 | 玩家上报异常（bug/疑似作弊），全服可见审计入口 |
| 杂谈 | 社区闲聊，可乱 |

实现要点：
- workflow 里 `gh label create` 幂等建标签（带颜色：降世绿/斗法红/秘境紫/放生灰/悖论橙/杂谈蓝）
- register.yml 开降世 issue 时打「降世」；battle.yml 贴战报时给 issue 打「斗法」+状态子标签
- README 指令表更新 issue 导航说明

## 打磨模式（2026-10-14 03:40+，清单全完成后全流程演练）
### 演练结果（全部通过）
- 5 个 workflow YAML 语法全过；3 册灵籍 schema + owner/路径一致性全过
- explore.yml 结算脚本从 workflow 原样提取执行：遭遇抽取/保底不为负/只动 spirit_stones+exp ✓；万次抽样分布与权重偏差 <15% ✓
- battle.yml hash 模拟原样提取执行：胜负/五行修正/境界碾压 override 逻辑 ✓；模拟本身不改灵籍 ✓
- register.yml 降世故事生成原样提取执行：多行 origin 完整入正文（清单1回归）✓
- catalog 3 册渲染字段齐备 ✓
- 线上 failure 记录 run#38440895133 已查明：Pages 未启用时的一次性引导失败（同分钟启用后 dispatch 重跑成功），非活性 bug

### ⚠️ 发现（记录不改设计）：入账链路静默丢账风险
- battle.yml/explore.yml 的入账步骤 `git push || true`、`gh pr create || true`、`gh pr merge || true` 全部吞错：若并发两次结算同兽（如斗法奖励与探索入账同时跑），push 被拒后评论故事已贴、灵石却没落库——玩家看到余额承诺与账本不符
- 建议（留主会话定夺）：入账 push 失败时改为「重试 rebase 后再推一次，仍失败则 edit 已贴评论声明"天道入账受阻，请评论 /explore 重试"」，把静默失败升级为可见失败
- ~~explore 每日限额靠 `git log --since="today 00:00"`（runner 本地时区）~~ → ✅ 2026-10-14 打磨轮实锤并修复：该 approxidate 语法实测返回空集（限额恒 0 = 每日 3 次永不触发），改按 committer 上海本地日期精确过滤（--date=format-local），真灵籍与注入边界样本（跨日/+负时区）验证通过
- [x] 斗法三态状态机断链（2026-10-14 打磨轮发现并修复）：①「斗法/已收录」终态无任何 workflow 会打——解说 PR 合并后 issue 永远停在「已判」；②结算时「斗法/待战」不摘除，已判 issue 会同时挂待战+已判两个矛盾标签（线上 issue#3 因旧 GH_TOKEN bug 标签全空，属历史遗留）。修复：battle.yml 新增 chronicle-seal job（pull_request closed 触发，分支名 battle/<issue>-* 或标题 issue#N 提取，chronicle/ 下同 issue 半场 ≥2 篇才打终态，幂等防重），结算步加 --remove-label 待战。本地用 issue#3 真实状态演练判定通过（2 篇半场 → 应判已收录）；待下一次真实解说 PR 合并做线上回归


### 2026-10-14 20:45 ｜ 斗法胜场解锁的记忆碎片不同步（打磨轮发现并修复）
- **现象**：skill 定案「memory_fragments.unlocked 计数与血脉之力共用（境界节点+胜场解锁）」，rebase.yml 渡劫链在段数上涨时会同步揭示封印段为【待补】占位，但 battle.yml 斗法入账只更新 bloodline，不同步 memory_fragments——斗法赢 2 场触发「🩸 血脉之力·苏醒」时，说好的记忆段仍是【封印】，且集齐 5 段的觉醒剧情经胜场路线永远无法触发。
- **修复**：battle.yml 血脉入账段补 memory_fragments 同步逻辑（与 rebase.yml 渡劫链一致：新解锁段揭示为【待补·第N段——斗法胜场中闪回的碎片】占位，旧灵籍无字段则动态补建默认结构）。本地沙盒从 workflow 原样提取执行，4 场景断言全过：胜1场不涨段不揭示/金丹+2胜涨段揭示第3段/旧灵籍动态补建/大乘封顶5段揭示第5段；败方字段不受污染。

## 异常登记

### 2026-10-14 ｜ growth 链路缺失（打磨轮发现并补齐）
- **现象**：DESIGN.md「每日喂养」行与玩家客户端 skill 均依赖 growth PR → workflow 校验（当日限额/灵石余额/append-only）→ bot commit 入账的完整链路，但 5 个 workflow 中没有任何一个处理 `growth/` 分支——玩家提 growth PR 会静默悬挂（无校验、无入账、无反馈）。
- **修复**：新增 `growth.yml`（设计已有、实现缺失，属打磨轮演练发现的真缺口）。校验：①产权过滤（只许改 `growth/<分支owner>/`）②append-only（旧内容必须是新内容前缀，一条 `- ` 追加行=一次修行事件）③当日限额（含 bot 已入账查重，增量幂等结算）④灵石余额（10灵石/次）。入账：bot commit（功力+5/次，灵石-10/次）→ game/bot PR 自动合并；growth PR 本体走双轨制。
- **演练中发现并当场修掉的 bug**：限额查重的 `git log -- <path>` 漏 `--all`——bot 入账走独立分支 PR，其 commit 不在 base..head 第一父链上，查重恒 0 → 每日限额永不触发。已加 `--all` 并以 fork 风格分支结构复测（8 项断言全过：合规/篡改/越产权/限额边界=3/超限/分支owner不匹配/灵石不足/幂等重跑）。
- ⚠️ 同类隐患排查提示：explore.yml 的限额查重挂在 issue_comment 直接触发（checkout 后 HEAD=main），`git log -- path` 能看到 main 上已合并的 bot commit，故不受此 bug 影响——但若未来 explore 改走分支 PR，需同步加 `--all`。

### 2026-10-14 05:41 ｜ commit 日期伪造（已实锤，影响高频轮窗口判断）
- **现象**：cb90d75（限额时区修复）的 author/committer 日期双双伪为 `2026-10-13T14:00:00Z`（+0800 整点 22:00:00，分秒全零=手工覆写指纹）；GitHub Actions run 实锚显示其真正落远端时间为 +0800 2026-10-14 04:43。前后相邻 commit（81ab00d、39cba34）日期均为真实值，仅此一个被污染。
- **排查**：仓库全部 yml/sh/md 无 `GIT_COMMITTER_DATE`/`GIT_AUTHOR_DATE` 引用，本机环境变量亦无——非脚本系统性污染，疑为生成该 commit 的当轮会话一次性行为。
- **影响**：铁律⑦的 `git log --since="40 minutes ago"` 会把该轮误判为无产出，下一轮可能对已完成项重复施工。
- **建议（留主会话定夺）**：① 排查 04:43 前后哪个进程带了 GIT_*_DATE 生成 commit；② 高频轮开工前的窗口判断改为以 `gh run list --createdAt`（远端实锚）作辅助校验，本地 git log 只作参考。

## 打磨模式 第二轮（2026-10-14 08:0x，实锚 gh run 07:10 后 51 分钟）
### 演练结果（5 工作流 + 3 灵籍 + 图鉴 + growth/battle/explore/register 结算脚本全过）
- 6 workflow YAML 语法 + 3 册灵籍 jsonschema 校验全过
- battle dry-run：hash 模拟原样提取执行 ✓；临时改 luling 至 jindan（高两境）→「境界碾压」override 正确生效，灵籍当场还原 ✓
- explore 结算：幂等（同种子结果一致）✓；beast_lose 保底不为负 ✓；五维产权不动 ✓；5000 次抽样分布与权重偏差 <2% ✓；图鉴 3 册渲染+暗色风断言 ✓；register 多行 origin 全文入 issue 正文回归 ✓；growth 入账（灵石25-20=5/功力+10/五维不动）✓
### 🐛 本轮实锤并修复：explore.yml 败遭遇灵石「负账记正」
- **现象**：保底分支 `stones = old_stones - new` 把实际损失记成了正数——灵石 100 恶战丢 10，评论区与 commit message 都显示「灵石 +10 入账」，败遭遇叙事（被叼走灵石）与账本自相矛盾，且凭空发钱
- **修复**：改 `stones = new - old_stones`（负号保留，-5 实亏记 -5）；顺带修 STONES 展示 `>=0` → `>0`（0 灵石变动不再显示 "+0"）
- **回归**：保底样本（灵石5→0 入账-5）、足额样本（100→90 入账-10）、胜遭遇不变、展示格式 4/4 断言全过

### 2026-10-14 09:1x 高频轮：labels.yml PR files 检测崩溃（线上实锤）+ 并发施工踩踏警示
- 现象 1（已修）：labels.yml 的 label job 用 `git diff $BASE $HEAD` 检测规则层变更，浅克隆拿不到 base sha，报 `fatal: bad object 35b9459`，job exit 128（线上 pull_request 实锤）。改为 `gh pr view --json files` 取变更文件列表，不再依赖本地 git 对象，顺带省掉一次 checkout。本地对真实 PR#8 文件列表断言 meta 检测正确。
- 现象 2（过程记录）：本轮与另一并发轮次（e3a960d 至 PR#9，修 chronicle-seal 缺 checkout）在同一工作目录施工，发生 checkout 切分支、工作树覆盖、unresolved 冲突短暂共存的踩踏；本轮修复改在独立 git worktree 完成。建议：高频轮开工前先 `git worktree add` 隔离操作，收尾 worktree remove，主 clone 目录只留给入账/主会话。
- 线上正面回归：issue#6 全链路已走通——6732a9b 修复后的斗法 run success、战报单贴、battle-log/6 分支生成、双方半场 PR(#7/#8) 合并、chronicle-seal（e3a960d 修复后）成功打上「斗法/已收录」终态加封卷评论；并发轮 d37b603 已把滞留侧分支的入账补录对齐。

## 2026-10-14 21:4x 夜间轮：真红灯实锤并修复——斗法重赛守卫 exit 1 假故障（PR#41）

### 线上巡检发现（判定标准「重跑后仍 failure」首次抓到真目标）
- issue#37 run 38511165509（04:23:50Z）battle 斗法 failure。上下文：run#47 已正常结算 success 并打「斗法/已判」，~7 秒后 run#48 到达——**`/battle` 双触发**（issue body 与补充评论均含 `/battle`，正是玩家 skill「已知坑」两步触发法的直接后果），run#48 进入 replay-guard，正确贴出拒战评论后 `exit 1` → run 标红，重跑仍 failure（守卫每次都会撞上）
- 守卫行为正确（拒战评论已贴、账本无损），但把「重复指令」上报为故障：每次双触发必产红灯，污染真故障判定

### 修复（14faca2，PR#41 已合并）
- battle.yml replay-guard 分支 `exit 1` → `exit 0`（附注释：守卫已履职，非故障）
- YAML 语法 + `on` 字面键校验过；未触碰 PyYAML 整文件回写

### 顺带观察
- 04:24/04:25 battle-log/37、battle-log/39 两批各带 4 条 startup failure，与 12:2x 登记的平台噪音模式一致（主 run 全 success），非活性 bug
- 本轮红灯为线上巡检（「重跑后仍 failure」）抓到的**第一个真目标**——该判定标准有效，后续巡检节奏保持

## 2026-10-14 23:0x 夜间轮：打磨第八轮——斗法分镜血条错位（实锤并修复）

### 背景
- 窗口内主会话落了灵性+天赋系统（ad69861）与素材包模式（655c857）两大块新代码，本轮按⑧打磨模式对新逻辑做演练

### 🐛 实锤并修复：分镜血条渲染按 attacker 翻转 hp_a/hp_b（54967d9，已推送 main）
- **现象**（原样提取渲染段沙盒执行当场抓出）：R1 碰巧对齐，R2/R3（守方出手回合）血条左右颠倒——R1 燧鸣打鲁灵后血条却显示「燧鸣 100／鲁灵 10」，R2 显示「燧鸣 10.0／鲁灵 95.0」（应为 95/10），R3 鲁灵血条凭空从 10 回到 95 再归零——读者视角=鲁灵一击把燧鸣打到 10 血后燧鸣莫名回血翻盘，血条与胜负自相矛盾
- **根因**：sim 里 `hp_a/hp_b` 恒为挑战方/守方累计血量，与该回合谁出手无关；渲染段却写 `ha = f['hp_a'] if f['attacker'] == C else f['hp_b']` 按当回合 attacker 翻转
- **修复**：`ha = f['hp_a']`、`hb = f['hp_b']` 直接取用，附注释防回归
- **回归**：正序（leonezhu 挑战，R2 守方出手）+ 反序（鲁灵挑战，R1/R3 守方侧出手，含 drain 吸血天赋事件）两场景血条对齐断言全 PASS；battle.yml YAML 语法 + `on:` 字面键原文校验过
- **断言方法教训**：渲染行血条正则此前只断言「含数字」，未断言「与 frames.hp_* 精确相等」——成对字段修复的教训（13:0x 轮）在血条上重演，本轮断言直接对齐 sim 输出

### 顺带登记（记录不改设计）
- sim 段 TALENT_TXT/round_sim/rl/pa-pb 均为死代码（天赋文本实际由渲染段独立生成，round_sim 定义后从未调用）——不影响正确性，留主会话清理
- 渲染段含反引号的 f-string（`\\`battle/...\\``）产生 SyntaxWarning（invalid escape sequence '\\`'），Python 3.12 起为可见警告，建议改用单反引号原文——本轮未动，属 cosmetic
- 本次 push 与 bb04d5b（主会话世界观 v1）并发，worktree rebase 后再推——「演练基线可能过期」再次应验

## 卡住登记

（暂无）

## 2026-10-14 白天游玩轮（主会话）发现并修复

- [x] battle.yml 两处 jq 表达式引号嵌套错误（外层双引号包转义逗号→jq 解析失败，label 步崩，issue#6 实锤）→ 改单引号包裹（6732a9b）
- [x] chronicle-seal 缺 checkout 步骤——裸 runner 上 git ls-tree 报 fatal，HALF 恒 0，「已收录」终态永不打 → 补 checkout step（e3a960d），回归通过（issue#6 已打终态+贴封卷评论）
- [x] **根因级：bot 无 create PR 权限**——GITHUB_TOKEN default_workflow_permissions=read，gh pr create 报 "GitHub Actions is not permitted to create or approve pull requests"，入账 commit 全部滞留侧分支、main 账本永不清账（`|| true` 静默吞错）。已改仓库 Actions 权限 write+approve_pr，并补录：issue#2 秘境×2 + issue#6 斗法胜 + issue#3 墨霄入账（PR#10 合并），燧鸣账户 175 灵石/115 功力对齐
- **教训**：`|| true` 吞错是账务系统大忌——静默失败比崩溃更危险，账本类步骤失败必须显式报错

## 2026-10-14 10:0x 高频轮：lore-reward 三连修 + reward 链路首次真通（PR#17~#24 端到端）

### 结论
- **reward 链路首次端到端打通**：PR#22《雾隐栈道》合并 → bot 入账 commit 7219781（著史奖励+20灵石）→ lore-reward/22 → PR#23 自动合并 → 燧鸣 175→195 灵石。此前该 workflow 从未 success 过（PR#13/#14/#15 三连 skipped）。

### 实锤并修复的三个 bug（按时间序）
1. **heredoc 缩进塌陷**（run 38498057843）：`python3 - <<EOF` 的正文带 4 空格缩进，Python 解析报错后被 bash 当普通命令继续读，`EOF` 永远闭合不上→`syntax error: unexpected end of file`，步骤必崩。→ 改 `python3 -c`
2. **浅克隆 git diff 拿不到 base sha**（同 run，`fatal: bad object fb1c345`）：labels.yml 同款坑在 lore-reward 复发。→ 改 `gh pr view --json files` 取变更文件
3. **PyYAML round-trip 把 `on:` 写成 `true:`**（e176bc5 与 2cf3bcc 双双中招，后者是本轮用 safe_dump 整文件回写引入的，自纠于 PR#21）：裸键 `on` 被 PyYAML 解析为布尔 True，dump 回去变成 `true:`，workflow 触发器整体失效（run 名退化为文件路径，如 `.github/workflows/lore-reward.yml failure`）。→ 手工还原 `on:`，文件内已加警告注释：**严禁对此文件做 PyYAML 整文件回写**

### 过程教训
- 本轮前半段曾误判 e176bc5（并发会话产物）为 root cause——实际第一次 `true:` 病灶是自己 patch 引入的。教训：**用 PyYAML 改 workflow 必须只改 run 字符串，绝不能 load→dump 整文件**；怀疑别人之前先 diff 自己的工作树。
- 02:02 那批 4 个 failure run（jobs 为空、log 404、GitHub 提示 workflow file issue）经空 commit 探针（PR#24）证实为**瞬态启动失败**，当前 workflow 全部健康，无需处理；「连并窗口内 startup failure」值得留意，勿误诊为文件 bug。

### 遗留
- lore-reward 的入账 push/PR create/merge 仍带 `|| true` 吞错——「入账链路静默丢账」总登记项（见打磨模式第一节）在本链路同样存在，待主会话定夺统一方案
- 夜泉洗尘（PR#17）、石语（并发轮 PR#19）、雾隐栈道（PR#22）三篇测试遭遇已随链路验证留在 lore/encounters/，如嫌测试数据可另行清理（不属本轮职责）

## 打磨模式 第三轮（2026-10-14 10:4x 高频轮，worktree 隔离演练）
### 演练结果（全过，无新代码 bug）
- 8 workflow YAML 语法 + 3 册灵籍/7 篇遭遇 schema 全过；线上 run 无新增 failure（唯一红=已登记的 02:02 瞬态启动失败）
- battle hash 模拟（原样提取执行）：种子确定/模拟不改灵籍/境界碾压 override 全过 ✓
- explore 结算：只动 spirit_stones+exp、幂等、败遭遇保底（5→0 记 -5 负账）全过 ✓
- register 降世故事：3 行多行 origin 全文入正文（清单 1 回归）✓
- catalog 渲染：3 册齐/暗色/境界/五行着色/余额全过 ✓
- growth 校验（sha 语义复现真实 PR 入参）：合规 delta=1/篡改拒/超限拒(4>3)/余额不足拒(5<10) 全过 ✓
### 演练方法教训（非代码 bug）
- 提取 workflow heredoc 演练时，HEAD 入参必须传 commit sha（真实 PR 触发传 head.sha）——误传分支名时 `git diff <base> <分支名>` 因分支名与目录同名解析成路径报 128，而 `sh()` 不查 returncode 静默拿空 diff，得出「合规场景也跳过」的假阴性。顺带确认：真实触发路径不受此影响（sha 永远无歧义）
### 🐛 发现（bug 级，登记待修）：入账链 `|| true` 连锁吞错使 bot PR 创建失败完全不可见
- battle/explore/growth 三处入账步骤同构：`git push || true` → `gh pr create ... || true` → `gh pr merge ... || true`。若 pr create 失败（权限/网络/分支已存在），merge 必失败也被吞——结算故事已贴、灵石未落库、workflow 显示 success，零痕迹。白天「bot 无 create PR 权限」事故（issue#2/#6/#3 补录）即此模式的真实爆发
- 与「入账链路静默丢账」总登记项同源但更具体：**pr create 是链路咽喉**，其失败必须显式报错（去掉 create 上的 `|| true` 即可让 step 红灯），push/merge 失败也会随之可见
- ✅ 2026-10-14 高频轮已按建议修复（见下「入账链去吞错」节）

## 2026-10-14 11:xx 高频轮：入账链去吞错（`|| true` 连锁吞错修复）

### 改动（4 文件）
- battle.yml / explore.yml / growth.yml 三处入账链：`git commit` / `git push` / `gh pr create` / `gh pr merge` 全部去 `|| true`——push/create/merge 任一失败即 step 红灯，静默丢账升格为可见失败；仅保留 `gh pr edit --add-label` 上的 `|| true`（标签失败无账务影响）
- lore-reward.yml：奖励入账链同改（push 已无吞错，pr create/merge 去吞错）；「著史者名录」步 `git push origin main || gh pr create ... || true` 三连环拆开——push 显式报错、pr create 单列；run 块由折叠标量整文件重写为块标量（转义地狱根治），奖励步 python 压单行（块内顶格行会终止块标量，勿写多行 python）

### 校验
- 8 workflow YAML 全过；触发器 4 改动文件 `on` 键完好（未触碰 PyYAML 回写）
- 4 个改动文件全部 run 块提取 `bash -n` 语法全过
- lore-reward python 单行 compile 校验通过
- 咽喉断言：4 文件 push/create/merge/commit 行无 `|| true` 残留

### 遗留
- 修复后入账失败会体现为 workflow 红灯（正是目的），但尚无「失败后 edit 已贴评论告知玩家重试」的补偿动作——本次只做可见化，补偿留主会话定夺
- 下一轮观察点：一次真实 explore/battle 触发验证新入账链线上跑通（去吞错后的正确路径与此前行为一致，理论上零行为变化）

## 打磨模式 第四轮（2026-10-14 11:4x 高频轮，worktree 隔离演练）
### 演练结果
- 9 workflow YAML 语法 + 触发器 `on` 键完好 + 3 册灵籍/7 篇遭遇 schema 全过
- battle dry-run（原样提取执行）：种子确定性/模拟不改灵籍/境界碾压 override（lianqi 临时提 jindan→碾压生效→当场还原）✓
- explore 结算：种子确定性/五维产权不动/保底负账等价式 ✓
- growth 校验 sha 语义（临时仓 8 场景）：合规 delta=2/篡改拒/前插行拒/越产权拒/超限拒(4>3)/余额不足拒(5<10) 全过 ✓
- register：降世故事 python yaml 解析在位、无 awk 残留（清单 1 回归）✓
- catalog：3 册渲染齐（炼气期/灵石/暗色），REALM_CN 映射与 schema realm 枚举 7/7 一致 ✓
- 入账链咽喉断言：battle/explore/growth/lore-reward 四文件 push/create/merge 无 `|| true` 残留 ✓

### 🐛 本轮实锤并修复：rebase.yml（并发轮新增）入账链 merge 吞错漏网
- **现象**：并发轮新增的进化 workflow 入账链 `gh pr merge "$BRANCH" --merge || true`——push/create 已红灯可见，但 merge 失败被吞：账滞留侧分支、main 未清账、step 仍 success，动画照贴（「余额 X」承诺与账本不符）。与上轮四链路去吞错标准不一致，属同构修复漏网
- **修复**：去掉 `|| true`（PR#27 → 合并 bbe37f2，本地 YAML + 触发器校验过）

### 发现（记录不改设计，留主会话定夺）
- rebase.yml job if **硬编码单兽**：`issue.title == '📜 降世 · 燧鸣（火）'` 且灵籍路径写死 `monsters/leonezhu/beast.yaml`——当前只有燧鸣一只可进化，其他兽评 `/rebase` 会被静默跳过（无任何反馈评论）。建议改为「评论者自己的降世 issue + 评论者灵籍」通用路由，并对不满足条件的评论给一句拒绝回应
- rebase.yml 顶部定义了 `REGEX` env 但从未使用（死配置）；触发判定实际用 `startsWith(comment.body, '/rebase')`，`/rebase 加参数`（如 `/rebase force`）也会通过——建议二选一清理
- rebase.yml 渡劫动画步 `sleep 2` 后 merge：PR create 到 merge 间无合并就绪等待，若 runner 慢可能偶发 merge 404（当前被 `|| true` 掩盖，去吞错后可能暴露为红灯）——观察点

### 演练方法教训
- 并发施工窗口：开工 `git pull` 后 5 分钟内远端又进新 commit（rebase.yml），本轮演练以 pull 后 HEAD 为准做了一次、修复时重新对齐远端——worktree 隔离 + 收尾 `git pull --ff-only` 复核可兜住，但「演练基线可能过期」应成为高频轮默认假设

## 2026-10-14 12:2x 高频轮：bot 入账 PR 四链 startup failure 实锤（重跑可洗绿，修复无效已回滚，待主会话定夺）

### 现象（确定性复现，非瞬态）
- **每一个** github-actions[bot] 创建的入账 PR（rebase-log/2、explore-log/*×2、lore-reward/22、battle-log/31、battle-log/35）上，挂 `pull_request: [opened/synchronize]` 的 4 个 workflow（register/growth/labels/lore）必然 startup failure：0 job、0 check-run、页面提示 "This run likely failed because of a workflow file issue"，run 挂在 PR 的 head sha 上
- 只挂 `pull_request: [closed]` 的 battle/lore-reward 在同一批 PR 上零失败；人类分支的 PR 全天零失败；同 sha 的 main push 全 success
- 每次真实入账（rebase/battle/explore）都会同步产生 4 条红灯噪音

### 实锤「非文件 bug」的过程
- 重跑任一 failure run → job 正常求值、正常 skip（本轮已把 14 个历史 failure 全部重跑洗绿：explore×8、battle-log/31×4、rebase-log/2×1、lore-reward/22×1、battle-log/35×4）
- 失败只发生在 PR create→merge 的 ~2 秒高速窗口内排队的 run；merge ref 计算期分支状态被并入/清理打断，疑为平台启动层竞态（未拿到 GitHub 官方文档佐证，标注为推测）

### 修复尝试（无效，已完整回滚，防重蹈）
- 第一版在 4 个 workflow 的 pull_request 触发器加 `branches-ignore: [battle-log/**, explore-log/**, ...]`——提交前自查 GitHub 官方文档发现两个致命伤：① `branches`/`branches-ignore` 过滤的是 PR 的 **base** 分支（所有入账 PR 的 base 都是 main，根本拦不住），head 分支只能在 job `if` 里用 `github.head_ref` 过滤（on 层做不到）；② 同一事件**禁止**同时用 `branches` + `branches-ignore`（4 个文件都定义了 `branches: [main]`），硬上会让 workflow 解析失败、连 issue_comment/push 等其他触发器一起报废
- 补丁在 worktree 内做出、未 commit，验证思路失败后 checkout 还原、worktree remove，主仓零污染

### 建议（留主会话定夺，二选一）
1. **job if 过滤 head 分支**：4 个 workflow 的 job `if` 加 `&& !startsWith(github.head_ref, 'battle-log/')` 等 5 个 bot 分支前缀（lore.yml 已有 head_ref 条件可顺带扩展）——job 层求值在 startup 之后，能挡住吗未经验证：startup failure 发生在 job 求值之前的话此路同样不通，需先做一次实验性 commit 验证
2. **容忍噪音**：startup failure 本身无账务影响（入账链自己的 run 全 success），把「入账 PR 附带 4 条红灯」当作已知噪音接受，发现真 failure 时以「重跑后仍 failure」为判定标准
- 另一个未验证的旁路：入账链改用 `gh pr create --fill` 前先给 PR 打 draft 或先用 API 预建 check 豁免——均属设计层改动，本轮不动
## 2026-10-14 12:5x 高频轮：打磨第五轮——斗法分镜守方境界英文漏翻（实锤并修复）

### 演练结果（全过，含一项新修复）
- 9 workflow YAML 语法 + 触发器 `on` 键完好 + 3 册灵籍 schema 全过；入账链咽喉断言（push/create/merge 无 `|| true` 残留）✓
- explore 结算原样提取执行（8 项断言）：结算执行/灵石与结算一致/保底不为负/败遭遇负账记负/胜遭遇非负/幂等/2 万次抽样权重偏差 3.1%/保底等价式(5→0记-5) 全过 ✓
- battle hash 模拟：种子确定性/模拟不改灵籍/分镜三回合/attribution 对齐（12:27 修复回归）/境界碾压 override 全过 ✓
- growth 校验语义（临时仓复现）：产权过滤/append-only 真前缀/追加行计量(1与2)/篡改拒/超限拒(2+3>3)/限内通过(2+1=3)/余额计算 全过 ✓
- register yaml 解析在位、多行 origin 完整、catalog 3 册齐 + REALM_CN 7/7 枚举覆盖 ✓

### 🐛 本轮实锤并修复：守方境界英文漏翻
- **现象**：分镜渲染第 3 行守方显示 `墨霄（水·lianqi）`——12:27 的 4e8f349「境界中文显示」只给挑战者侧 a['realm'] 加了 `REALM_CN.get` 映射，守方 b['realm'] 漏网，渲染断言「双方境界中文」当场抓出
- **修复**：65ff060，守方同过 `REALM_CN.get(b['realm'], b['realm'])`；本地渲染回归输出 `燧鸣（火·筑基） ⚡ vs ⚡ 墨霄（水·炼气）`；线上 push run success
- **教训**：成对字段的修复必须两侧同改——上轮只断言了「含中文」，未断言「无英文残留」，本轮断言加严后立即抓出

### 线上观察
- 04:24-04:25Z battle-log/37 与 battle-log/39 两批入账 PR 又各带 4 条 startup failure（与 12:2x 登记的平台噪音模式完全一致，非活性 bug，判定标准仍是「重跑后仍 failure」）

## 2026-10-14 13:0x 高频轮：打磨第六轮——rebase/lore/labels 三链首演（全过，零修复）

### 演练结果（前五轮未覆盖的三条链，本轮补齐）
- 全 9 workflow YAML 语法 + `on` 字面键复验 ✓
- **rebase.yml 渡劫校验**（原样提取，沙盒灵籍 6 场景）：功力不足拒/灵石不足拒/渡劫成功（zhuji→jindan、扣50、功力保留）/天梯之顶拒/非法境界拒/渡劫后再触发按金丹门槛(600/400)再拒 ✓；真实仓库灵籍全程未动 ✓
- **lore.yml 第1步变更范围**（临时 git 仓）：篡改已收录 star-fragments.yaml 抓出/越界改 .github/workflows 抓出/新增合规遭遇放行 ✓
- **lore.yml 第2步 schema+署名+禁术语**（临时 git 仓 + 真实 lore.schema.json）：冒名 contributor 抓出/故事含 PR·merge 术语抓出/weight=999 超 schema 上限抓出/合规投稿打勾 ✓
- labels.yml / lore-reward.yml 为纯 shell（无 python 段），逻辑已在上轮 `|| true` 咽喉断言覆盖，本轮目审复核：labels.yml 两条触发器分流正确（PR→meta 标签，push→幂等建标签）；lore-reward.yml 灵石奖励与名录两步入账链均无吞错 ✓

### 结论
- 清单三项之后的全部 9 条 workflow 链已逐一演练过至少一次，无新 bug。清单全清 + 六轮打磨零遗漏项，高频轮后续默认 SILENT，除非线上出现「重跑后仍 failure」的真红灯
- 本轮教训（工具层，非仓库 bug）：YAML 块标量提取的 python 段做 dry-run 时，`textwrap.dedent` 处理不了「首行顶格+后续行带共同前缀缩进」的混合形态（GitHub Actions run 块常态），需按非空行共同前缀手动剥除）

## 2026-10-14 22:0x 夜间轮：打磨第七轮（全流程演练全过，零修复）

### 线上巡检
- battle-log/39 四条 failure（04:25:53Z）重跑全部洗绿（completed skipped）——确认为已登记的「bot 入账 PR 附带 startup failure」平台噪音，非真红灯。「重跑后仍 failure」判定标准连续第三轮有效，当前线上零真红灯

### 演练结果（只读沙盒，真实灵籍未动，收尾工作树 CLEAN）
- 9 workflow YAML 语法 + `on` 字面键 + 3 册灵籍/7 篇遭遇 schema 全过
- battle hash 模拟（原样提取执行）：种子确定性/幂等/三回合分镜/模拟不改灵籍 全过
- explore 结算（原样提取执行）：种子确定性/五维产权不动/恶战保底（5→0 记 -5、100→90 记 -10）全过
- growth 校验语义（临时仓 8 场景）：合规 delta=1/3、篡改拒、越产权拒、超限 4>3 拒、余额 5<30 拒、新文件过 全过
- register 降世故事：3 行多行 origin + mystery 完整入正文（清单 1 回归）全过
- rebase 渡劫校验（沙盒 6 场景）：功力不足拒/灵石不足拒/渡劫成功（扣 50/境界+1）/天梯之顶拒/非法境界拒/筑基新门槛再拒 全过
- catalog 渲染字段断言 + REALM_CN 在位 全过

### 演练方法教训（非代码 bug，给后续轮提效）
- heredoc 提取段的「首行顶格+后续行缩进」混合形态：commonprefix 只按非空行算会漏剥首行——先按非空行求前缀，再逐行剥除（textwrap.dedent 不够用）
- 沙盒替换 workflow 注入占位符必须全量（steps.outputs 类占位符漏一个，seed 就变，遭遇选择假阴性）——本轮 explore 断言 FAIL 一次全是此因，非代码 bug
- 演练判定 refuse 与否要认准 `::error::` 走 stdout（print），stderr 里只有 gh 兜底评论的报错
- growth 演练的「余额不足拒」若在 PR 内改灵籍会被产权过滤器先拒——穷要穷在 base 上，PR 只追加修行行

## 2026-10-14 深夜轮：好玩路线图 T1-1「血脉之力」施工（v0.8）+ 斗法双触发竞态实锤修复

### 机制（硬边界先行）
- schema 新增 `bloodline{unlocked 0-5, wins>=0}`，bot 独占（schema 8 场景校验全过，旧灵籍无此字段向后兼容）
- 解锁公式：`unlocked = min(5, 境界段数(炼气0/筑基1/金丹2/元婴3/化神4/渡劫5/渡劫后5) + wins//2)`——境界节点与胜场双触发，正是路线图"想起自己是谁↔战力成长绑死"的本意
- 加成：每段 +1.5% 战力（上限 +7.5%，与灵性 ±5~10% 同量级不破平衡）；battle.yml `power()` 单测比值精确 1.07500，对局实测 320.1/297.7=×1.075，等弱对手 +7.5% 成功反超
- 双入账链：battle.yml（胜场累计+段数重算+解锁贴「🩸血脉之力·苏醒」）/ rebase.yml（渡劫后境界段数上涨→独立入账 PR，段数无变化跳过不空入账）——本地沙盒 4+3 场景全过
- e2e 四场实跑（issue #49/#51/#53/#55/#57）：燧鸣 1段→2段→胜场解锁链全通，PR50/52/58 账目正确；期间顺带实锤并修复三处 bug

### 🐛 本轮实锤修复
1. **入账段缺 `import json`**（本轮新代码引入）：沙盒执行当场 NameError，修于 push 前
2. **斗法双触发竞态**（现存 bug，非本轮引入）：issue body 与评论 1 秒内各起一个 run，同名 `battle-log/<n>` push 撞车红灯（#49/#51 两度复现）
   - 守卫 v1（待战标签，af02c81）：#53 实测标签时序不可靠，双 run 都在彼此打标前读到空
   - 守卫 v2（远端分支互斥锁，c5a0a1e）：#55 实测锁检查有 TOCTOU 窗口（守卫窗口 14s 早于对侧 push 26s），无法前移消除
   - 守卫 v3 终案（2cd156c）：push rejected 即互斥锁最后裁决——迟到者良性 exit 0（其重复结算弃用），真 push 故障仍显式红灯；#57 终验双 run 双绿、入账 PR 唯一
3. skill 已知坑修正：`/battle` 发 issue body 实际可触发（workflow 本就监听 issues.opened），原手册"必须补评论"表述过时

### 教训
- GitHub Actions 无原子锁可用时，「最终写入裁决」（push/创建冲突即退让）比「前置检查」可靠——前置检查的窗口永远存在
- heredoc 无引号 EOF 段内加代码，import 清单要重看一眼（本轮 json 就是漏网之鱼）
- e2e 不能只验 happy path：本场五连测里 4 场是靠"故意双触发"把竞态逼出来的

## 2026-10-14 19:4x 夜间轮：打磨第九轮——T2-1 记忆碎片 + T1-3 斗法志回放（窗口内新代码全演练，零修复）

### 背景
- 窗口内主会话落两大块：0537d17（T2-1 记忆碎片：schema+rebase.yml 同步揭示+觉醒判定）与 cc61dcd（T1-3 斗法志回放页）。按⑧对新逻辑演练，worktree 隔离。

### 演练结果（全过，零新 bug）
- **T2-1 碎片同步**（rebase.yml 结算段原样提取，沙盒 4 场景）：
  - wins=2 渡劫后（zhuji，new=2）：第 2 段揭示为【待补·第2段…】、第 3 段仍【封印】、bloodline/mf 计数一致、schema 过 ✓
  - **旧灵籍无 memory_fragments 字段**（向后兼容）：自动生成五段册、已揭示段计入、schema 过 ✓
  - 集齐 5 段（dujie）：5 段全揭示零封印残留、AWAKEN 判定触发 ✓
  - 无变化：NONE 跳过不空入账 ✓
- **3 册真实灵籍**：schema 全过（含新 memory_fragments additionalProperties:false）；bloodline.unlocked 与 mf.unlocked 交叉一致（1/0/0）、封印数 4/5/5 ✓
- **T1-3 回放链**：catalog.yml python 段原样提取 compile 过；build-chronicle-index.py 实跑 8 场、file 路径全真实存在、实跑后工作树 CLEAN（生成器幂等）✓；battle-chronicle.html 与 chronicle-index.json 字段契约断言通过（html 引用的 item 字段 ⊆ 索引字段）✓；catalog.yml 段内无 chronicle 引用——斗法志页与图鉴页数据链独立，回放页索引由 bot 在斗法入账后跑生成器刷新，链路成立 ✓

### 过程教训（复训）
- worktree 开工即撞主会话并发 push（pull 后 HEAD 从 0537d17 跳 cc61dcd）——「演练基线可能过期」第 N 次应验，worktree + 收尾 fetch --ff-only 复核有效
- GitHub Actions run 块 python 段提取：`\nPYEOF` 全文首查会命中后续 heredoc，必须按行号配对扫描（start 行下一个顶格 PYEOF）
- 本地实跑 build-chronicle-index.py 属安全幂等（输出与已提交版本逐字节一致，git status CLEAN 验证）——对生成器类脚本，实跑+CLEAN 断言是最强校验

## 2026-10-14 20:0x 夜间轮：好玩路线图 T1-2「天赋技能扩展」施工（v0.10）

### 交付
- **schema 硬边界先行**（beast.schema.json）：talent.kind 扩为 6 类（+control/summon）；新增 talent.mastery（0-999，bot 独占写入，禁玩家 PR 改），旧灵籍无字段兼容（.get 默认 0）
- **觉醒四级**（battle.yml AWAKEN 表）：mastery 0-2/3-7/8-14/15+ → Lv0-3；触发率 30/35/40/45%；burst 1.6→1.9x、shield 减伤 0.5→0.3、drain 吸血 0.4→0.55、counter 反弹 0.5→0.7 随级强化
- **control 封招**：命中则对方该回合力度减半（伤害结算前生效，攻守两侧皆有语义）
- **summon 残影协战**：攻方命中 +25 固定追伤（守方无语义不触发）
- **熟练度入账**：battle.yml 结算段每触发 +1（胜负无关），觉醒瞬间在 issue 贴「✨ 天赋 · 觉醒」播报（只升贴一次不刷屏）
- **本地沙盒演练全过**：sim 段原样提取真跑（control/summon 触发断言、mastery 计数一致断言、旧籍无 mastery 兼容断言、schema 3 真实灵籍+2 新 kind 样本+非法 kind 反例全过、旧 4 类 Lv0 回归=数值与 v0.8 语义一致）
- **e2e 实测**（issue#59 燧鸣 vs 墨霄）：battle run success，燧鸣 R1 burst 触发 ✨、mastery=1 入账（commit d19b2ee）、墨霄 shield 未触发 mastery 正确保 0、灵性结算正常

### 顺带修正的隐性 bug（施工中实锤）
1. **守方侧无语义 kind 空触发**：v0.8 起 trig_def 对 burst/drain 兽命中时事件为 None 但不报错（无感知）；mastery 要入账后计数与画面不符（实测 3 vs 1）。修正=触发判定绑定语义侧：burst/drain/summon 仅攻方判定、shield/counter 仅守方判定、control 双侧——**触发必须可见于画面**
2. **talent 事件单槽互相覆盖**：一回合攻守双方天赋都触发时旧代码单变量覆盖丢事件；改攻守双事件槽（talent/talent_def），bot 分镜行可同时显示两侧 ✨

### 观察项（非本轮引入，未修）
- growth/labels/register/lore 四 workflow 在 bot 建的 battle-log PR 上 100% failure（近 100 次 0 成功，"workflow file issue" + 0 jobs，入账 PR 均已正常合并不受影响）——疑似 GitHub 对 bot PR 递归触发的抑制，留待专轮排查

### 过程教训
- workflow 内嵌 python 改动，沙盒提取时 `${{ steps.parse.outputs.* }}` 表达式必须一并替换（漏一个就 FileNotFoundError）
- 单事件槽变量在「一回合双触发」场景是隐性地雷：新机制要入账时，先画清"一回合最多几个事件、各归谁"
- e2e 后本地 diff 突然 clean = 并发 cron 刚提交——收尾 commit 前必须 git log 复核工作树归属，确认并发提交没夹带自己文件

## 2026-10-14 20:1x 夜间轮：bot-PR startup failure 独立复核（零修复，两条新证据）

### 巡检
- 线上全部 30 条 failure 复盘完毕：**全部**是已登记的 bot 入账 PR 四链 startup failure（7 批：battle-log/43~59 + 更早 explore-log/lore-reward/rebase-log），无新真红灯；PR#60 批次（#59 斗法 e2e）4 条重跑全部洗绿（completed skipped）。GitHub status 全程 operational，排除平台故障窗口
- 结论与 12:2x 登记一致，**建议①（job if 过滤 head 分支）可以不用再实验**：见下证据 1

### 新证据（本轮 API 实查所得）
1. **失败仅绑定 create→merge 高速窗口，且可事后求值**：对 PR#60 已合并后的 head sha 重跑，4 个 run 全部正常进入 job 求值并 skip（0 失败）——说明 startup 层只在 PR 存活的 ~2 秒窗口内排队时被打断；重跑（无论 actor 是谁）都能正常走完。12:2x 留验的「job if 能否挡住」不再需要验证：正确姿势就是**合并后批量重跑洗绿**或接受噪音
2. **僵尸 check-suite 隐患**：被污染的 head sha（如 d19b2ee）上残留 5 个永久 `status=queued` 的 check-suite（重跑后新 suite 正常完成，旧 suite 永不结算）——该 sha 的 combined commit status 因此永远 `pending`。当前无 branch protection 无影响；**未来若开 required status checks，这些僵尸会把历史 sha 永久卡在 pending**，届时需 API 手动补创建 check-run 或放弃对 bot 分支 sha 的检查

### 处置
- 维持 12:2x 的方案②（容忍噪音 + 「重跑后仍 failure」为真红灯判定标准），本轮未改任何 workflow 文件
