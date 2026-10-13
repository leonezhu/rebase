# 迭代日志（ITERATION）

> 夜间 cron 每轮迭代在此记录。设计定案由主会话写入，施工项完成后打勾。

## 施工清单（cron 按序取项，每轮一项）

- [x] 1. 修 register.yml 的 YAML 解析 bug：awk 提取 origin 对多行不健壮 → 改 python yaml 库解析；顺带修复降世 issue 正文漏 YAML 原文问题（根因同一个）✅ 2026-10-14（origin/mystery 全文入正文，GITHUB_ENV heredoc 传变量，本地对真实灵籍演练断言通过）
- [ ] 2. explore.yml 秘境探索 workflow：issue 评论 `/explore` 触发 → hash 定遭遇表 → bot 贴事件故事 → 灵石/经验入账 bot commit
- [x] 3. catalog.yml + Pages 图鉴：main push 时扫描 monsters/*.yaml 生成玄幻暗色静态 HTML → GitHub Pages ✅ 2026-10-14（3 册灵籍本地渲染断言通过；首次上线需在仓库 Settings → Pages 把 Source 设为 GitHub Actions）
- [ ] 4. PR 双轨制（v0.6 设计定案，见下）
- [ ] 5. issue 标签体系（v0.6 设计定案，见下）

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

## 卡住登记

（暂无）
