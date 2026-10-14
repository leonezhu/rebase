# 迭代日志（ITERATION）

> 夜间 cron 每轮迭代在此记录。设计定案由主会话写入，施工项完成后打勾。

## 2026-10-15 03:1x 夜间轮：打磨第十六轮——传记静态地址链两条真断链实锤并修复（pages.yml 触发盲区 + 世界索引无人重铸）

### 发现（打磨模式演练，铁律⑧——上一窗口落 664a40a「传记地址统一为 tales/<id>.html 静态形式」，演练该新链路）
- **澄清一个疑似事故**：线上 `tales/leonezhu-雄大.html` 返回 HTTP 404 但响应体正是 404.html——这是设计内行为（GitHub Pages 对缺失路径返回 404.html 内容、URL 保持原样，兜底渲染器 JS 从 location.pathname 解析 id 拉 md 渲染）。本地 curl 双探针实锤，链路成立，非断链
- **真断链①（触发盲区）**：664a40a 把传记入口改成 tales-list.html + 404.html 兜底，但 pages.yml 的 push paths 没有这两个文件、也没有 `tales/*.md`——传记 md 入库/改文后 Pages **不自动重部署**，线上永远停留在最后一次部署的旧版本（当前线上 404.html/tales-list.html 是 dispatch 手动带上来的，下一次变更就会滞留）
- **真断链②（索引无人重铸）**：`scripts/build-world-index.py`（world/index.json 的 tales 字段来源=传记目录页数据源）**没有任何 workflow 挂载**——a98ef4e 提交语声称「index.json 由脚本自动生成」，但自动链从未接上，全仓 grep 实锤。新传记入库后 tales-list.html 目录页读到的永远是手跑时代的旧索引

### 修复（pages.yml 最小侵入）
1. push paths 补 `tales/*.md`、`tales-list.html`、`404.html`
2. build job 新增「构建世界资产索引」步：跑 build-world-index.py → 有变更才 commit（`git diff --cached --quiet` 幂等守卫）→ `pull --rebase` 并发保险 → push（沿用 catalog.yml 同范式，push 无 `|| true` 吞错）
3. 部署产物为整仓 checkout（`path: .`），新索引与改文后的 md 同一次 run 内一起上线

### 验证（6 断言全过）
- YAML parse + `on:` 字面键原文完好（只 patch run 块未触碰 PyYAML 回写）✓；三个新路径在位 ✓；索引步在位且 deploy needs 链完好 ✓；索引步 run 块 `bash -n` 语法过 ✓；build-world-index.py 幂等实跑（对当前 main 零 diff）✓；工作树收尾只剩本轮 pages.yml ✓
- 过程纪律：开工撞见并发会话 DESIGN.md 未提交改动（v0.20 称号打勾）——未触碰，该会话随后自行提交（df47da8），收尾工作树干净

### 线上验证（一红一绿，红灯=我方修复自己引入、并发会话同分钟修复）
- 首次部署 run 38620813420 红灯：索引步 push main 403——pages.yml job 级 `permissions: contents: read`（部署 job 只需读，我给 build 加写步骤后权限没跟着提），同 catalog.yml 2e180d7 事故模式
- 并发主会话 845844e（03:07，与我的修复 attempt 同分钟）已带同款修复 `contents: write` 入 main——本地 retry commit 时发现 working tree clean，对照确认修复内容一致，我方 commit 空手而归（避免重复提交）
- **终态线上闭环**：845844e Pages Deploy success ✓；线上 tales-list.html/404.html 均更新 ✓；`tales/雄大.html` 静态地址返回 404 状态码+404.html 渲染器内容（浏览器执行 JS 后正常出传记，设计内）✓

### 遗留观察项（记录不改）
- 索引步 push main 会再触发一次 pages.yml（paths 含 world/index.json）→ 二次 run 时 diff --cached --quiet 幂等跳过 commit、无空推送，但会多跑一次部署；若嫌噪音可后续给 push 加 `[skip ci]` 或 paths 排除 bot commit，属优化非缺陷
- catalog.yml 图鉴仍只渲染 monsters/（v2 后恒空，「全服灵籍 0 册」）——players/ 人修档案只做威名对账不渲染，属 v2 迁移待办（与 ITERATION 早前登记的「growth/rebase/catalog monsters 引用待轮替」同项），留主会话定夺是否给图鉴加人修卡

## 2026-10-15 03:1x 夜间轮：好玩路线图 T3「称号系统」收口施工（v0.20·威名不只是文案落地）

### 交付（五文件，随 f1869f4 入 main——被并发轮夹带，内容经逐文件 diff 核实无损）
- **world/lore/titles.yaml 威名录**：称号系统唯一权威账本，10 枚既有称号各配 effect（0.5%/1.0%）+ how（世界观口吻取得之道）+ first_seen 史料——授予逻辑 v0.14-v0.19 已散落三 workflow，本轮只补数值正源，不改任何既有授予条件
- **schemas/titles.schema.json 硬边界**：effect≤2.0（防单枚失衡）/名讳全中文 2-6 字/how 6-60 字零术语/granted_by_bot const true（威名只能天道授予）——数值 schema 先行铁律
- **battle.yml 战力加成**：双轨 power()（人修+灵兽）乘 titles_mult()=1+min(CAP,Σeffect)/100，全服封顶 TITLES_CAP=5%；威名录缺失/坏档显式红灯禁静默降级（账本类失败必须可见）
- **catalog.yml 威名对账闸**：双轨全查（monsters/ 灵兽 + players/ 人修档案），录外称号=伪造红灯+封顶对账（Σ>CAP=账实不符）
- **awaken.yml 防伪**：觉醒档案自带 titles=伪造拒绝（同灵根 hash 不可自选铁律）

### 沙盒验证（原样提取+对照实验）
- 战力对照 3 独立 seed：陆惊鸿（越级斩+初鸣）战力比值精确 1.015（注意：两枚=1.5% 不是 2.5%，粗断言第一次就抓出了我的记错——round(pb,1) 引入 ~2e-4 噪声，去掉 round 后 1e-9 精确）
- 封顶实锤：10 枚全拿比值精确 1.05（8% 封为 5%）
- 对账闸反例（天下第一）红灯+正例（现存 5 档零伪造）通过；awaken 防伪反例（自带初鸣）拦截+合法空 titles 不误伤
- 威名录过自家 schema+name 唯一+granted_by_bot=false 反例正确拒绝

### e2e（部分达成，候补登记）
- catalog run 38619514838：对账闸线上 success（威名录加载+players/ 三档全查）✓
- battle issue#99（雄大×陆惊鸿）：run 38620015024 sim 段实锤威名录生产加载成功，但战斗被**既有灵性闭关闸**拦下——雄大昨日连败三场 spirit=10，UTC 日期未翻惰性恢复不触发（+20=30 恰好不<30，北京 UTC+8 零点后可战）。属正确游戏行为非 bug，但「带威名首战入账」候补待 UTC 翻日后自然验证
- 处置：issue#99 留世界观收尾评论（引路灵劝闭关），不刷重赛

### 教训
- **并发夹带第三次应验**：五文件 commit 前被并发轮 f1869f4 打包推上 main（对方 tale 修复+我五文件同 commit）——共享工作目录 add 后立即 commit，犹豫即夹带；本次靠逐文件 diff 核实零损失
- e2e 前先查玩家当前状态（spirit/心境）：雄大连败三日灵性见底，硬开战必吃闭关闸——game state 是 e2e 的前置条件，不是噪音
- 沙盒对照断言别用 round 过的输出做 1e-9 精确断言；unrounded 值才配精确数学


## 2026-10-15 02:5x 夜间轮：打磨第十五轮——awaken.yml 误杀斗法入账 PR（每场斗法必红灯的真 bug）实锤并修复

### 发现（打磨模式例行演练，铁律⑧——上一窗口主会话刚落人修v2大清理 df73eb3/a13138f，演练其断链）
- 全量体检 11 workflow + 3 player.yaml schema + world/ 16 文件：核心全绿；8 个 workflow 残留 monsters//lore/ 引用逐一过目定性——battle/explore 的 `players/ 优先, monsters/ 兜底` 是 v2「双轨清零」的有意碰撞兜底（灵籍迁移后 monsters/ 恒空=零碰撞），growth/rebase/register/catalog 的 monsters 引用是待轮替的 v2 迁移项（v2 生命周期走 players/，不属断链），**零真断链**
- **真目标在 awaken.yml 连续 3 次 failure**（run 38611408874/38613729518/38614002946，battle-log/90/93/95）——jobs=1 有步骤日志，**不符合**「bot 入账 PR 四链 startup failure + 重跑洗绿」已登记噪音模式（实测重跑三连，全部仍 failure、步骤报「发现 2 份」）

### 实锤根因
- awaken.yml 找 player.yaml 用 `gh pr view --json files`（=PR **全部**变更文件，不区分 added/modified），而斗法入账 PR 必然**修改**双方 players/*.yaml → 「一次觉醒只许一份 player.yaml，发现 2 份」误杀 → **人修 v2 的每一场斗法结算，awaken 必产一条红灯**
- 次生洞：即使过了计数闸，入账 PR 会流进「外人 PR → player/待审」步被打标签+评论（垃圾信息）；workflow_dispatch 触发时 `pull_request.number` 为空 → `gh api .../pulls//files` 必红灯

### 修复（随 74dd403/57c2b31 入 main）
1. 文件列表改 `gh api repos/{}/pulls/{}/files --jq 'select(.status == "added")'`——**只认新增**（觉醒=注册新档），modified 档不入计数；无新增档 → 写 `IS_REGISTER=false` 后跳过
2. merge/待审两步加 `env.IS_REGISTER == 'true'` 闸——入账 PR 零副作用流过
3. job 级 `if: github.event_name == 'pull_request'`——dispatch 触发安全 skip

### 验证（四断言全过）
- YAML parse + `on:` 字面键 + heredoc python compile + bash -n 全过
- 负向回放：真实入账 PR#96（2 个 modified）→ added 过滤=空 → IS_REGISTER=false → 全步跳过 ✓
- 正向回放：真实觉醒 PR#86 → added 含 players/leonezhu.yaml → 走校验+auto-merge，行为不变 ✓
- 线上：workflow_dispatch run 38618306334 → job 正确 skipped ✓（修复后首个 pull_request 触发的入账 PR 留自然回归观察点）

### 过程记录
- 本轮 awaken.yml 修复在本地验证期间**未提交**，被同机并发会话的 74dd403/57c2b31（"修复专题页"提交、作者伪装 bot）夹带推上 main——内容恰好是已验证的本轮修复，零损失；但反向印证 ITERATION「夹带」教训：**共享工作目录下未提交改动随时会被并发轮打包，修完尽快 commit**，隔轮验证靠运气

## 2026-10-15 02:2x 夜间轮：打磨第十四轮——battle.yml 战前素材跨轨污染（玩家近事串到灵兽斗法史）实锤并修复

### 发现（打磨模式演练 battle 双轨，铁律⑧——上一轮 issue#90 e2e 只跑了玩家×玩家同轨）
- 沙盒混合轨重放（players/leonezhu × monsters/wild-leigu）：sim/入账/渲染三段全过，玩家档顶层字段兼容无 KeyError——上轮 7 连修的双轨归一本身是干净的
- **但 lore 段实锤跨轨污染**：`dossier()` 按 `glob(chronicle/<owner>/*.md)` 取「近事」，而人修玩家与旧灵兽**共用 owner 空间**——`chronicle/leonezhu/` 是灵兽燧鸣时代的半场志。玩家「雄大」的战前素材包里贴的是燧鸣火羽大战墨霄老蛟的故事
- **线上已发生**：issue#90（人修 v2 首战 雄大×陆惊鸿）战报素材包中，双方「近事」均为燧鸣斗法志——解说 Agent 若照素材包呼应「近事」，会把另一个角色的历史写进玩家的人生（叙事连贯性事故，非账务事故）

### 修复（最小侵入，灵兽轨零变化）
- `dossier()` 按 `'genes' in beast` 分流：灵兽轨照旧读 `chronicle/<owner>/` 半场志；人修轨改读 player.yaml 自身 `chronicle` 人生大事记末 2 条（v2 skill 定案「叙事前必读」的正源，本就该是它）
- 沙盒四断言全过：①玩家近事不再含燧鸣、改为「D10 藏经阁亲选赤阳吐纳法」等人生大事记 ✓ ②野游魂无 chronicle 目录返回空列表不崩 ✓ ③墨霄灵兽轨回归仍读 2 篇半场志 ✓ ④workflow YAML parse + `on:` 字面键 + 双 job 完整 ✓；monsters/*/beast.yaml 零触碰
- 演练红线复用上轮教训：渲染段 `subprocess.run(gh issue comment)` 先桩后跑，零外发

### 教训
- 「双轨」改造的演练矩阵必须有**混合轨**用例（玩家×灵兽）——同轨全绿≠跨轨安全；issue#90 恰好是玩家×玩家，把污染掩盖到了下一场
- `chronicle/<owner>/` 目录语义在 v2 里已经漂移（灵兽半场志 ≠ 玩家人生史）：凡按 owner 取叙事资产的代码，双轨时代都要先问「这个 owner 名下挂的到底是谁的历史」

## 2026-10-15 00:5x 夜间轮：打磨第十三轮——逮住 explore.yml 人修双轨半成品（严重）并修复

### 发现（打磨模式演练 68ca729 三件套 explore 双轨，铁律⑧）
- 68ca729 给 explore.yml 加 `players/<owner>.yaml` 双轨时**只改了文件路径、没改字段读取**：结算段 `d['element']`（旧灵兽顶层字段）在玩家档里嵌在 `spirit_root.element` 下，玩家探索必 `KeyError: 'element'` 崩溃。演练 1 沙盒原样提取实锤（leonezhu rc=1）
- **第二层同因崩溃**：social 段 `pa = d['personality']`——player.schema 无 personality 字段，玩家档 social 命中同样 KeyError
- **第三层 bot 层隐性 bug**（施工中顺带实锤）：入账步 `git add "$F"` 引用的 `$F` 是上一个 step 的 shell 局部变量，**跨 step 不传递**——该步 `$F` 一直是空值，旧轨时代靠 `git add monsters/` 兜底才碰巧没炸，双轨后玩家档会整单漏 add（commit 空 → push 无变更 → PR 合并不入账=账实不符）

### 修复（最小侵入，不改设计）
1. element 读取改 `d.get('element') or (d.get('spirit_root') or {}).get('element')`，缺源显式红灯不静默
2. social 触发条件加 `'personality' in d` 守卫——玩家档跳过同仓相遇（social 是灵兽世界的事件，不硬造性格数值），灵兽轨行为零变化
3. 入账步自行解析 `$F`（players 优先 monsters 兜底），消除跨 step 变量依赖

### 沙盒验证（enc 段原样提取，4 断言全过）
- ①玩家档普通遭遇：seed/权重命中与独立复算一致、star-fragments 动态遭遇正常并入 ✓
- ②玩家档 + social 命中 cid：跳过不崩、social=None ✓
- ③artifact 事件（cid=21）：法宝「储物旧镯」入 artifacts 栏（origin=秘境遗珍+日期）、ARTIFACT 播报行、重放逐字节确定 ✓
- ④回归：wild-leigu 旧轨 social/普通遭遇均正常 ✓
- workflow YAML parse + `on:` 字面键完好；monsters/*/beast.yaml 零触碰

### 教训
- 「加轨道」类改动必须演练**新轨全链路**（读字段→social 分支→入账 add），只验文件存在=半成品；本 bug 若上线，第一个玩家 /explore 就红灯
- bot 层跨 step 的 shell 变量（`$F`）是地雷：GitHub Actions 每个 step 独立 shell，此前没炸只是因为别处兜底——修 bug 时顺带审所有 `$VAR` 跨 step 引用

## 2026-10-15 00:0x 夜间轮：打磨第十二轮——逮住 awaken.yml 校验闸整体失效（严重）并修复

### 发现（打磨模式全流程演练，铁律⑧）
- 清单三项（register python 解析 / explore.yml / catalog）均已在前几轮完成；git log --since=40min 有产出（be946b6 叙事连贯性系统），按铁律⑦跳过清单进入打磨
- 例行演练（15 workflow YAML parse + `on:` 字面键 + players/monsters 双 schema 回归 + world/lore 数据文件 parse，全过）之后对 awaken.yml 做 hash 派生复核时，**发现 `if err:` 被注释掉**（ca176d8 事故）

### 实锤 bug（ca176d8 副作用，非故意）
- ca176d8「去掉名讳查重」删查重块时，把紧随其后的 `if err:` 误改为 `# if err:` → **校验失败分支永不触发**：schema 校验、缺字段检查、owner 一致性、**防作弊 hash 灵根闸**全部形同虚设——任何人可提交自选天根（purity 99 + heavenly）的 player.yaml 且必然过闸
- 时间窗：10-14 23:55 至本轮修复。期间线上只有 leonezhu 一册入册（灵根 fire/75/normal 与天道 hash 复算一致，是按公式生成的合规档），**存量零污染**

### 修复与验证
- 恢复 `if err:`（1 行）；沙盒三断言：①现行灵籍过闸（hash 复算 fire/75/normal 一致）②伪天根攻击样本（metal/99/heavenly）被拒 ③修复后 workflow YAML parse + `on:` 字面键完好
- 教训：删代码块时若块尾是卫语句开头，必须连带检查其缩进体归属——上轮 ITERATION 已有「演练先读尾部」红线，本轮证明演练断言必须覆盖「闸门真的会拒绝坏样本」而不仅是「好样本能过」

## 2026-10-14 23:1x 夜间轮：打磨第十一轮——v0.17 纯小说体演练（14 断言全过）+ 指引行非法转义顺手修

### 背景
- 40min 窗口内主会话落 v0.17 纯小说体战斗画面（91208ff）+ 零术语合规修（ed7f96d）+ import hashlib 补（16782bb），按铁律⑧对新代码演练，worktree 隔离

### 演练结果（sim 段+渲染段原样提取执行，14/14 PASS）
- 画面段：无回合标题（R1/R2/R3 行消失）、无伤害数值（`-数字` 招式行消失）、**小说本体零术语干净**、句式池衔接词在位、结局段在位 ✓
- 种子确定性：sim+渲染重放逐字节一致 ✓
- 血条数据层回归：渲染行数值与 frames.hp_a/hp_b 对齐（54967d9 老 bug 哨兵）✓
- 三场景：挑战方先手/守方先手（R1/R3 守方侧）轮转正确、同境无 override 回归 ✓
- 灵籍全程零触碰 ✓

### 实锤并修复：指引行 f-string 反引号非法转义（ITERATION 两轮登记的 cosmetic 项，本轮顺手修）
- **现象升级**：`f"- @{w} PR 到 \`battle/{ISSUE}-{w}\`"` 中 `\`` 是 invalid escape sequence（SyntaxWarning 由来），实际输出把 `\`` 原样带进 bot 评论——玩家看到的指引行是 `PR 到 \`battle/84-x\``，行内代码格式失效且带反斜杠杂符。不只是 cosmetic，是**可见显示瑕疵**
- **顺带的合规发现**：该行含「PR」技术术语，位于面向玩家的战斗画面评论内（虽属指引层非小说本体）
- 修复：改「请把本方半场心理戏以分支 battle/{ISSUE}-{w} 提交」——去转义、去术语、语义不变
- battle.yml YAML parse + `on:` 字面键校验过；全文件 `\`` 非法转义清零

### ⚠️ 演练操作事故与自救（给后续轮的红线教训）
- **渲染段尾部是 `subprocess.run(gh issue comment, check=True)`——原样提取执行会外发真评论**。本轮首次渲染执行时向 issue#84 误发 4 条雷骨 vs 尘舟战报评论，已用 API 全部删除还原（issue#84 终态 4 条：1 指令 + 拾焰战报 3，与施工时一致）；灵籍/账本零影响（演练只跑到渲染段，未进奖励入账步）
- **教训**：含网络副作用的段落演练必须先读尾部——凡 `gh`/`subprocess` 外发调用，提取后一律先桩后跑（本轮已用 `_fake_run` 桩重跑全绿）

### 线上状态
- issue#83/#84 双双正常结算（v0.17 首两战），唯观察项：#84 战报与血脉/天赋播报的评论顺序偶有交错（bot 三步连发，无账务影响）

## 2026-10-14 23:0x 夜间轮：好玩路线图 T3「灵兽社交」施工（v0.16）+ explore.yml 并发竞态实锤修复

### 设计（硬边界先行）
- 挂载点选择：/explore 内 25% 概率把本次遭遇**替换**为「同仓相遇」——不新增命令、不占额外额度、复用每日 3 次上限与既有入账 PR 链（工量最低且无新攻击面）
- 亲疏判定（数值归系统，确定性可回放）：五行相生→恒亲和；相克→性格 L1 距离 dist>180=宿敌/否则萍水；同行→dist≤120 亲和/180<dist 宿敌/其余萍水。零随机，seed 段 [12:16) 只选对象、[16:20) 只选文案
- 数值查表固定：亲和 +12石/+8功，萍水 0石/+4功，宿敌 -6石/+10功。只动评论者灵籍，对方灵籍零触碰
- 防刷三闸：world/social_log.yaml bot 独占写 + 落盘前 jsonschema 自校验（schemas/social.schema.json）+ 同对每日 1 次 + 近 7 日滚动窗口（schema maxItems 300 兜底）
- 叙事归玩家：lore/social.yaml 9 条文案池（亲/萍/敌×3），运行时占位符白名单 {name}{other}{el} + 零术语复检，不过显式红灯

### 实现
- schemas/social.schema.json（新）、lore/social.yaml（新）、.github/workflows/explore.yml（社交块 88 行 + bot 评论「同仓相遇」标题/social 提示行 + social_log 条件入账 commit）
- 本地验证：selfcheck 48 断言全过（schema 好/坏样本、文案池逐条、判定矩阵 6 case 手算对照——其间逮住自写相生表笔误水生火→修正水生木）；40 seed 沙盒重放：命中 10/40≈25%✓、同对同日重放正确落入查重跳过✓、宿敌路径（墨霄×砚灰 dist=245）构造验证✓

### e2e（issue#77，run 38585670612/38585844863 等）
- 三连 /explore：兽斗恶战（旧路径回归 ✓）→ **萍水·尘舟**（PR#78 自动合并，+0/+4）→ **亲和·雷骨**（+12/+8）
- **实锤真 bug**：两条 /explore 排队并发同跑，beast.yaml+social_log.yaml 双 add/add 冲突——PR#80 合并红灯，**bot 评论已向玩家宣告 +12/+8 但主仓未落账**（账实不符）。玩家侧最恶劣的一种静默失败
- 修复：explore.yml 入账步 push 前加 `git pull --rebase origin main`（5a300f2，与 abyss.yml 同范式）。观察项：rebase 只能吸收错峰入账，两 run 秒级真并发仍可能撞，届时显式红灯（可接受——红灯可重试，静默不可饶恕）
- #80 冲突手工化解合并（fd64ae7）：保留两笔相遇日志（都真实发生）、拾焰 exp 44+8=52/灵石 117 与评论宣告核对一致 ✓；验证 issue #77 关闭

### 红线自查
- monsters/*/beast.yaml 未手改任何数值（#80 化解是合并 bot 已宣告的入账，非凭空造数）
- 入账链零 || true 吞错；workflow YAML 本地 parse 过；对方灵籍全程只读

## 2026-10-14 22:3x 夜间轮：好玩路线图 T3「秘境遭遇动态化」收尾施工（v0.15 运行时硬边界）

### 定性：半成品补完，非从零实装
- 路线图行 322 未勾，但链路本体（lore.yml 投稿闸 / lore-reward 奖励 / explore.yml 动态并入）已在 10:0x 高频轮打通（PR#17~#24 端到端）——缺的是结算侧运行时硬边界：explore.yml 以 `try/except` 静默跳过加载失败的遭遇稿，且字段缺失时静默取默认值（weight=5/stones=10/exp=10），不符「schema 硬边界先行」既定模式
- **旧版风险实证**（沙盒三类恶意样本全部溜过静默闸）：`{0}` 越界占位符（线上 str.format 必 IndexError→结算崩）、`{__class__}` 注入、技术术语污染玩家文本——投稿闸（lore.yml）虽拦新稿，但运行时对已收录文件零复检，投稿闸被改/绕过时结算侧裸奔

### 交付
- **explore.yml 运行时三闸**（不过即 `::error` + exit 1 显式红灯，绝不静默降级）：①lore.schema.json jsonschema 自校验（bot 结算也必须过 schema）②占位符白名单只许 `{name}`/`{el}`（手写扫描器防 str.format 注入/坐标越界）③零术语复查（banned 列表与 lore.yml 同源）
- **lore.yml 投稿闸收紧**（追加不破坏既有）：占位符白名单（正则闭合对扫描）+ 零收益拒收录（stones=0 且 exp=0=白蹭著史奖励的钓鱼稿）
- 资格闸 schema 依赖：结算段 pip install 补 jsonschema

### 沙盒（28+ 断言全过）
- 14 workflow YAML 语法 + `on:` 字面键原文校验全过（PyYAML on→True 坑已防）
- explore 结算段**原样提取执行**（防沙盒/线上两套代码漂移）：现存 2 动态+8 内置遭遇并入、总权重 127 复算一致
- 运行时三闸正反 8 样本：合规过/`{0}`拒/`{__class__}`拒/术语拒/缺字段拒/越界拒/additionalProperties 拒/created_at 缺省（可选字段）过
- lore 新闸 6 断言 + 现存两篇投稿（断剑残鸣/星坠之壤）经新闸零破坏回归——不动既有功能铁律 ✓

### e2e（issue#73 → run 38578768924 → PR#74）
- c1fa559 推上后 test issue#73 评论 /explore → run success → bot 贴遭遇故事 + PR#74 自动合并
- 灵籍入账核对：功力 25→30（+5，lost 遭遇）、灵石 130 不动（lost 0 灵石设计内）✓
- 抽中内置 lost 非动态稿——seed 确定性反推可指名必中动态稿，但评论 id 由 GitHub 服务端分配无法预约，动态稿线上必中链留待自然探索验证（运行时加载逻辑已由「原样提取执行」覆盖，与线上同一份代码）

### 过程纪律
- 开工快照逮住并发 cron 的「雾渊更名」未提交改动（5 文件）——stash 隔离，随后并发会话自行提交上线（bb54006），stash 冗余已 drop
- 本轮 push 前 git fetch 复核（rebase 因未暂存改动拒绝→改为先 commit 再 pull --rebase，Fast-forward 无冲突）

## 2026-10-14 22:05 夜间轮：打磨模式演练（全流程）——逮住「败者复起」死代码 bug

### 演练结果（本轮零修复，符合铁律⑧）
- 全仓 YAML/JSON 语法全过；7 册灵籍 + world/abyss.yaml schema 校验全绿
- **深渊 e2e 线上复核**：22:0x 红灯 run 38576719723 定性为**设计内 reject**（同日二次 /abyss 触发每日限额 → bot 正确贴限额评论 + exit 1），勿当事故告警；成功链（首击 88 伤/反噬扣 10 灵石/入账 e54e570）正常——v0.14 深渊线上通过
- **battle 结算段 dry-run**（沙盒夹具 4 兽，对工作区版 battle.yml 原样提取执行）：同级首胜数值（stones+30/exp+50/spirit 100封顶-15=85）/败方代价（-15 保底/心境低落/streak+1）/称号幂等/越级 ×2.5+越级斩/灵性同日不重复恢复/schema 兼容——**除下述 bug 外全部通过**

### 发现的真 bug（在并发 cron 未提交的 battle.yml WIP 内，本轮不触碰避免夹带）
- **「败者复起」称号永远不可达（死代码）**：`奖励入账` step 第 457 行 `d['battle_history']['lose_streak'] = 0` 先清零，第 463 行才读 `lose_streak` 判 `>= 2` ——胜方连败史被提前抹掉，条件恒 False。修法：把 `streak = d.get('battle_history', {}).get('lose_streak', 0)` 提到清零行之前。
- 本轮沙盒已实锤：夹具胜方带 `lose_streak: 2` 入场，结算后 titles 只有 `['初鸣']`，缺「败者复起」
- 留给称号系统归属轮次修复（工作区改动归并发轮，避免跨轮夹带）

## 2026-10-14 22:0x 夜间轮：好玩路线图 T3-1「404深渊」施工（v0.14 世界Boss）

### 交付
- **schema 硬边界先行**（schemas/abyss.schema.json）：world/abyss.yaml 全服唯一状态文件——week_id(ISO周)/boss{name,title,element,hp_max恒600,hp_current}/slain/damage_log(owner+date+damage append-only)/rain_log(灵石雨台账)/updated_at；bot 独占写+落盘前 jsonschema 自校验
- **lore/abyss.yaml 文案池**：六名深渊主宰（缄碑/蔓冢/塌方/回潮/余烬/失焦，金木土水火金——同元素两名是有意的），每名 omen/taunt/weak_hint 三段；弱点暗示只给意象给谜面（碑文畏火/花畏金/悬土畏木/死水畏土/执火畏水/散光畏金），五行克制本身是谜底——zero 技术术语零数值
- **abyss.yml 双 job**：
  - attack（issue_comment /abyss）：资格闸（缔约→未slain→每日1次按damage_log查重）→ 伤害=战力×0.4（公式与battle.yml逐项同源：五行相克1.15/被克0.87/血脉+1.5%每段/灵性90+×1.05/<50×0.9/心境/hash涨落±10%）→ 30%反噬-10灵石保底0（PvE不白给）→ 击杀=hp归零→灵石雨（全员30+自身伤害/10，输出榜首+50，单commit入账全员beast.yaml）→ bot贴战况（血条🟥🟩十格+本周出手数+弱点点题）
  - weekly（周一cron 01:23 UTC+dispatch）：幂等开周报issue（`<!-- abyss:week_id -->` MARKER查重）
- **Boss 生成**：hash("abyss|"+ISO周) 从文案池确定性抽取，104周分布验证无断档；attack 按需自生成（不依赖weekly先跑），可回放不可操控；concurrency group=abyss 串行化
- README 指令表补 /abyss 行

### 沙盒（17 断言全过）
- workflow语法/concurrency/lore池/schema正反样本/hash分布/首击入账/满血一刀不死/反噬扣款/world落盘过schema/补刀击杀判定/灵石雨=30+伤害/10+榜首50/击杀后slain拒战
- 断言自身踩坑记录：PyYAML 把顶层 `on:` 解析成布尔 True 键——断言 `wf.get('on')` 恒空会假红灯（非 workflow 缺陷）

### e2e（四跑闭环）
- run 38576312753 **红灯逮住真 bug**：world/ 目录首周不存在 → `W.open('w')` FileNotFoundError（坐标系统没踩中只因 world/ 已被先前步骤建过）。修复=结算前 `Path('world').mkdir(exist_ok=True)`（c5b757c）。教训：**"新机制的首个状态文件"不能假设父目录存在——坐标是第二个吃 world/ 螃蟹的，深渊是第一个**
- run 38576508630 成功链实锤：拾焰（火）88 伤打余烬（火）【同五行无克制】、30%反噬命中-10灵石（130保住）、血条512/600、PR#71 bot 自动合并、world/abyss.yaml+灵籍同 commit 入账 ✓
- 同日重复 /abyss → run 38576719723 正确拒绝（"今日已入过雾"），failure 属 reject 设计预期
- weekly dispatch run 38576862438 success，周报 issue#72 开出（本周主宰·余烬）✓
- **击杀链（灵石雨全员入账）**：逻辑沙盒已验、线上待真实击杀自然验证（hp600 需约 7~8 人次/周）

### 过程纪律
- 开工/收尾各一次 git status 快照：收尾时工作区有并发 cron 的称号系统改动（battle.yml+beast.schema.json）——未触碰，DESIGN.md 勾选行单独 patch、仅提交 DESIGN.md+ITERATION.md
- 两次 push 前均 `git pull --rebase`（首次 rebase 上了并发 cron 的 ad73bc9..6d52bd9）

## 2026-10-14 21:5x 夜间轮：catalog.yml 只读令牌修复（线上红灯实锤）

### 发现
- catalog.yml 在 7674403 改为「生成 docs/catalog.html 纯存档」时，permissions 残留 `contents: read`（旧 Pages 部署被撤，但忘了改令牌权限）→ bot 有权读仓库却无权 push，「提交图鉴静态页」步骤恒 403（run 38573789907/38573812043/38573112973/38569868643 连续 4 次红灯）
- 顺带发现：concurrency group 仍是 `"pages"`——与 pages.yml 部署组同名，图鉴 bot commit 的 run 会 cancel/被 cancel 部署 run，撞车风险

### 修复（2e180d7）
- permissions 改 `contents: write`，删 pages/id-token 残留；concurrency 组改独立 `catalog`
- push 前补 `git pull --rebase`（checkout→生成→commit 期间 main 前进时防 non-FF 拒绝）
- 线上验证：手动 dispatch run 38574261156 success，bot commit 5bf9cd7 已入 main，docs/catalog.html 生成（7 册灵籍）

### 过程纪律（符合夜间铁律⑦）
- 开工发现 explore.yml 有未提交改动（转世豁免），未触碰，后证实为并发 cron 的工作且已自行提交（469c97b）——开工前 status 快照避免了夹带

## 2026-10-14 21:0x 夜间轮：好玩路线图 T2-3「重逢伏笔」施工（v0.12 旧分支坐标）

### 交付
- **schema 硬边界先行**（schemas/coordinates.schema.json）：world/coordinates.yaml 全服唯一状态文件，total_fragments 恒7/probes_required_per_fragment 恒20/unlocked 0-7/fragments 7段定长/probe_log 记 owner+上海日期；bot 独占写入，且 workflow 在落盘前 jsonschema 自校验（bot 也必须过自己的 schema）
- **coordinate.yml**：任意 issue 评论 /coordinate → 四重资格闸（灵籍存在→化神+→当日未测（probe_log 按 owner+日期查重）→灵石≥50）→ 扣50灵石+全服计数+1 → 每20次按序揭示1枚 → bot 贴探测结果（含进度条、新碎片全文、已显形碎片折叠列表）→ bot PR 入账（beast.yaml+world 同 commit，push/create/merge 零吞错）
- **碎片文本**：lore/coordinates.yaml 预作7枚（倒悬的海→重逢之日，零技术术语零数值，留白不解释）；workflow 只按揭示序取文本，不生成不改写——「叙事归玩家数值归系统」在 world 级的落地：任何 Agent 都不能写坐标数值，坐标叙事不进账本
- **并发安全**：concurrency group=coordinate 串行化揭示判定；seed 无随机成分（计数到阈值必揭示，天然幂等可回放）
- **README 命令表**补 /coordinate 一行

### 沙盒演练（11 断言全过，从 workflow 原样提取结算段执行）
- A1 未缔约拒绝 / A2 非化神拒绝（燧鸣 zhuji 实册）/ A3 灵石不足拒绝 / A4 首次探测成功+扣费50 / A5 同日重复拒绝 / A6 第20次揭示第1枚（文本=倒悬的海）/ A6a unlocked 与碎片入册一致 / A7 沙盒 world 文件独立过 schema / A8 第140次揭示第7枚封顶 / A8a 集齐后照常计数不越7

### 沙盒逮住的真 bug（已修）
- **集齐7枚后探测计数撞 schema 上限**：初版 probe_count/probe_log 设 maximum/maxItems=140，集齐后再探测 → 计数 141 → jsonschema 自校验炸 → 入账红灯且灵石已扣（白扣）。修正：去掉上限（集齐后照常计数保持审计连续性，仅揭示停止）。教训：**「有上限的字段」要问一句"到顶后机制是否还活着"——活着的循环不该被静态上限卡死**

### e2e
- ✅ 2026-10-14 21:0x 夜间轮补测（run 38568674361）：拒绝链线上实锤通过——leonezhu（燧鸣·筑基·295灵石）在 issue#62 评论 `/coordinate`，bot 正确回复「尚在筑基——旧分支的坐标太远」，workflow failure 符合 reject 设计；副作用查证干净：world/coordinates.yaml 未被误建、灵石未扣。**成功链（扣费+计数+揭示+bot PR 入账）线上仍未实测**——现库 7 册灵籍无一只化神+，需等首只灵兽修到化神（或测试期临时造化神灵籍）才能走通，留给后续轮次
- 注意：`/coordinate` 的 reject 走 `exit 1`，run 结论为 failure 属预期——监控告警勿把 coordinate 的 failure 一律当事故

### 过程教训
- workflow 块标量提取后必须 textwrap.dedent 再 compile/执行——缩进残留的 IndentationError 会伪装成「提取失败」
- worktree 外直接改工作区时，开工前 git status 区分并发 cron 的夹带改动（本轮 DESIGN.md 的「成长机制 v3」段落为主会话未提交进行时改动，本轮勾选行单独 patch 不触碰）

## 施工清单（cron 按序取项，每轮一项）

- [x] 1. 修 register.yml 的 YAML 解析 bug：awk 提取 origin 对多行不健壮 → 改 python yaml 库解析；顺带修复降世 issue 正文漏 YAML 原文问题（根因同一个）✅ 2026-10-14（origin/mystery 全文入正文，GITHUB_ENV heredoc 传变量，本地对真实灵籍演练断言通过）
- [x] 2. explore.yml 秘境探索 workflow：issue 评论 `/explore` 触发 → hash 定遭遇表 → bot 贴事件故事 → 灵石/经验入账 bot commit ✅ 2026-10-14（8 种遭遇加权随机，种子=评论者+评论id+当日次数可复现不可操控；每兽每日限 3 次按 bot commit 记录查重；败遭遇灵石保底不为负；本地演练权重分布+保底+语法断言全过）
- [x] 3. catalog.yml + Pages 图鉴：main push 时扫描 monsters/*.yaml 生成玄幻暗色静态 HTML → GitHub Pages ✅ 2026-10-14（3 册灵籍本地渲染断言通过；Pages 已于同日用 API 启用 build_type=workflow，首次部署成功，线上 https://leonezhu.github.io/rebase/ 已含 3 册灵籍）
- [x] 4. PR 双轨制（v0.6 设计定案，见下）✅ 2026-10-14（register.yml 双轨分流：主人=自动合并/其他玩家=止步 player/待审 禁止自动合并；降世 issue 统一移到 merged 后开（双通道通用+幂等防重+打「降世」标签）；新增 labels.yml=meta/规则 自动打标；CODEOWNERS=* @leonezhu；battle/explore 的 bot PR 打 game/bot；9 个游戏标签已用 API 建入仓库；本地 24 项断言全过）
  - ⚠️ 遗留：CODEOWNERS 的强制 review 需仓库 Settings → Branch protection 开启 "Require review from Code Owners"，workflow 层无法代设，待主人在网页端开启
- [x] 5. issue 标签体系（v0.6 设计定案，见下）✅ 2026-10-14（9 个游戏标签已提前用 API 建入仓库；battle.yml：/battle 触发打「斗法」+「斗法/待战」，结算贴结果前打「斗法/已判」；labels.yml 新增 ensure-labels push 兜底 job 幂等补建全部游戏标签（含斗法三态子标签）；README 增「issue 标签导航」表；本地 YAML+断言校验全过；push 后线上 ensure-labels 实跑 success，斗法三态子标签已在仓库生效）

- [x] 6. 守仓人低语（T2-2，v0.11）✅ 2026-10-14（schema 先行=schemas/whisper.schema.json 纯叙事硬边界：≤200字/零数值字段/占位符≤2——铁律"叙事归玩家数值归系统"由 schema 落地；文案池 lore/whispers.yaml 8条+whisper-pick.py 本地6断言全过（其间修掉一个断言自写错的假红灯A5）；whisper.yml 每周一确定性投递；e2e 三跑实锤：首跑投递步骤恒 skip → 根因 hashFiles() 不支持 /tmp 绝对路径（只认 workspace 相对模式），修复后真实投递 issue#62 ✓ + 同周重跑幂等跳过 ✓；观察项：wild-* 三兽由并发 cron 绕过 register 直接入库导致无降世 issue，低语机制"无锚即缄默"正确兜底，但降世 issue 缺失本身是 register 流程纪律问题，留给后续轮次定夺）

## 已知 bug

- [x] issue body 里的 `/battle` 不触发 issue_comment 事件——✅ 2026-10-14 修复：battle.yml 增加 `issues: [opened]` 触发，job if 双事件分流，CMD_BODY/CHALLENGER 用 `comment.x || issue.x` 兜底统一取值；模拟种子改用 `github.event.id`（comment.id 在 issues 事件下为空，会导致 issues 入口的种子后缀恒空，属顺带修掉的隐性 bug）。本地断言+模拟脚本注入双事件变量独立执行通过
- [x] 降世 issue 正文漏 YAML 原文（issue#2 已手动修复正文；workflow 根因在清单第 1 项一并修）
- [x] schema 缺 `spirit_recovered_at` 字段——battle.yml 灵性惰性恢复机制（ad69861 实装）会向灵籍写入该字段，但 schema `additionalProperties: False` 未声明，导致任何带此字段的灵籍过不了校验 PR。✅ 2026-10-14 修复：schema 补录该字段（type: string, format: date），3 册真实灵籍本地校验全过

## 设计定案 v0.6（2026-10-14，主会话）

### PR 双轨制（施工项 4）

| 通道 | 来源 | 合并策略 |
|---|---|---|
| game/bot | github-actions[bot] 生成的 PR（battle-log 入账、chronicle 解说） | workflow 尾部 auto-merge，打标签 `game/bot` |
| player | 人类玩家 register/growth/battle 分支 | 校验通过只打标签 `player/待审` + 评论"校验通过，等待驯兽师长老过目"，**禁止自动合并** |
| meta | 任何人改 workflow/schema/README | CODEOWNERS 强制 leonezhu review，标签 `meta/规则` |

实现要点：
- register.yml 的 auto-merge 步骤加条件：`github.actor == 'leonezhu'` 的 PR 且走 register 流程 → 自动合；其他玩家 → 止步于"校验通过"
- 新建 CODEOWNERS：`*.yml` `*.json` `.github/` 全部 `@leonezhu`

### issue 标签体系（施工项 5）

| 标签 | 用途 |
|---|---|
| 降世 | 怪兽降世传记 issue（每兽一个，永久存在 = 怪兽主页/操作台） |
| 斗法 | 对战 issue（状态子标签：待战 / 已判 / 已收录） |
| 秘境 | 定时投放的世界事件 |
| 放生 | 放生申请与冷静期追踪 |
| 悖论 | 玩家上报异常（bug/疑似作弊），全服可见审计入口 |
| 杂谈 | 社区闲聊，可乱 |

实现要点：
- workflow 里 `gh label create` 幂等建标签（带颜色：降世绿/斗法红/秘境紫/放生灰/悖论橙/杂谈蓝）
- register.yml 开降世 issue 时打「降世」；battle.yml 贴战报时给 issue 打「斗法」+状态子标签
- README 指令表更新 issue 导航说明

## 打磨模式（2026-10-14 03:40+，清单全完成后全流程演练）
### 演练结果（全部通过）
- 5 个 workflow YAML 语法全过；3 册灵籍 schema + owner/路径一致性全过
- explore.yml 结算脚本从 workflow 原样提取执行：遭遇抽取/保底不为负/只动 spirit_stones+exp ✓；万次抽样分布与权重偏差 <15% ✓
- battle.yml hash 模拟原样提取执行：胜负/五行修正/境界碾压 override 逻辑 ✓；模拟本身不改灵籍 ✓
- register.yml 降世故事生成原样提取执行：多行 origin 完整入正文（清单1回归）✓
- catalog 3 册渲染字段齐备 ✓
- 线上 failure 记录 run#38440895133 已查明：Pages 未启用时的一次性引导失败（同分钟启用后 dispatch 重跑成功），非活性 bug

### ⚠️ 发现（记录不改设计）：入账链路静默丢账风险
- battle.yml/explore.yml 的入账步骤 `git push || true`、`gh pr create || true`、`gh pr merge || true` 全部吞错：若并发两次结算同兽（如斗法奖励与探索入账同时跑），push 被拒后评论故事已贴、灵石却没落库——玩家看到余额承诺与账本不符
- 建议（留主会话定夺）：入账 push 失败时改为「重试 rebase 后再推一次，仍失败则 edit 已贴评论声明"天道入账受阻，请评论 /explore 重试"」，把静默失败升级为可见失败
- ~~explore 每日限额靠 `git log --since="today 00:00"`（runner 本地时区）~~ → ✅ 2026-10-14 打磨轮实锤并修复：该 approxidate 语法实测返回空集（限额恒 0 = 每日 3 次永不触发），改按 committer 上海本地日期精确过滤（--date=format-local），真灵籍与注入边界样本（跨日/+负时区）验证通过
- [x] 斗法三态状态机断链（2026-10-14 打磨轮发现并修复）：①「斗法/已收录」终态无任何 workflow 会打——解说 PR 合并后 issue 永远停在「已判」；②结算时「斗法/待战」不摘除，已判 issue 会同时挂待战+已判两个矛盾标签（线上 issue#3 因旧 GH_TOKEN bug 标签全空，属历史遗留）。修复：battle.yml 新增 chronicle-seal job（pull_request closed 触发，分支名 battle/<issue>-* 或标题 issue#N 提取，chronicle/ 下同 issue 半场 ≥2 篇才打终态，幂等防重），结算步加 --remove-label 待战。本地用 issue#3 真实状态演练判定通过（2 篇半场 → 应判已收录）；待下一次真实解说 PR 合并做线上回归


### 2026-10-14 20:45 ｜ 斗法胜场解锁的记忆碎片不同步（打磨轮发现并修复）
- **现象**：skill 定案「memory_fragments.unlocked 计数与血脉之力共用（境界节点+胜场解锁）」，rebase.yml 渡劫链在段数上涨时会同步揭示封印段为【待补】占位，但 battle.yml 斗法入账只更新 bloodline，不同步 memory_fragments——斗法赢 2 场触发「🩸 血脉之力·苏醒」时，说好的记忆段仍是【封印】，且集齐 5 段的觉醒剧情经胜场路线永远无法触发。
- **修复**：battle.yml 血脉入账段补 memory_fragments 同步逻辑（与 rebase.yml 渡劫链一致：新解锁段揭示为【待补·第N段——斗法胜场中闪回的碎片】占位，旧灵籍无字段则动态补建默认结构）。本地沙盒从 workflow 原样提取执行，4 场景断言全过：胜1场不涨段不揭示/金丹+2胜涨段揭示第3段/旧灵籍动态补建/大乘封顶5段揭示第5段；败方字段不受污染。

## 异常登记

### 2026-10-14 ｜ growth 链路缺失（打磨轮发现并补齐）
- **现象**：DESIGN.md「每日喂养」行与玩家客户端 skill 均依赖 growth PR → workflow 校验（当日限额/灵石余额/append-only）→ bot commit 入账的完整链路，但 5 个 workflow 中没有任何一个处理 `growth/` 分支——玩家提 growth PR 会静默悬挂（无校验、无入账、无反馈）。
- **修复**：新增 `growth.yml`（设计已有、实现缺失，属打磨轮演练发现的真缺口）。校验：①产权过滤（只许改 `growth/<分支owner>/`）②append-only（旧内容必须是新内容前缀，一条 `- ` 追加行=一次修行事件）③当日限额（含 bot 已入账查重，增量幂等结算）④灵石余额（10灵石/次）。入账：bot commit（功力+5/次，灵石-10/次）→ game/bot PR 自动合并；growth PR 本体走双轨制。
- **演练中发现并当场修掉的 bug**：限额查重的 `git log -- <path>` 漏 `--all`——bot 入账走独立分支 PR，其 commit 不在 base..head 第一父链上，查重恒 0 → 每日限额永不触发。已加 `--all` 并以 fork 风格分支结构复测（8 项断言全过：合规/篡改/越产权/限额边界=3/超限/分支owner不匹配/灵石不足/幂等重跑）。
- ⚠️ 同类隐患排查提示：explore.yml 的限额查重挂在 issue_comment 直接触发（checkout 后 HEAD=main），`git log -- path` 能看到 main 上已合并的 bot commit，故不受此 bug 影响——但若未来 explore 改走分支 PR，需同步加 `--all`。

### 2026-10-14 05:41 ｜ commit 日期伪造（已实锤，影响高频轮窗口判断）
- **现象**：cb90d75（限额时区修复）的 author/committer 日期双双伪为 `2026-10-13T14:00:00Z`（+0800 整点 22:00:00，分秒全零=手工覆写指纹）；GitHub Actions run 实锚显示其真正落远端时间为 +0800 2026-10-14 04:43。前后相邻 commit（81ab00d、39cba34）日期均为真实值，仅此一个被污染。
- **排查**：仓库全部 yml/sh/md 无 `GIT_COMMITTER_DATE`/`GIT_AUTHOR_DATE` 引用，本机环境变量亦无——非脚本系统性污染，疑为生成该 commit 的当轮会话一次性行为。
- **影响**：铁律⑦的 `git log --since="40 minutes ago"` 会把该轮误判为无产出，下一轮可能对已完成项重复施工。
- **建议（留主会话定夺）**：① 排查 04:43 前后哪个进程带了 GIT_*_DATE 生成 commit；② 高频轮开工前的窗口判断改为以 `gh run list --createdAt`（远端实锚）作辅助校验，本地 git log 只作参考。

## 打磨模式 第二轮（2026-10-14 08:0x，实锚 gh run 07:10 后 51 分钟）
### 演练结果（5 工作流 + 3 灵籍 + 图鉴 + growth/battle/explore/register 结算脚本全过）
- 6 workflow YAML 语法 + 3 册灵籍 jsonschema 校验全过
- battle dry-run：hash 模拟原样提取执行 ✓；临时改 luling 至 jindan（高两境）→「境界碾压」override 正确生效，灵籍当场还原 ✓
- explore 结算：幂等（同种子结果一致）✓；beast_lose 保底不为负 ✓；五维产权不动 ✓；5000 次抽样分布与权重偏差 <2% ✓；图鉴 3 册渲染+暗色风断言 ✓；register 多行 origin 全文入 issue 正文回归 ✓；growth 入账（灵石25-20=5/功力+10/五维不动）✓
### 🐛 本轮实锤并修复：explore.yml 败遭遇灵石「负账记正」
- **现象**：保底分支 `stones = old_stones - new` 把实际损失记成了正数——灵石 100 恶战丢 10，评论区与 commit message 都显示「灵石 +10 入账」，败遭遇叙事（被叼走灵石）与账本自相矛盾，且凭空发钱
- **修复**：改 `stones = new - old_stones`（负号保留，-5 实亏记 -5）；顺带修 STONES 展示 `>=0` → `>0`（0 灵石变动不再显示 "+0"）
- **回归**：保底样本（灵石5→0 入账-5）、足额样本（100→90 入账-10）、胜遭遇不变、展示格式 4/4 断言全过

### 2026-10-14 09:1x 高频轮：labels.yml PR files 检测崩溃（线上实锤）+ 并发施工踩踏警示
- 现象 1（已修）：labels.yml 的 label job 用 `git diff $BASE $HEAD` 检测规则层变更，浅克隆拿不到 base sha，报 `fatal: bad object 35b9459`，job exit 128（线上 pull_request 实锤）。改为 `gh pr view --json files` 取变更文件列表，不再依赖本地 git 对象，顺带省掉一次 checkout。本地对真实 PR#8 文件列表断言 meta 检测正确。
- 现象 2（过程记录）：本轮与另一并发轮次（e3a960d 至 PR#9，修 chronicle-seal 缺 checkout）在同一工作目录施工，发生 checkout 切分支、工作树覆盖、unresolved 冲突短暂共存的踩踏；本轮修复改在独立 git worktree 完成。建议：高频轮开工前先 `git worktree add` 隔离操作，收尾 worktree remove，主 clone 目录只留给入账/主会话。
- 线上正面回归：issue#6 全链路已走通——6732a9b 修复后的斗法 run success、战报单贴、battle-log/6 分支生成、双方半场 PR(#7/#8) 合并、chronicle-seal（e3a960d 修复后）成功打上「斗法/已收录」终态加封卷评论；并发轮 d37b603 已把滞留侧分支的入账补录对齐。

## 2026-10-14 21:4x 夜间轮：真红灯实锤并修复——斗法重赛守卫 exit 1 假故障（PR#41）

### 线上巡检发现（判定标准「重跑后仍 failure」首次抓到真目标）
- issue#37 run 38511165509（04:23:50Z）battle 斗法 failure。上下文：run#47 已正常结算 success 并打「斗法/已判」，~7 秒后 run#48 到达——**`/battle` 双触发**（issue body 与补充评论均含 `/battle`，正是玩家 skill「已知坑」两步触发法的直接后果），run#48 进入 replay-guard，正确贴出拒战评论后 `exit 1` → run 标红，重跑仍 failure（守卫每次都会撞上）
- 守卫行为正确（拒战评论已贴、账本无损），但把「重复指令」上报为故障：每次双触发必产红灯，污染真故障判定

### 修复（14faca2，PR#41 已合并）
- battle.yml replay-guard 分支 `exit 1` → `exit 0`（附注释：守卫已履职，非故障）
- YAML 语法 + `on` 字面键校验过；未触碰 PyYAML 整文件回写

### 顺带观察
- 04:24/04:25 battle-log/37、battle-log/39 两批各带 4 条 startup failure，与 12:2x 登记的平台噪音模式一致（主 run 全 success），非活性 bug
- 本轮红灯为线上巡检（「重跑后仍 failure」）抓到的**第一个真目标**——该判定标准有效，后续巡检节奏保持

## 2026-10-14 23:0x 夜间轮：打磨第八轮——斗法分镜血条错位（实锤并修复）

### 背景
- 窗口内主会话落了灵性+天赋系统（ad69861）与素材包模式（655c857）两大块新代码，本轮按⑧打磨模式对新逻辑做演练

### 🐛 实锤并修复：分镜血条渲染按 attacker 翻转 hp_a/hp_b（54967d9，已推送 main）
- **现象**（原样提取渲染段沙盒执行当场抓出）：R1 碰巧对齐，R2/R3（守方出手回合）血条左右颠倒——R1 燧鸣打鲁灵后血条却显示「燧鸣 100／鲁灵 10」，R2 显示「燧鸣 10.0／鲁灵 95.0」（应为 95/10），R3 鲁灵血条凭空从 10 回到 95 再归零——读者视角=鲁灵一击把燧鸣打到 10 血后燧鸣莫名回血翻盘，血条与胜负自相矛盾
- **根因**：sim 里 `hp_a/hp_b` 恒为挑战方/守方累计血量，与该回合谁出手无关；渲染段却写 `ha = f['hp_a'] if f['attacker'] == C else f['hp_b']` 按当回合 attacker 翻转
- **修复**：`ha = f['hp_a']`、`hb = f['hp_b']` 直接取用，附注释防回归
- **回归**：正序（leonezhu 挑战，R2 守方出手）+ 反序（鲁灵挑战，R1/R3 守方侧出手，含 drain 吸血天赋事件）两场景血条对齐断言全 PASS；battle.yml YAML 语法 + `on:` 字面键原文校验过
- **断言方法教训**：渲染行血条正则此前只断言「含数字」，未断言「与 frames.hp_* 精确相等」——成对字段修复的教训（13:0x 轮）在血条上重演，本轮断言直接对齐 sim 输出

### 顺带登记（记录不改设计）
- sim 段 TALENT_TXT/round_sim/rl/pa-pb 均为死代码（天赋文本实际由渲染段独立生成，round_sim 定义后从未调用）——不影响正确性，留主会话清理
- 渲染段含反引号的 f-string（`\\`battle/...\\``）产生 SyntaxWarning（invalid escape sequence '\\`'），Python 3.12 起为可见警告，建议改用单反引号原文——本轮未动，属 cosmetic
- 本次 push 与 bb04d5b（主会话世界观 v1）并发，worktree rebase 后再推——「演练基线可能过期」再次应验

## 2026-10-14 22:4x 夜间轮：打磨第十轮——v0.15 战斗画面三连修（bug 2+3）

### 背景
- 窗口内（40min）主会话落战斗画面直出 v0.15（c8ff07e）+ TODAY 热修（7d70ac7），按铁律⑧对新代码演练，worktree 隔离

### 实锤并修复三处（2baed9a，已推 main）
1. **schema 缺 `battle_history` 字段**（本轮最重）：79438f1 称号系统给 battle.yml 加了 `battle_history.lose_streak` 写入，但 schema 只申报了 `titles`——issue#75 的 bot 结算 commit（cfdd82f）已把该字段写进拾焰/墨霄两册真实灵籍，**两册账本过不了自家 schema 校验**（additionalProperties 红灯）。修复：schema 补 battle_history（lose_streak/win_streak，bot 独占），7 册真实灵籍全部回绿
2. **「战斗画面」血条错位回归**：v0.15 画面段 `💚 {an} {fr['hp_a']}` 按当回合 attacker 摆位——**54967d9 修过的数据层同款 bug 在新渲染段重演**。issue#75 线上实锤：R2（墨霄出手）显示「💚 墨霄 26.2」，26.2 实为拾焰血量。修复：ca/cb 恒取挑战方/守方名，沙盒以 issue#75 真实 frames 回归 3/3 对齐
3. **「败者复起」死代码修复**（ITERATION 打磨轮登记项，此前因属并发轮 WIP 未触碰）：`lose_streak=0` 先清后读恒 False。修复：`prev_lose_streak` 先读后清，沙盒临时 git 仓端到端实锤（连败 2 场后胜 → titles=['初鸣','败者复起']）

### 校验
- battle.yml YAML 语法 + `on:` 字面键；渲染段/结算段原样提取 compile 过
- 7 册灵籍 schema 7/7 PASS；乱入键反例仍正确拒绝
- 14 workflow 全量 YAML + on 键复验通过

### 教训（复训+新）
- **「新机制写入的字段必须同 commit 申报 schema」应是铁律**——titles 申报了、battle_history 漏了，因为后者是嵌套在称号逻辑里的隐藏副作用写入。写 bot 入账代码时逐字段对 schema 自查
- 成对字段修复的教训（13:0x 轮）第三次应验：数据层修过的错位，新写的渲染段照抄了错误直觉（按 attacker 摆位）——修 bug 时在 bug 现场留注释，本轮已在数据层 384 行与画面段 416 行各留一处
- 渲染段 f-string 反引号 SyntaxWarning 仍在（cosmetic，已登记未动）

## 卡住登记

（暂无）

## 2026-10-14 白天游玩轮（主会话）发现并修复

- [x] battle.yml 两处 jq 表达式引号嵌套错误（外层双引号包转义逗号→jq 解析失败，label 步崩，issue#6 实锤）→ 改单引号包裹（6732a9b）
- [x] chronicle-seal 缺 checkout 步骤——裸 runner 上 git ls-tree 报 fatal，HALF 恒 0，「已收录」终态永不打 → 补 checkout step（e3a960d），回归通过（issue#6 已打终态+贴封卷评论）
- [x] **根因级：bot 无 create PR 权限**——GITHUB_TOKEN default_workflow_permissions=read，gh pr create 报 "GitHub Actions is not permitted to create or approve pull requests"，入账 commit 全部滞留侧分支、main 账本永不清账（`|| true` 静默吞错）。已改仓库 Actions 权限 write+approve_pr，并补录：issue#2 秘境×2 + issue#6 斗法胜 + issue#3 墨霄入账（PR#10 合并），燧鸣账户 175 灵石/115 功力对齐
- **教训**：`|| true` 吞错是账务系统大忌——静默失败比崩溃更危险，账本类步骤失败必须显式报错

## 2026-10-14 10:0x 高频轮：lore-reward 三连修 + reward 链路首次真通（PR#17~#24 端到端）

### 结论
- **reward 链路首次端到端打通**：PR#22《雾隐栈道》合并 → bot 入账 commit 7219781（著史奖励+20灵石）→ lore-reward/22 → PR#23 自动合并 → 燧鸣 175→195 灵石。此前该 workflow 从未 success 过（PR#13/#14/#15 三连 skipped）。

### 实锤并修复的三个 bug（按时间序）
1. **heredoc 缩进塌陷**（run 38498057843）：`python3 - <<EOF` 的正文带 4 空格缩进，Python 解析报错后被 bash 当普通命令继续读，`EOF` 永远闭合不上→`syntax error: unexpected end of file`，步骤必崩。→ 改 `python3 -c`
2. **浅克隆 git diff 拿不到 base sha**（同 run，`fatal: bad object fb1c345`）：labels.yml 同款坑在 lore-reward 复发。→ 改 `gh pr view --json files` 取变更文件
3. **PyYAML round-trip 把 `on:` 写成 `true:`**（e176bc5 与 2cf3bcc 双双中招，后者是本轮用 safe_dump 整文件回写引入的，自纠于 PR#21）：裸键 `on` 被 PyYAML 解析为布尔 True，dump 回去变成 `true:`，workflow 触发器整体失效（run 名退化为文件路径，如 `.github/workflows/lore-reward.yml failure`）。→ 手工还原 `on:`，文件内已加警告注释：**严禁对此文件做 PyYAML 整文件回写**

### 过程教训
- 本轮前半段曾误判 e176bc5（并发会话产物）为 root cause——实际第一次 `true:` 病灶是自己 patch 引入的。教训：**用 PyYAML 改 workflow 必须只改 run 字符串，绝不能 load→dump 整文件**；怀疑别人之前先 diff 自己的工作树。
- 02:02 那批 4 个 failure run（jobs 为空、log 404、GitHub 提示 workflow file issue）经空 commit 探针（PR#24）证实为**瞬态启动失败**，当前 workflow 全部健康，无需处理；「连并窗口内 startup failure」值得留意，勿误诊为文件 bug。

### 遗留
- lore-reward 的入账 push/PR create/merge 仍带 `|| true` 吞错——「入账链路静默丢账」总登记项（见打磨模式第一节）在本链路同样存在，待主会话定夺统一方案
- 夜泉洗尘（PR#17）、石语（并发轮 PR#19）、雾隐栈道（PR#22）三篇测试遭遇已随链路验证留在 lore/encounters/，如嫌测试数据可另行清理（不属本轮职责）

## 打磨模式 第三轮（2026-10-14 10:4x 高频轮，worktree 隔离演练）
### 演练结果（全过，无新代码 bug）
- 8 workflow YAML 语法 + 3 册灵籍/7 篇遭遇 schema 全过；线上 run 无新增 failure（唯一红=已登记的 02:02 瞬态启动失败）
- battle hash 模拟（原样提取执行）：种子确定/模拟不改灵籍/境界碾压 override 全过 ✓
- explore 结算：只动 spirit_stones+exp、幂等、败遭遇保底（5→0 记 -5 负账）全过 ✓
- register 降世故事：3 行多行 origin 全文入正文（清单 1 回归）✓
- catalog 渲染：3 册齐/暗色/境界/五行着色/余额全过 ✓
- growth 校验（sha 语义复现真实 PR 入参）：合规 delta=1/篡改拒/超限拒(4>3)/余额不足拒(5<10) 全过 ✓
### 演练方法教训（非代码 bug）
- 提取 workflow heredoc 演练时，HEAD 入参必须传 commit sha（真实 PR 触发传 head.sha）——误传分支名时 `git diff <base> <分支名>` 因分支名与目录同名解析成路径报 128，而 `sh()` 不查 returncode 静默拿空 diff，得出「合规场景也跳过」的假阴性。顺带确认：真实触发路径不受此影响（sha 永远无歧义）
### 🐛 发现（bug 级，登记待修）：入账链 `|| true` 连锁吞错使 bot PR 创建失败完全不可见
- battle/explore/growth 三处入账步骤同构：`git push || true` → `gh pr create ... || true` → `gh pr merge ... || true`。若 pr create 失败（权限/网络/分支已存在），merge 必失败也被吞——结算故事已贴、灵石未落库、workflow 显示 success，零痕迹。白天「bot 无 create PR 权限」事故（issue#2/#6/#3 补录）即此模式的真实爆发
- 与「入账链路静默丢账」总登记项同源但更具体：**pr create 是链路咽喉**，其失败必须显式报错（去掉 create 上的 `|| true` 即可让 step 红灯），push/merge 失败也会随之可见
- ✅ 2026-10-14 高频轮已按建议修复（见下「入账链去吞错」节）

## 2026-10-14 11:xx 高频轮：入账链去吞错（`|| true` 连锁吞错修复）

### 改动（4 文件）
- battle.yml / explore.yml / growth.yml 三处入账链：`git commit` / `git push` / `gh pr create` / `gh pr merge` 全部去 `|| true`——push/create/merge 任一失败即 step 红灯，静默丢账升格为可见失败；仅保留 `gh pr edit --add-label` 上的 `|| true`（标签失败无账务影响）
- lore-reward.yml：奖励入账链同改（push 已无吞错，pr create/merge 去吞错）；「著史者名录」步 `git push origin main || gh pr create ... || true` 三连环拆开——push 显式报错、pr create 单列；run 块由折叠标量整文件重写为块标量（转义地狱根治），奖励步 python 压单行（块内顶格行会终止块标量，勿写多行 python）

### 校验
- 8 workflow YAML 全过；触发器 4 改动文件 `on` 键完好（未触碰 PyYAML 回写）
- 4 个改动文件全部 run 块提取 `bash -n` 语法全过
- lore-reward python 单行 compile 校验通过
- 咽喉断言：4 文件 push/create/merge/commit 行无 `|| true` 残留

### 遗留
- 修复后入账失败会体现为 workflow 红灯（正是目的），但尚无「失败后 edit 已贴评论告知玩家重试」的补偿动作——本次只做可见化，补偿留主会话定夺
- 下一轮观察点：一次真实 explore/battle 触发验证新入账链线上跑通（去吞错后的正确路径与此前行为一致，理论上零行为变化）

## 打磨模式 第四轮（2026-10-14 11:4x 高频轮，worktree 隔离演练）
### 演练结果
- 9 workflow YAML 语法 + 触发器 `on` 键完好 + 3 册灵籍/7 篇遭遇 schema 全过
- battle dry-run（原样提取执行）：种子确定性/模拟不改灵籍/境界碾压 override（lianqi 临时提 jindan→碾压生效→当场还原）✓
- explore 结算：种子确定性/五维产权不动/保底负账等价式 ✓
- growth 校验 sha 语义（临时仓 8 场景）：合规 delta=2/篡改拒/前插行拒/越产权拒/超限拒(4>3)/余额不足拒(5<10) 全过 ✓
- register：降世故事 python yaml 解析在位、无 awk 残留（清单 1 回归）✓
- catalog：3 册渲染齐（炼气期/灵石/暗色），REALM_CN 映射与 schema realm 枚举 7/7 一致 ✓
- 入账链咽喉断言：battle/explore/growth/lore-reward 四文件 push/create/merge 无 `|| true` 残留 ✓

### 🐛 本轮实锤并修复：rebase.yml（并发轮新增）入账链 merge 吞错漏网
- **现象**：并发轮新增的进化 workflow 入账链 `gh pr merge "$BRANCH" --merge || true`——push/create 已红灯可见，但 merge 失败被吞：账滞留侧分支、main 未清账、step 仍 success，动画照贴（「余额 X」承诺与账本不符）。与上轮四链路去吞错标准不一致，属同构修复漏网
- **修复**：去掉 `|| true`（PR#27 → 合并 bbe37f2，本地 YAML + 触发器校验过）

### 发现（记录不改设计，留主会话定夺）
- rebase.yml job if **硬编码单兽**：`issue.title == '📜 降世 · 燧鸣（火）'` 且灵籍路径写死 `monsters/leonezhu/beast.yaml`——当前只有燧鸣一只可进化，其他兽评 `/rebase` 会被静默跳过（无任何反馈评论）。建议改为「评论者自己的降世 issue + 评论者灵籍」通用路由，并对不满足条件的评论给一句拒绝回应
- rebase.yml 顶部定义了 `REGEX` env 但从未使用（死配置）；触发判定实际用 `startsWith(comment.body, '/rebase')`，`/rebase 加参数`（如 `/rebase force`）也会通过——建议二选一清理
- rebase.yml 渡劫动画步 `sleep 2` 后 merge：PR create 到 merge 间无合并就绪等待，若 runner 慢可能偶发 merge 404（当前被 `|| true` 掩盖，去吞错后可能暴露为红灯）——观察点

### 演练方法教训
- 并发施工窗口：开工 `git pull` 后 5 分钟内远端又进新 commit（rebase.yml），本轮演练以 pull 后 HEAD 为准做了一次、修复时重新对齐远端——worktree 隔离 + 收尾 `git pull --ff-only` 复核可兜住，但「演练基线可能过期」应成为高频轮默认假设

## 2026-10-14 12:2x 高频轮：bot 入账 PR 四链 startup failure 实锤（重跑可洗绿，修复无效已回滚，待主会话定夺）

### 现象（确定性复现，非瞬态）
- **每一个** github-actions[bot] 创建的入账 PR（rebase-log/2、explore-log/*×2、lore-reward/22、battle-log/31、battle-log/35）上，挂 `pull_request: [opened/synchronize]` 的 4 个 workflow（register/growth/labels/lore）必然 startup failure：0 job、0 check-run、页面提示 "This run likely failed because of a workflow file issue"，run 挂在 PR 的 head sha 上
- 只挂 `pull_request: [closed]` 的 battle/lore-reward 在同一批 PR 上零失败；人类分支的 PR 全天零失败；同 sha 的 main push 全 success
- 每次真实入账（rebase/battle/explore）都会同步产生 4 条红灯噪音

### 实锤「非文件 bug」的过程
- 重跑任一 failure run → job 正常求值、正常 skip（本轮已把 14 个历史 failure 全部重跑洗绿：explore×8、battle-log/31×4、rebase-log/2×1、lore-reward/22×1、battle-log/35×4）
- 失败只发生在 PR create→merge 的 ~2 秒高速窗口内排队的 run；merge ref 计算期分支状态被并入/清理打断，疑为平台启动层竞态（未拿到 GitHub 官方文档佐证，标注为推测）

### 修复尝试（无效，已完整回滚，防重蹈）
- 第一版在 4 个 workflow 的 pull_request 触发器加 `branches-ignore: [battle-log/**, explore-log/**, ...]`——提交前自查 GitHub 官方文档发现两个致命伤：① `branches`/`branches-ignore` 过滤的是 PR 的 **base** 分支（所有入账 PR 的 base 都是 main，根本拦不住），head 分支只能在 job `if` 里用 `github.head_ref` 过滤（on 层做不到）；② 同一事件**禁止**同时用 `branches` + `branches-ignore`（4 个文件都定义了 `branches: [main]`），硬上会让 workflow 解析失败、连 issue_comment/push 等其他触发器一起报废
- 补丁在 worktree 内做出、未 commit，验证思路失败后 checkout 还原、worktree remove，主仓零污染

### 建议（留主会话定夺，二选一）
1. **job if 过滤 head 分支**：4 个 workflow 的 job `if` 加 `&& !startsWith(github.head_ref, 'battle-log/')` 等 5 个 bot 分支前缀（lore.yml 已有 head_ref 条件可顺带扩展）——job 层求值在 startup 之后，能挡住吗未经验证：startup failure 发生在 job 求值之前的话此路同样不通，需先做一次实验性 commit 验证
2. **容忍噪音**：startup failure 本身无账务影响（入账链自己的 run 全 success），把「入账 PR 附带 4 条红灯」当作已知噪音接受，发现真 failure 时以「重跑后仍 failure」为判定标准
- 另一个未验证的旁路：入账链改用 `gh pr create --fill` 前先给 PR 打 draft 或先用 API 预建 check 豁免——均属设计层改动，本轮不动
## 2026-10-14 12:5x 高频轮：打磨第五轮——斗法分镜守方境界英文漏翻（实锤并修复）

### 演练结果（全过，含一项新修复）
- 9 workflow YAML 语法 + 触发器 `on` 键完好 + 3 册灵籍 schema 全过；入账链咽喉断言（push/create/merge 无 `|| true` 残留）✓
- explore 结算原样提取执行（8 项断言）：结算执行/灵石与结算一致/保底不为负/败遭遇负账记负/胜遭遇非负/幂等/2 万次抽样权重偏差 3.1%/保底等价式(5→0记-5) 全过 ✓
- battle hash 模拟：种子确定性/模拟不改灵籍/分镜三回合/attribution 对齐（12:27 修复回归）/境界碾压 override 全过 ✓
- growth 校验语义（临时仓复现）：产权过滤/append-only 真前缀/追加行计量(1与2)/篡改拒/超限拒(2+3>3)/限内通过(2+1=3)/余额计算 全过 ✓
- register yaml 解析在位、多行 origin 完整、catalog 3 册齐 + REALM_CN 7/7 枚举覆盖 ✓

### 🐛 本轮实锤并修复：守方境界英文漏翻
- **现象**：分镜渲染第 3 行守方显示 `墨霄（水·lianqi）`——12:27 的 4e8f349「境界中文显示」只给挑战者侧 a['realm'] 加了 `REALM_CN.get` 映射，守方 b['realm'] 漏网，渲染断言「双方境界中文」当场抓出
- **修复**：65ff060，守方同过 `REALM_CN.get(b['realm'], b['realm'])`；本地渲染回归输出 `燧鸣（火·筑基） ⚡ vs ⚡ 墨霄（水·炼气）`；线上 push run success
- **教训**：成对字段的修复必须两侧同改——上轮只断言了「含中文」，未断言「无英文残留」，本轮断言加严后立即抓出

### 线上观察
- 04:24-04:25Z battle-log/37 与 battle-log/39 两批入账 PR 又各带 4 条 startup failure（与 12:2x 登记的平台噪音模式完全一致，非活性 bug，判定标准仍是「重跑后仍 failure」）

## 2026-10-14 13:0x 高频轮：打磨第六轮——rebase/lore/labels 三链首演（全过，零修复）

### 演练结果（前五轮未覆盖的三条链，本轮补齐）
- 全 9 workflow YAML 语法 + `on` 字面键复验 ✓
- **rebase.yml 渡劫校验**（原样提取，沙盒灵籍 6 场景）：功力不足拒/灵石不足拒/渡劫成功（zhuji→jindan、扣50、功力保留）/天梯之顶拒/非法境界拒/渡劫后再触发按金丹门槛(600/400)再拒 ✓；真实仓库灵籍全程未动 ✓
- **lore.yml 第1步变更范围**（临时 git 仓）：篡改已收录 star-fragments.yaml 抓出/越界改 .github/workflows 抓出/新增合规遭遇放行 ✓
- **lore.yml 第2步 schema+署名+禁术语**（临时 git 仓 + 真实 lore.schema.json）：冒名 contributor 抓出/故事含 PR·merge 术语抓出/weight=999 超 schema 上限抓出/合规投稿打勾 ✓
- labels.yml / lore-reward.yml 为纯 shell（无 python 段），逻辑已在上轮 `|| true` 咽喉断言覆盖，本轮目审复核：labels.yml 两条触发器分流正确（PR→meta 标签，push→幂等建标签）；lore-reward.yml 灵石奖励与名录两步入账链均无吞错 ✓

### 结论
- 清单三项之后的全部 9 条 workflow 链已逐一演练过至少一次，无新 bug。清单全清 + 六轮打磨零遗漏项，高频轮后续默认 SILENT，除非线上出现「重跑后仍 failure」的真红灯
- 本轮教训（工具层，非仓库 bug）：YAML 块标量提取的 python 段做 dry-run 时，`textwrap.dedent` 处理不了「首行顶格+后续行带共同前缀缩进」的混合形态（GitHub Actions run 块常态），需按非空行共同前缀手动剥除）

## 2026-10-14 22:0x 夜间轮：打磨第七轮（全流程演练全过，零修复）

### 线上巡检
- battle-log/39 四条 failure（04:25:53Z）重跑全部洗绿（completed skipped）——确认为已登记的「bot 入账 PR 附带 startup failure」平台噪音，非真红灯。「重跑后仍 failure」判定标准连续第三轮有效，当前线上零真红灯

### 演练结果（只读沙盒，真实灵籍未动，收尾工作树 CLEAN）
- 9 workflow YAML 语法 + `on` 字面键 + 3 册灵籍/7 篇遭遇 schema 全过
- battle hash 模拟（原样提取执行）：种子确定性/幂等/三回合分镜/模拟不改灵籍 全过
- explore 结算（原样提取执行）：种子确定性/五维产权不动/恶战保底（5→0 记 -5、100→90 记 -10）全过
- growth 校验语义（临时仓 8 场景）：合规 delta=1/3、篡改拒、越产权拒、超限 4>3 拒、余额 5<30 拒、新文件过 全过
- register 降世故事：3 行多行 origin + mystery 完整入正文（清单 1 回归）全过
- rebase 渡劫校验（沙盒 6 场景）：功力不足拒/灵石不足拒/渡劫成功（扣 50/境界+1）/天梯之顶拒/非法境界拒/筑基新门槛再拒 全过
- catalog 渲染字段断言 + REALM_CN 在位 全过

### 演练方法教训（非代码 bug，给后续轮提效）
- heredoc 提取段的「首行顶格+后续行缩进」混合形态：commonprefix 只按非空行算会漏剥首行——先按非空行求前缀，再逐行剥除（textwrap.dedent 不够用）
- 沙盒替换 workflow 注入占位符必须全量（steps.outputs 类占位符漏一个，seed 就变，遭遇选择假阴性）——本轮 explore 断言 FAIL 一次全是此因，非代码 bug
- 演练判定 refuse 与否要认准 `::error::` 走 stdout（print），stderr 里只有 gh 兜底评论的报错
- growth 演练的「余额不足拒」若在 PR 内改灵籍会被产权过滤器先拒——穷要穷在 base 上，PR 只追加修行行

## 2026-10-14 深夜轮：好玩路线图 T1-1「血脉之力」施工（v0.8）+ 斗法双触发竞态实锤修复

### 机制（硬边界先行）
- schema 新增 `bloodline{unlocked 0-5, wins>=0}`，bot 独占（schema 8 场景校验全过，旧灵籍无此字段向后兼容）
- 解锁公式：`unlocked = min(5, 境界段数(炼气0/筑基1/金丹2/元婴3/化神4/渡劫5/渡劫后5) + wins//2)`——境界节点与胜场双触发，正是路线图"想起自己是谁↔战力成长绑死"的本意
- 加成：每段 +1.5% 战力（上限 +7.5%，与灵性 ±5~10% 同量级不破平衡）；battle.yml `power()` 单测比值精确 1.07500，对局实测 320.1/297.7=×1.075，等弱对手 +7.5% 成功反超
- 双入账链：battle.yml（胜场累计+段数重算+解锁贴「🩸血脉之力·苏醒」）/ rebase.yml（渡劫后境界段数上涨→独立入账 PR，段数无变化跳过不空入账）——本地沙盒 4+3 场景全过
- e2e 四场实跑（issue #49/#51/#53/#55/#57）：燧鸣 1段→2段→胜场解锁链全通，PR50/52/58 账目正确；期间顺带实锤并修复三处 bug

### 🐛 本轮实锤修复
1. **入账段缺 `import json`**（本轮新代码引入）：沙盒执行当场 NameError，修于 push 前
2. **斗法双触发竞态**（现存 bug，非本轮引入）：issue body 与评论 1 秒内各起一个 run，同名 `battle-log/<n>` push 撞车红灯（#49/#51 两度复现）
   - 守卫 v1（待战标签，af02c81）：#53 实测标签时序不可靠，双 run 都在彼此打标前读到空
   - 守卫 v2（远端分支互斥锁，c5a0a1e）：#55 实测锁检查有 TOCTOU 窗口（守卫窗口 14s 早于对侧 push 26s），无法前移消除
   - 守卫 v3 终案（2cd156c）：push rejected 即互斥锁最后裁决——迟到者良性 exit 0（其重复结算弃用），真 push 故障仍显式红灯；#57 终验双 run 双绿、入账 PR 唯一
3. skill 已知坑修正：`/battle` 发 issue body 实际可触发（workflow 本就监听 issues.opened），原手册"必须补评论"表述过时

### 教训
- GitHub Actions 无原子锁可用时，「最终写入裁决」（push/创建冲突即退让）比「前置检查」可靠——前置检查的窗口永远存在
- heredoc 无引号 EOF 段内加代码，import 清单要重看一眼（本轮 json 就是漏网之鱼）
- e2e 不能只验 happy path：本场五连测里 4 场是靠"故意双触发"把竞态逼出来的

## 2026-10-14 19:4x 夜间轮：打磨第九轮——T2-1 记忆碎片 + T1-3 斗法志回放（窗口内新代码全演练，零修复）

### 背景
- 窗口内主会话落两大块：0537d17（T2-1 记忆碎片：schema+rebase.yml 同步揭示+觉醒判定）与 cc61dcd（T1-3 斗法志回放页）。按⑧对新逻辑演练，worktree 隔离。

### 演练结果（全过，零新 bug）
- **T2-1 碎片同步**（rebase.yml 结算段原样提取，沙盒 4 场景）：
  - wins=2 渡劫后（zhuji，new=2）：第 2 段揭示为【待补·第2段…】、第 3 段仍【封印】、bloodline/mf 计数一致、schema 过 ✓
  - **旧灵籍无 memory_fragments 字段**（向后兼容）：自动生成五段册、已揭示段计入、schema 过 ✓
  - 集齐 5 段（dujie）：5 段全揭示零封印残留、AWAKEN 判定触发 ✓
  - 无变化：NONE 跳过不空入账 ✓
- **3 册真实灵籍**：schema 全过（含新 memory_fragments additionalProperties:false）；bloodline.unlocked 与 mf.unlocked 交叉一致（1/0/0）、封印数 4/5/5 ✓
- **T1-3 回放链**：catalog.yml python 段原样提取 compile 过；build-chronicle-index.py 实跑 8 场、file 路径全真实存在、实跑后工作树 CLEAN（生成器幂等）✓；battle-chronicle.html 与 chronicle-index.json 字段契约断言通过（html 引用的 item 字段 ⊆ 索引字段）✓；catalog.yml 段内无 chronicle 引用——斗法志页与图鉴页数据链独立，回放页索引由 bot 在斗法入账后跑生成器刷新，链路成立 ✓

### 过程教训（复训）
- worktree 开工即撞主会话并发 push（pull 后 HEAD 从 0537d17 跳 cc61dcd）——「演练基线可能过期」第 N 次应验，worktree + 收尾 fetch --ff-only 复核有效
- GitHub Actions run 块 python 段提取：`\nPYEOF` 全文首查会命中后续 heredoc，必须按行号配对扫描（start 行下一个顶格 PYEOF）
- 本地实跑 build-chronicle-index.py 属安全幂等（输出与已提交版本逐字节一致，git status CLEAN 验证）——对生成器类脚本，实跑+CLEAN 断言是最强校验

## 2026-10-14 20:0x 夜间轮：好玩路线图 T1-2「天赋技能扩展」施工（v0.10）

### 交付
- **schema 硬边界先行**（beast.schema.json）：talent.kind 扩为 6 类（+control/summon）；新增 talent.mastery（0-999，bot 独占写入，禁玩家 PR 改），旧灵籍无字段兼容（.get 默认 0）
- **觉醒四级**（battle.yml AWAKEN 表）：mastery 0-2/3-7/8-14/15+ → Lv0-3；触发率 30/35/40/45%；burst 1.6→1.9x、shield 减伤 0.5→0.3、drain 吸血 0.4→0.55、counter 反弹 0.5→0.7 随级强化
- **control 封招**：命中则对方该回合力度减半（伤害结算前生效，攻守两侧皆有语义）
- **summon 残影协战**：攻方命中 +25 固定追伤（守方无语义不触发）
- **熟练度入账**：battle.yml 结算段每触发 +1（胜负无关），觉醒瞬间在 issue 贴「✨ 天赋 · 觉醒」播报（只升贴一次不刷屏）
- **本地沙盒演练全过**：sim 段原样提取真跑（control/summon 触发断言、mastery 计数一致断言、旧籍无 mastery 兼容断言、schema 3 真实灵籍+2 新 kind 样本+非法 kind 反例全过、旧 4 类 Lv0 回归=数值与 v0.8 语义一致）
- **e2e 实测**（issue#59 燧鸣 vs 墨霄）：battle run success，燧鸣 R1 burst 触发 ✨、mastery=1 入账（commit d19b2ee）、墨霄 shield 未触发 mastery 正确保 0、灵性结算正常

### 顺带修正的隐性 bug（施工中实锤）
1. **守方侧无语义 kind 空触发**：v0.8 起 trig_def 对 burst/drain 兽命中时事件为 None 但不报错（无感知）；mastery 要入账后计数与画面不符（实测 3 vs 1）。修正=触发判定绑定语义侧：burst/drain/summon 仅攻方判定、shield/counter 仅守方判定、control 双侧——**触发必须可见于画面**
2. **talent 事件单槽互相覆盖**：一回合攻守双方天赋都触发时旧代码单变量覆盖丢事件；改攻守双事件槽（talent/talent_def），bot 分镜行可同时显示两侧 ✨

### 观察项（非本轮引入，未修）
- growth/labels/register/lore 四 workflow 在 bot 建的 battle-log PR 上 100% failure（近 100 次 0 成功，"workflow file issue" + 0 jobs，入账 PR 均已正常合并不受影响）——疑似 GitHub 对 bot PR 递归触发的抑制，留待专轮排查

### 过程教训
- workflow 内嵌 python 改动，沙盒提取时 `${{ steps.parse.outputs.* }}` 表达式必须一并替换（漏一个就 FileNotFoundError）
- 单事件槽变量在「一回合双触发」场景是隐性地雷：新机制要入账时，先画清"一回合最多几个事件、各归谁"
- e2e 后本地 diff 突然 clean = 并发 cron 刚提交——收尾 commit 前必须 git log 复核工作树归属，确认并发提交没夹带自己文件

## 2026-10-14 20:1x 夜间轮：bot-PR startup failure 独立复核（零修复，两条新证据）

### 巡检
- 线上全部 30 条 failure 复盘完毕：**全部**是已登记的 bot 入账 PR 四链 startup failure（7 批：battle-log/43~59 + 更早 explore-log/lore-reward/rebase-log），无新真红灯；PR#60 批次（#59 斗法 e2e）4 条重跑全部洗绿（completed skipped）。GitHub status 全程 operational，排除平台故障窗口
- 结论与 12:2x 登记一致，**建议①（job if 过滤 head 分支）可以不用再实验**：见下证据 1

### 新证据（本轮 API 实查所得）
1. **失败仅绑定 create→merge 高速窗口，且可事后求值**：对 PR#60 已合并后的 head sha 重跑，4 个 run 全部正常进入 job 求值并 skip（0 失败）——说明 startup 层只在 PR 存活的 ~2 秒窗口内排队时被打断；重跑（无论 actor 是谁）都能正常走完。12:2x 留验的「job if 能否挡住」不再需要验证：正确姿势就是**合并后批量重跑洗绿**或接受噪音
2. **僵尸 check-suite 隐患**：被污染的 head sha（如 d19b2ee）上残留 5 个永久 `status=queued` 的 check-suite（重跑后新 suite 正常完成，旧 suite 永不结算）——该 sha 的 combined commit status 因此永远 `pending`。当前无 branch protection 无影响；**未来若开 required status checks，这些僵尸会把历史 sha 永久卡在 pending**，届时需 API 手动补创建 check-run 或放弃对 bot 分支 sha 的检查

### 处置
- 维持 12:2x 的方案②（容忍噪音 + 「重跑后仍 failure」为真红灯判定标准），本轮未改任何 workflow 文件
