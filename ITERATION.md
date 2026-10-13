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

- [ ] issue body 里的 `/battle` 不触发 issue_comment 事件（只监听评论）——短期靠"发评论不发 body"规避；长期可在 battle.yml 加 `issues` 事件触发并检查 body 前缀
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
- 另：explore 每日限额靠 `git log --since="today 00:00"`（runner 本地时区）grep commit message 查重，TZ=Asia/Shanghai 前缀在 `git log --since` 语法下行为存疑，建议改用固定 UTC 界线或按 issue 评论时间戳查重

## 卡住登记

（暂无）
