#!/usr/bin/env python3
"""同地与行事校验: 双方不在同一地点/对方闭关或退场 → 战书被天道驳回"""
import yaml, os, glob, sys

r0_f = 'battle_result.json'
import json
if not os.path.exists(r0_f):
    print('no battle_result.json, skip')
    sys.exit(0)
r0 = json.load(open(r0_f))
A, D = r0.get('challenger'), r0.get('defender')
if not A or not D:
    print('incomplete battle_result.json, skip')
    sys.exit(0)

def find_doc(owner):
    for c in ([f'players/{owner}.yaml'] + sorted(glob.glob(f'players/{owner}-*.yaml')) + [f'monsters/{owner}/beast.yaml']):
        if os.path.exists(c):
            return c
    return None

def locname(lid):
    try:
        return yaml.safe_load(open(f'world/locations/{lid}.yaml', encoding='utf-8'))['name']
    except Exception:
        return lid

pa, pd = find_doc(A), find_doc(D)
if not pa or not pd:
    print('::notice::缺档，跳过同地校验')
    sys.exit(0)
da, dd = yaml.safe_load(open(pa, encoding='utf-8')), yaml.safe_load(open(pd, encoding='utf-8'))

REASONS = []
wa, wd = da.get('where', ''), dd.get('where', '')
if wa and wd and wa != wd:
    REASONS.append(f'{da.get("name", A)} 身在【{locname(wa)}】，{dd.get("name", D)} 身在【{locname(wd)}】——千里之遥，战书寄不到。')

ACT_BLOCK = {'biguan': '闭关', 'seclusion': '闭关', 'retired': '长眠', 'fallen': '兵解', 'none': '长眠'}
act = dd.get('activity', '')
if act in ACT_BLOCK:
    REASONS.append(f'{dd.get("name", D)} 正在{ACT_BLOCK[act]}，不与外事。天道不打搅入定之人。')
if dd.get('status') in ('retired', 'fallen'):
    REASONS.append(f'{dd.get("name", D)} 已退场，传记已终卷，故人不接新战。')

if REASONS:
    body = '🏝️ **天道不允**：\n\n' + '\n\n'.join('> ' + x for x in REASONS)
    body += '\n\n*（同地校验——先把角色带到同一处，才有胜负可言。移动：评论 /travel <地点>。）*'
    import subprocess
    issue = str(r0.get('issue', '0'))
    repo = os.environ.get('GITHUB_REPOSITORY', 'leonezhu/rebase')
    subprocess.run(['gh', 'issue', 'comment', issue, '-R', repo, '-b', body], capture_output=True)
    sys.exit(1)

print('同地校验通过：', wa or '未知', '&', wd or '未知')
