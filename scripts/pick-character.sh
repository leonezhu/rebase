#!/usr/bin/env bash
# 多角色选通: /explore [@角色名] —— 一人可多档，显式指名或唯一活角色直通
# 输出: 选中的档案路径(打印到stdout, 失败时已发issue评论并exit 1)
set -u
EXPLORER="${1:-}"
ISSUE="${2:-}"
COMMENT="${3:-}"
REPO="${GITHUB_REPOSITORY:-leonezhu/rebase}"

CHARACTER=$(echo "$COMMENT" | sed -n 's/.*\/explore[[:space:]]*@\([^[:space:]]*\).*/\1/p' | head -1)
F=""

if [ -n "$CHARACTER" ]; then
  # 按角色名(档案name字段)或文件名片段匹配
  F=$(python3 - "$CHARACTER" <<'PYEOF'
import sys, glob, yaml
want = sys.argv[1]
for f in sorted(glob.glob('players/*.yaml')):
    d = yaml.safe_load(open(f, encoding='utf-8'))
    if d.get('name') == want or want in f:
        print(f)
        break
PYEOF
)
elif [ -f "players/$EXPLORER.yaml" ]; then
  F="players/$EXPLORER.yaml"
else
  # 无指名: 唯一活角色直通; 多个活角色 → 列出让选
  RES=$(python3 - "$EXPLORER" <<'PYEOF'
import sys, glob, yaml
owner = sys.argv[1]
lives = []
for f in sorted(glob.glob(f'players/{owner}-*.yaml')):
    try:
        d = yaml.safe_load(open(f, encoding='utf-8'))
    except Exception:
        continue
    if d.get('status') not in ('retired', 'fallen'):
        lives.append((f, str(d.get('name', f))))
if len(lives) == 1:
    print('ONE:' + lives[0][0])
elif len(lives) > 1:
    print('MULTI:' + '|'.join(n for _, n in lives))
PYEOF
)
  case "$RES" in
    ONE:*) F="${RES#ONE:}" ;;
    MULTI:*)
      NAMES="${RES#MULTI:}"
      gh issue comment "$ISSUE" -R "$REPO" \
        -b "🧭 你有多位角色：**${NAMES//|/、}**。指名探索：\`/explore @角色名\`。" || true
      exit 1 ;;
  esac
fi

# 兜底: 旧灵兽
if [ -z "$F" ] && [ -f "monsters/$EXPLORER/beast.yaml" ]; then
  F="monsters/$EXPLORER/beast.yaml"
fi

if [ -z "$F" ] || [ ! -f "$F" ]; then
  gh issue comment "$ISSUE" -R "$REPO" \
    -b "@${EXPLORER} 你尚未觉醒（players/ 无你的档案），秘境之门不识你的气息。先去 README 觉醒入道吧。" || true
  exit 1
fi

echo "$F"
