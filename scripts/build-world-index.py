#!/usr/bin/env python3
"""
自动生成 world/index.json 元数据清单
扫描 world/ 下各子目录的 yaml 文件，输出为统一的 index.json
"""
import yaml, json, os, sys
from pathlib import Path

BASE = Path('/Users/xiong/Documents/GitHub/rebase/world')
OUTPUT = BASE / 'index.json'

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

def main():
    out = {}
    kinds = {
        'gongfa': BASE/'gongfa',
        'artifacts': BASE/'artifacts',
        'locations': BASE/'locations',
        'npcs': BASE/'npcs',
        'events': BASE/'events',
        'tales': BASE.parent/'tales',  # tales/ at repo root
    }
    for kind, dirp in kinds.items():
        if dirp.exists():
            out[kind] = scan_dir(dirp, kind)
        else:
            out[kind] = []
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f'[OK] {OUTPUT} written — {sum(len(v) for v in out.values())} total assets')

if __name__ == '__main__':
    main()
