#!/usr/bin/env python3
"""rebase-guard 执法核心（平台无关）

输入（stdin JSON 或函数调用）:
  text          最终回复文本
  changed_paths 本回合变更文件路径列表
  attempt       本轮已重试次数（防循环）
输出:
  {"verdict": "allow"} 或 {"verdict": "block", "message": "..."}

适配模式:
  --adapter hermes      函数式: 由 __init__.py import 调用
  --adapter claude-stop Claude Code Stop hook: stdin=hook payload, stdout=decision JSON
  --adapter claude-pre  Claude Code PreToolUse: 预留
"""
import json
import re
import sys

# 剧情场判定: 这些路径出现=本回合在做游戏内的事
GAME_PATH_MARKERS = ("players/", "world/", "tales/")

# 对话禁词（汇报铁律 v2.1: GitHub 层词汇不入对话）
BANNED = [
    "issue", "pull request", "commit", "push", "workflow", "yaml", "yml",
    "github", "repo", "run id", "actionlint", "base64",
    "仓库", "部署", "入账", "校验",
]


def check_tale_updated(changed_paths):
    """动了角色档案/世界资产却没动传记 → 剧情未入史"""
    paths = [str(p).replace("\\", "/") for p in (changed_paths or [])]
    game = [p for p in paths if any(m in p for m in ("players/", "world/"))]
    tales = [p for p in paths if "tales/" in p]
    if game and not tales:
        return (
            "本回合你更新了角色档案或世界资产，但传记（tales/）没有一并入传。"
            "传记是世界的正史——请调用 scripts/append-tale.py 把本段剧情写入传记"
            "（或确认本次确实不构成剧情），然后再收尾。"
        )
    return None


def check_text(text, enabled=True):
    """对话纯度检查（默认关闭: 工程讨论会误伤, 由配置开启）"""
    if not enabled or not text:
        return None
    low = text.lower()
    hits = [w for w in BANNED if w in low]
    if hits:
        return "回复中混入了机制层词汇（" + "、".join(hits[:5]) + "）——天道的语言里没有这些词，请改写后重发。"
    if re.search(r"[A-Za-z]{2,}", text):
        return "回复中混入了英文单词——对话必须纯中文，请改写后重发。"
    if re.search(r"[0-9]", text):
        return "回复中出现了阿拉伯数字——状态用体感表达，钱财用汉字数字，请改写后重发。"
    return None


def evaluate(text, changed_paths=None, attempt=0, text_checks=False):
    """统一裁决。attempt>=2 放行（防死循环, 上层还有 nudge 上限兜底）"""
    if attempt >= 2:
        return {"verdict": "allow"}
    msg = check_tale_updated(changed_paths)
    if msg:
        return {"verdict": "block", "message": msg}
    msg = check_text(text, enabled=text_checks)
    if msg:
        return {"verdict": "block", "message": msg}
    return {"verdict": "allow"}


# ---------- Claude Code 适配 ----------

def _paths_from_transcript(transcript_path):
    """从会话记录里捞本回合 Edit/Write 触过的路径（宽松正则, 够用即可）"""
    paths = set()
    try:
        with open(transcript_path, encoding="utf-8", errors="ignore") as f:
            for line in f:
                if '"file_path"' not in line and "'file_path'" not in line:
                    continue
                for m in re.finditer(r"file_path[\"']?\s*:\s*[\"']([^\"']+)[\"']", line):
                    paths.add(m.group(1))
    except OSError:
        pass
    return sorted(paths)


def main():
    argv = sys.argv[1:]
    mode = argv[argv.index("--adapter") + 1] if "--adapter" in argv else "hermes"
    raw = sys.stdin.read() or "{}"
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {}

    if mode == "hermes":
        print(json.dumps(evaluate(
            data.get("text", ""), data.get("changed_paths") or [],
            data.get("attempt", 0), data.get("text_checks", False),
        ), ensure_ascii=False))
        return

    if mode == "claude-stop":
        # 防 Stop hook 死循环: 已因本 hook 续过一轮则放行
        if data.get("stop_hook_active"):
            print("{}")
            return
        changed = _paths_from_transcript(data.get("transcript_path", ""))
        v = evaluate(data.get("last_assistant_message") or "", changed, 0)
        if v.get("verdict") == "block":
            print(json.dumps({"decision": "block", "reason": v["message"]}, ensure_ascii=False))
        else:
            print("{}")
        return

    print("{}")


if __name__ == "__main__":
    main()
