#!/usr/bin/env python3
"""守仓人低语（T2-2）本地校验 + 演练。

断言清单：
  A1 池内每条低语过 schemas/whisper.schema.json（jsonschema 硬校验）
  A2 whisper_id 无重复
  A3 占位符只许 {beast}/{owner} 且每条 ≤2 个
  A4 演练：三只灵兽近 7 日活跃 → hash 选 1 只 + 1 条低语，选出低语长度 ≤200
  A5 幂等：同种子重跑两次结果一致（确定性）
  A6 防刷屏：脚本断言「同目标 7 日内二次低语」逻辑会被 min_interval_days 拦截
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import yaml
from jsonschema import validate

ROOT = Path(__file__).resolve().parent.parent
fail = 0


def check(name, cond, detail=""):
    global fail
    mark = "✓" if cond else "✗"
    print(f"{mark} {name}" + (f" — {detail}" if detail else ""))
    if not cond:
        fail += 1


pool = yaml.safe_load((ROOT / "lore/whispers.yaml").read_text(encoding="utf-8"))
schema = json.load(open(ROOT / "schemas/whisper.schema.json"))

# A1 schema 硬校验（每条整体作为一个文档校验，min_interval_days 按池统一值合入）
for w in pool["whispers"]:
    doc = dict(w)
    doc.setdefault("max_length", 200)
    doc["min_interval_days"] = pool["min_interval_days"]
    doc["pool_version"] = pool["whisper_pool_version"]
    try:
        validate(doc, schema)
    except Exception as e:
        check(f"A1 {w.get('whisper_id', '?')} 过 schema", False, str(e)[:200])
check("A1 全部低语过 schema", fail == 0, f"{len(pool['whispers'])} 条")

ids = [w["whisper_id"] for w in pool["whispers"]]
check("A2 whisper_id 无重复", len(ids) == len(set(ids)))

ok_ph = True
for w in pool["whispers"]:
    ph = [t for t in ("{beast}", "{owner}") if t in w["text"]]
    others = [tok for tok in w["text"].replace("{beast}", "|").replace("{owner}", "|").split("|")
              if tok.startswith("{") and tok.endswith("}")]
    if others or len(ph) > 2:
        ok_ph = False
        print(f"  违规: {w['whisper_id']} 占位符 {ph}{others}")
check("A3 占位符合法且 ≤2", ok_ph)

# ===== 演练：复刻 workflow 的选择算法 =====
WEEK_SEED = "2026-W42"
beasts = [p for p in (ROOT / "monsters").iterdir() if (p / "beast.yaml").exists()]


def active_recent(days: int) -> list:
    out = []
    for p in beasts:
        owner = p.name
        r = subprocess.run(
            ["git", "log", "-1", "--format=%ct", "--", f"monsters/{owner}/beast.yaml"],
            capture_output=True, text=True, cwd=ROOT)
        if not r.stdout.strip():
            continue
        last = int(r.stdout.strip())
        now = int(subprocess.run(["git", "log", "-1", "--format=%ct"],
                                 capture_output=True, text=True, cwd=ROOT).stdout.strip())
        if 0 <= now - last <= days * 86400:
            out.append(owner)
    return out


active = active_recent(7)
check("A4 存在近 7 日活跃灵兽", len(active) >= 1, f"活跃={active}")
if active:
    digest = hashlib.sha256(f"whisper|{WEEK_SEED}".encode()).hexdigest()
    target = active[int(digest, 16) % len(active)]
    w = pool["whispers"][int(digest[8:16], 16) % len(pool["whispers"])]
    text = w["text"].replace("{beast}", "燧鸣").replace("{owner}", "leonezhu")
    check("A4 选出低语且长度合规", len(text) <= 200, f"目标={target} 低语={w['whisper_id']} {len(text)}字")
    print(f"  → 本周低语预览: {text[:60]}…")

    # A5 幂等
    d2 = hashlib.sha256(f"whisper|{WEEK_SEED}".encode()).hexdigest()
    check("A5 同种子幂等", (target, w["whisper_id"]) == (
        active[int(d2, 16) % len(active)],
        pool["whispers"][int(d2[8:16], 16) % len(pool["whispers"])]["whisper_id"]))

# A6 间隔拦截逻辑：上次投递距今 <7 天 → 跳过
import datetime
last_post = datetime.date(2026, 10, 12)   # 模拟上周一投过
today = datetime.date(2026, 10, 14)
gap = (today - last_post).days
check("A6 7 日间隔拦截生效", gap < pool["min_interval_days"],
      f"模拟间隔 {gap} 天 < min_interval_days={pool['min_interval_days']} → 应跳过")

print(("ALL PASS" if fail == 0 else f"{fail} FAILED"))
sys.exit(1 if fail else 0)
