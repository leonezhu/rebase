# 命令速查与调试坑（references）

## 命令速查（Agent 自用）

> 前置：先按 gamebook「世界仓库解析」确定 `$REPO`（自动探测 > 会话配置 > 默认 leonezhu/rebase）

```bash
# 读玩家档案（权威状态）
gh api repos/$REPO/contents/players/<玩家名>.yaml --jq .content | base64 -d

# 斗法（两步：建 issue + 补评论触发）
gh issue create -R "$REPO" -t "斗法：A 挑战 B" -b "/battle @B"
gh issue comment <issue号> -R "$REPO" -b "/battle @B"

# 探索（开 issue 或发评论均可）
gh issue create -R "$REPO" -t "秘境探索 · <地点>" -b "/explore [@角色名]"

# 移动角色
gh issue comment <issue号> -R "$REPO" -b "/travel <地点id>"

# 盯一次结算跑完（放后台）
gh run watch <run-id> -R "$REPO" --exit-status

# 传记入传（对话通道剧情必走；回目自增+全卷终保护由脚本负责）
python3 scripts/append-tale.py <角色名> <回目名> <<'EOF'
正文...
EOF
```

## 工具使用铁律

- **write_file 写已存在文件前必须 read_file**：write_file 拒绝覆盖未读取过的文件。写传记前先读完整内容，或用 patch 做定向编辑
- **git push 被拒时先 pull --rebase**：远端有新提交时 push 会被拒，先 `git pull --rebase` 再 push
- **Python heredoc 内联易坏**：多行脚本落盘独立 .py 文件再调用，避免字符串转义问题

## workflow 调试坑（实锤过的）

- **改 workflow 必跑 actionlint**：YAML safe_load 通过 ≠ GitHub schema 通过
- bash 变量写成 `${{WINNER}}`（双括号=GitHub expression）→ 骨架 failure：jobs 为空、run name 显示为文件路径
- python heredoc 里忘了 import（`glob` 等）→ 运行时才炸
- `grep -oP '[a-zA-Z0-9-]+'` 匹配不到中文角色名
- `github.event.comment.body` 直接内联进 run 有注入风险——经 env 变量传入
- python 源码经多层字符串转义（f-string 嵌 YAML 嵌 markdown）极易坏——**落盘独立 .py 脚本再由 workflow 调用**，是唯一稳的写法
- 斗法 issue 标签状态机：待战 → 已判 → 已收录
- `/battle` 建议建 issue 后补一条评论触发，时序更稳（body 触发有约 1 秒竞态，已由标签守卫化解）

## 传记回目解析坑（append-tale.py）

`parse_cn()` 解析中文数字时，**遇到'十'之后跟个位必须用加法而非乘法**：

- 错误算法：每个非零数字都 `v = v * 10 + digit` → "十一" 变成 `(1*10)*10+1 = 101`
- 正确算法：`v >= 10` 说明已进十位，后续个位是**加**，不是再乘一次十

修复后逻辑：
```python
if ch == '十':
    v = (v or 1) * 10  # 无十位则视作一十
else:
    d = CNUM[ch]
    v = v + d if v >= 10 else v * 10 + d  # 十位已定后个位是加不是乘
```

验证范围：1~99 全数正确。百位以上暂不支持（够用）。
