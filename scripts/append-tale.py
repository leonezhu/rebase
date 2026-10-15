#!/usr/bin/env python3
"""传记续写(幕后统一入口): 回目中文自增 + 幕文追加 + eventlog同commit
用法: python3 scripts/append-tale.py <角色名> <回目名> <<'EOF'
正文(多行markdown)...
EOF
规则: 全卷终的传记拒绝续写; 回目自增由本脚本负责(调用方不管编号)"""
import sys, re, subprocess
from pathlib import Path

NAME = sys.argv[1]
TITLE = sys.argv[2]
BODY = sys.stdin.read().strip()

CNUM = {'零':0,'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9}
def cnum(x):
    if x < 10: return ['零','一','二','三','四','五','六','七','八','九'][x]
    if x < 100:
        t_, o = divmod(x, 10)
        return (['','一','二','三','四','五','六','七','八','九'][t_] if t_ > 1 else '') + '十' + (['','一','二','三','四','五','六','七','八','九'][o] if o else '')
    return str(x)

def parse_cn(a):
    if a.isdigit(): return int(a)
    CNUM = {'零':0,'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9}
    v = 0
    for ch in a:
        if ch == '零': continue
        if ch == '十':
            v = (v or 1) * 10  # 无十位则视作一十
        else:
            d = CNUM[ch]
            v = v + d if v >= 10 else v * 10 + d  # 十位已定后个位是加不是乘
    return v

# 找档案(含retired, 只读档名)
import glob
cands = [f for f in glob.glob(f'players/*-{NAME}.yaml')] or [f'players/{NAME}.yaml']
cand = next((c for c in cands if Path(c).exists()), None)
if not cand:
    sys.exit(f'未找到角色档案: {NAME}')
stem = Path(cand).stem
tale_f = Path(f'tales/{stem}.md')
if not tale_f.exists():
    sys.exit(f'传记不存在: {tale_f}')
mt = tale_f.read_text(encoding='utf-8')
if '全卷终' in mt:
    sys.exit('该传记已全卷终, 不再续写')

acts = re.findall(r'^## 第([一二三四五六七八九十百零]+)回', mt, re.M)
n = max((parse_cn(a) for a in acts), default=0)
sec = f'\n\n## 第{cnum(n+1)}回 · {TITLE}\n\n{BODY}\n'
tale_f.write_text(mt.rstrip() + sec, encoding='utf-8')
print(f'✓ {stem} 第{cnum(n+1)}回 · {TITLE}')
