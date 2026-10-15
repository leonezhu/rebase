# rebase-guard

万灵变基录的执法插件。**skill 讲道理（SKILL.md 铁律），plugin 不讲道理（hook 强制）。**

## 执法内容

1. **传记必入传**：回合内更新了角色档案（players/）或世界资产（world/）却没动传记（tales/）→ block，强迫先调 `scripts/append-tale.py`
2. 对话纯度检查（文本层面）：预留，默认关（工程会话会误伤），按需开

## 平台支持

| 平台 | 目录形态 | hook | 状态 |
|---|---|---|---|
| Hermes Agent | `plugin.yaml` + `__init__.py` → `~/.hermes/plugins/` | pre_verify | ✅ 已实现 |
| Claude Code | `.claude-plugin/plugin.json` + `hooks/hooks.json` | Stop | ✅ 已实现 |
| Copilot CLI | 兼容读取 `.claude-plugin/` | agentStop（适配中） | 🔜 |
| OpenCode | TS 适配器（tool.execute.after） | — | 🔜 |

## 安装

**Hermes**（推荐 symlink，一份真源）:
```bash
ln -s <仓库>/plugins/rebase-guard ~/.hermes/plugins/rebase-guard
```

**Claude Code**:
```bash
claude plugin install <仓库路径>/plugins/rebase-guard
# 或开发调试: claude --plugin-dir <仓库>/plugins/rebase-guard
```

执法核心在 `core/guard.py`，平台适配层只做格式转换——规则改一处，全家生效。

## 防循环

- attempt ≥ 2 放行（同回合最多打回两次）
- Claude Code 尊重 `stop_hook_active` 标志
- Hermes 侧由 `agent.max_verify_nudges` 兜底
