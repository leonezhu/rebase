#!/usr/bin/env python3
"""斗法志索引生成器: chronicle/*/*.md → chronicle-index.json(Pages回放页数据源)"""
import glob, json, re, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
idx = []
for f in sorted(glob.glob('chronicle/*/*.md')):
    owner = f.split('/')[1]
    c = open(f, encoding='utf-8').read()
    m = re.search(r'^#\s+(.+)$', c, re.M)
    title = m.group(1).strip() if m else os.path.basename(f)
    issue = re.search(r'issue#?(\d+)', title + ' ' + f)
    idx.append({'owner': owner, 'file': f, 'title': title,
                'issue': issue.group(1) if issue else '',
                'excerpt': c[:200].strip().split('\n')[-1][:80]})
json.dump(idx, open('chronicle-index.json', 'w'), ensure_ascii=False, indent=1)
print(f'chronicle-index.json: {len(idx)} 场')
