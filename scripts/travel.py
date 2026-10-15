#!/usr/bin/env python3
"""行旅: /travel <地点id> —— 移动角色到指定地点, 记入世界记忆账本"""
import yaml, os, glob, subprocess, sys
from datetime import date

DEST = os.environ['DEST']
TRAVELER = os.environ['TRAVELER']
ISSUE = os.environ['ISSUE']
REPO = os.environ.get('GITHUB_REPOSITORY', 'leonezhu/rebase')

def gh(*args):
    return subprocess.run(['gh', *args], capture_output=True, text=True)

def find_doc(owner):
    for c in ([f'players/{owner}.yaml'] + sorted(glob.glob(f'players/{owner}-*.yaml'))):
        if os.path.exists(c):
            return c
    return None

loc_path = f'world/locations/{DEST}.yaml'
if not os.path.exists(loc_path):
    have = [os.path.basename(f)[:-4] for f in glob.glob('world/locations/*.yaml')]
    gh('issue', 'comment', ISSUE, '-R', REPO, '-b',
       f'🏝️ 天道翻遍了舆图，没有「{DEST}」这处地方。已知之地：{", ".join(have)}。')
    sys.exit(0)
loc = yaml.safe_load(open(loc_path, encoding='utf-8'))

pf = find_doc(TRAVELER)
if not pf:
    gh('issue', 'comment', ISSUE, '-R', REPO, '-b', '🏝️ 尚无你的行旅档案——先觉醒，再上路。')
    sys.exit(0)
d = yaml.safe_load(open(pf, encoding='utf-8'))
if d.get('status') in ('retired', 'fallen'):
    gh('issue', 'comment', ISSUE, '-R', REPO, '-b', '🏝️ 故人已退场，不再行旅。')
    sys.exit(0)
if d.get('activity') in ('biguan', 'seclusion'):
    gh('issue', 'comment', ISSUE, '-R', REPO, '-b', '🏝️ 你正在闭关，行不得路。让 Agent 把 activity 改掉出关，再启程。')
    sys.exit(0)

old = d.get('where', '未知之地')
d['where'] = DEST
d['activity'] = 'traveling'
yaml.safe_dump(d, open(pf, 'w', encoding='utf-8'), allow_unicode=True, sort_keys=True)

log_f = f'world/eventlog/{date.today().strftime("%Y-%m")}.yaml'
entry = ('- day: ' + date.today().isoformat() + '\n'
         '  actor: ' + TRAVELER + '\n'
         '  name: ' + str(d.get('name', TRAVELER)) + '\n'
         '  where: ' + DEST + '\n'
         '  what: 自 ' + old + ' 行旅至 ' + loc['name'] + '\n'
         '  consequence: where=' + DEST + ', activity=traveling\n'
         '  evidence: issue#' + ISSUE + '\n')
os.makedirs('world/eventlog', exist_ok=True)
open(log_f, 'a').write('\n' + entry)

subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'])
subprocess.run(['git', 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com'])
subprocess.run(['git', 'add', pf, log_f])
subprocess.run(['git', 'commit', '-m', f'行旅: {d.get("name", TRAVELER)} {old}→{loc["name"]}'])
r = subprocess.run(['git', 'push', 'origin', 'HEAD:main'], capture_output=True, text=True)
if r.returncode == 0:
    msg = ('🧭 **' + str(d.get('name', TRAVELER)) + '** 启程，自 ' + old + ' 行至 **' + loc['name'] + '**。\n\n'
           '> ' + str(loc.get('desc', '')) + '\n\n'
           '*（已记入世界记忆账本。同处之地者，方可 /battle 相约。）*')
    gh('issue', 'comment', ISSUE, '-R', REPO, '-b', msg)
else:
    print(r.stderr[-300:])
    sys.exit(1)
