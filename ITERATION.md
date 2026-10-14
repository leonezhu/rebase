# 迭代日志（ITERATION）

> 夜间 cron 每轮迭代在此记录。设计定案由主会话写入，施工项完成后打勾。

## 施工清单（cron 按序取项，每轮一项）

- [x] 1. 修 register.yml 的 YAML 解析 bug：awk 提取 origin 对多行不健壮 → 改 python yaml 库解析；顺带修复降世 issue 正文漏 YAML 原文问题（根因同一个）✅ 2026-10-14（origin/mystery 全文入正文，GITHUB_ENV heredoc 传变量，本地对真实灵籍演练断言通过）
- [x] 2. explore.yml 秘境探索 workflow：issue 评论 `/explore` 触发 → hash 定遭遇表 → bot 贴事件故事 → 灵石/经验入账 bot commit ✅ 2026-10-14（8 种遭遇加权随机，种子=评论者+评论id+当日次数可复现不可操控；每兽每日限 3 次按 bot commit 记录查重；败遭遇灵石保底不为负；本地演练权重分布+保底+语法断言全过）
- [x] 3. catalog.yml + Pages 图鉴：main push 时扫描 monsters/*.yaml 生成玄幻暗色静态 HTML → GitHub Pages ✅ 2026-10-14（3 册灵籍本地渲染断言通过；Pages 已于同日用 API 启用 build_type=workflow，首次部署成功，线上 https://leonezhu.github.io/rebase/ 已含 3 册灵籍）
- [x] 4. PR 双轨制（v0.6 设计定案，见下）✅ 2026-10-14（register.yml 双轨分流：主人=自动合并/其他玩家=止步 player/待审 禁止自动合并；降世 issue 统一移到 merged 后开（双通道通用+幂等防重+打「降世」标签）；新增 labels.yml=meta/规则 自动打标；CODEOWNERS=* @leonezhu；battle/explore 的 bot PR 打 game/bot；9 个游戏标签已用 API 建入仓库；本地 24 项断言全过）
  - ⚠️ 遗留：CODEOWNERS 的强制 review 需仓库 Settings → Branch protection 开启 "Require review from Code Owners"，workflow 层无法代设，待主人在网页端开启
- [x] 5. issue 标签体系（v0.6 设计定案，见下）✅ 2026-10-14（9 个游戏标签已提前用 API 建入仓库；battle.yml：/battle 触发打「斗法」+「斗法/待战」，结算贴结果前打「斗法/已判」；labels.yml 新增 ensure-labels push 兜底 job 幂等补建全部游戏标签（含斗法三态子标签）；README 增「issue 标签导航」表；本地 YAML+断言校验全过；push 后线上 ensure-labels 实跑 success，斗法三态子标签已在仓库生效）

## 已知 bug

- [x] issue body 里的 `/battle` 不触发 issue_comment 事件——✅ 2026-10-14 修复：battle.yml 增加 `issues: [opened]` 触发，job if 双事件分流，CMD_BODY/CHALLENGER 用 `comment.x || issue.x` 兜底统一取值；模拟种子改用 `github.event.id`（comment.id 在 issues 事件下为空，会导致 issues 入口的种子后缀恒空，属顺带修掉的隐性 bug）。本地断言+模拟脚本注入双事件变量独立执行通过
- [x] 降世 issue 正文漏 YAML 原文（issue#2 已手动修复正文；workflow 根因在清单第 1 项一并修）

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
