"""rebase-guard — Hermes 适配层

挂 pre_verify：回合收尾前，若本回合改过角色档案/世界资产但没动传记，
block 强迫 Agent 先走 scripts/append-tale.py 入传。

铁律见 SKILL.md（讲道理）；本插件是执法层（不讲道理）。
"""
import sys
from pathlib import Path

_CORE = Path(__file__).resolve().parent / "guard"
if str(_CORE) not in sys.path:
    sys.path.insert(0, str(_CORE))

from guard import evaluate  # noqa: E402

# 文本纯度检查默认关（工程会话会误伤）；对游戏会话可在 skill 流程里开
_TEXT_CHECKS = False


def _on_pre_verify(final_response: str = "", changed_paths=None,
                   attempt: int = 0, **_) -> dict | None:
    v = evaluate(final_response or "", changed_paths or [], attempt, _TEXT_CHECKS)
    if v.get("verdict") == "block":
        # Claude-Code Stop 形态, Hermes pre_verify 原生接受
        return {"decision": "block", "reason": v["message"]}
    return None


def register(ctx) -> None:
    ctx.register_hook("pre_verify", _on_pre_verify)
