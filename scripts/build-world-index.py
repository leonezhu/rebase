#!/usr/bin/env python3
"""
自动生成 world/index.json 元数据清单
扫描 world/ 下各子目录的 yaml 文件，输出为统一的 index.json
tales/ 特殊：扫描 tales/*-*.md 文件，命名约定 owner-名字.md
"""
import yaml, json, os, sys, re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUTDIR = BASE / 'world'
OUTPUT = OUTDIR / 'index.json'

def load_yaml(path):
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f)

def scan_dir(dirpath, kind):
    records = []
    for p in sorted(dirpath.glob('*.yaml')):
        try:
            d = load_yaml(p)
            records.append(d)
        except Exception as e:
            print(f'[WARN] {p.name}: {e}', file=sys.stderr)
    return records

def scan_tales(dirpath):
    """传记：命名约定 owner-角色名.md，一人可有多条记录"""
    records = []
    for p in sorted(dirpath.glob('*.md')):
        m = re.match(r'^(.+?)-(.+)\.md$', p.name)
        if not m:
            print(f'[WARN] tales/{p.name}: 不符合 owner-名字.md 命名约定，跳过', file=sys.stderr)
            continue
        owner, name = m.group(1), m.group(2)
        text = p.read_text(encoding='utf-8')
        # 统计回目（## 第X回）
        entries = len(re.findall(r'^##\s+', text, re.M))
        # 取第一段引用块做简介
        desc_m = re.search(r'^>\s+(.+)$', text, re.M)
        records.append({
            'id': p.stem,           # leonezhu-雄大
            'owner': owner,          # leonezhu
            'name': name,            # 雄大
            'entries': entries,
            'desc': desc_m.group(1) if desc_m else '',
            'status': '连载中',
        })
    return records

def main():
    out = {}
    kinds = {
        'gongfa': OUTDIR/'gongfa',
        'artifacts': OUTDIR/'artifacts',
        'locations': OUTDIR/'locations',
        'npcs': OUTDIR/'npcs',
        'events': OUTDIR/'events',
        'titles': OUTDIR/'titles.yaml',
    }
    for kind, dirp in kinds.items():
        out[kind] = scan_dir(dirp, kind) if dirp.exists() else []
    # titles 是列表，单独扫描
    if OUTDIR/'titles.yaml'.exists():
        try:
            out['titles'] = load_yaml(OUTDIR/'titles.yaml')
        except Exception as e:
            print(f'[WARN] titles.yaml: {e}', file=sys.stderr)
    else:
        out['titles'] = []
    out['tales'] = scan_tales(BASE/'tales')
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    total = sum(len(v) for v in out.values())
    print(f'[OK] {OUTPUT} written — {total} total assets')

if __name__ == '__main__':
    main()
