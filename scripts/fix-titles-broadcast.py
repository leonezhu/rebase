#!/usr/bin/env python3
"""Replace the TCEOF python-heredoc broadcast block in battle.yml with pure bash.

Root cause being fixed: afdd173 (titles finalize) added a block whose combination
python3 - <<'TCEOF' ... TCEOF inside the run script made GitHub's workflow parser
reject the WHOLE file (startup_failure on every event; PyYAML/psych parse fine).
Bisect: reverting afdd173's battle.yml diff removed the startup failures.
"""
import yaml

PATH = '.github/workflows/battle.yml'
src = open(PATH, encoding='utf-8').read()

start = src.index("          # 威名授予播报(v0.18 称号收口)")
end = src.index("          TCEOF\n", start) + len("          TCEOF\n")

newblock = """          # 威名授予播报(v0.18 称号收口)：闭关复出——🎖️ 与 🩸/✨ 同级的戏眼
          # 修复注：旧实现用 python heredoc(<<'TCEOF')构造，令 GitHub workflow 解析器整体拒收
          # 本文件（PyYAML/psych 可解析但 GH 一律 startup_failure，issue/评论事件不再起 run——
          # 2026-10-15 e2e 实锤并二分定位到该块）。改纯 bash + stdin heredoc。
          if python3 -c "import json,sys;r=json.load(open('battle_result.json'));sys.exit(0 if r.get('winner') in r.get('comeback',[]) else 1)"; then
            WINNER=$(python3 -c "import json;print(json.load(open('battle_result.json'))['winner'])")
            WNAME=$(python3 -c "import yaml;print(yaml.safe_load(open('monsters/'+__import__('os').environ['W']+'/beast.yaml',encoding='utf-8'))['name'])" 2>/dev/null || true)
            gh issue comment ${{ github.event.issue.number }} -R leonezhu/rebase --body-file - <<BCEOF
          ## 🎖️ 威名 · 铸成

          > 威名不是谁赏的，是自己一场一场挣来的——

          **@$WINNER** 获授「**闭关复出**」——从闭关中被放出关来，还赢了这一场。
          BCEOF
          else
            echo "无威名授予，跳过播报"
          fi
"""

src = src[:start] + newblock + src[end:]
open(PATH, 'w', encoding='utf-8').write(src)

d = yaml.safe_load(open(PATH))
print('yaml OK, jobs:', list(d['jobs'].keys()))
print('battle steps:', len(d['jobs']['battle']['steps']))
