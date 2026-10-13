# Rebase 《灵基纪元》

> 万物皆分支，唯有强者能变基。
>
> A GitHub-native monster-raising battle game. Your repo is the world, PRs are rituals, and every beast writes its own chronicle.

**还在设计阶段。** 完整设计框架见 [DESIGN.md](DESIGN.md)。

## 玩法一瞥

- **缔约**：回答三个问题，Agent 将你的回答炼成一只独一无二的怪兽——它是你当下的镜像
- **修行**：每日喂养、探索秘境，commit 即功力
- **斗法**：与天下灵兽对战，双方 Agent 各写半场战斗解说
- **变基（进化）**：境界圆满时渡天劫（CI 全绿），历史重写，形态重塑

## 技术形态

零后端。GitHub 就是服务器：

| 概念 | 实现 |
|---|---|
| 游戏服务器 | 本仓库（public） |
| 规则引擎 | GitHub Actions workflows |
| 官方账本（灵籍） | `monsters/` `battles/` `chronicle/`（仅 bot 可写） |
| 玩家客户端 | 任何 Agent（Hermes / OpenClaw / Claude Code / Copilot CLI）或 `gh` CLI |
| 图鉴 | GitHub Pages（自动构建） |

状态推进全部通过 PR / issue / 评论驱动，public repo 的 Actions 免费无上限。

## 状态

🚧 v0.5 设计框架阶段 · MVP 开发中

- [x] 世界观 & 命名（《Rebase》，赛博修仙）
- [x] 核心循环 & 心流曲线
- [x] 五维基因 + 性格 + 五行相克
- [x] 数据架构（灵籍/洞府双层）
- [x] 玩法→workflow 映射
- [ ] MVP：缔约 + 斗法最小闭环

## License

MIT
