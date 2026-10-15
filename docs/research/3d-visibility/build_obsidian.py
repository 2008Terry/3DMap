"""Build a new, self-contained Obsidian research collection from verified records."""
from pathlib import Path
from collections import Counter, defaultdict
import json
import re
import yaml

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "obsidian" / "3D结构透视研究"
BASE = "3D结构透视研究"
DATE = "2026-10-15"
datasets = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(ROOT.glob("*sources.json"))]
sources = [s for d in datasets for s in d["sources"]]
byid = {s["id"]: s for s in sources}
families = json.loads((ROOT / "method-families.json").read_text(encoding="utf-8"))
assert len(byid) == len(sources)
assert len({s["url"].rstrip("/") for s in sources}) == len(sources)
assert all(i in byid for f in families for i in f["source_ids"])

def clean(text, limit=68):
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "-", text).rstrip(" .")[:limit].rstrip(" .")

source_paths = {s["id"]: f'来源/{s["id"]} {clean(s["title"])}' for s in sources}
family_paths = {f["id"]: f'方法/{f["id"]} {f["title"]}' for f in families}

def link(path, label=None):
    return f"[[{BASE}/{path}|{label or path.split('/')[-1]}]]"

def S(i):
    s = byid[i]
    return link(source_paths[i], f'{i} · {s["title"]} ({s["year"] or "未核实年份"})')

def F(i):
    return link(family_paths[i], next(f["title"] for f in families if f["id"] == i))

def page(path, title, body, properties=None):
    p = OUT / f"{path}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    fm = {"type": "research-note", "created": DATE, "updated": DATE, "status": "文献研究，未本地复现"}
    fm.update(properties or {})
    # Obsidian table cells need escaped alias pipes inside wikilinks.
    body = "\n".join(re.sub(r"\[\[[^\]]+\]\]", lambda m: m.group(0).replace("|", r"\|"), line)
                     if line.startswith("|") else line for line in body.splitlines())
    p.write_text("---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False).rstrip() + "\n---\n\n# " + title + "\n\n" + body.strip() + "\n", encoding="utf-8")

home = link("00 3D结构透视研究 Dashboard", "研究 Dashboard")
evidence_names = {"full-primary": "全文级原始资料", "abstract-primary": "原始摘要或受限索引", "official-doc": "官方文档"}
for s in sources:
    method_refs = [F(f["id"]) for f in families if s["id"] in f["source_ids"]]
    related = [S(i) for i in s.get("related_ids", []) if i in byid and i != s["id"]]
    body = f'返回 {home} · {link("03 来源索引", "来源索引")}\n\n[原始来源]({s["url"]})\n\n作者/机构：{s["authors_or_org"]}。年份：{s["year"] if s["year"] else "未核实，见来源核对说明"}。证据层级：{evidence_names[s["evidence_status"]]}。'
    labels = [
        ("mechanism_zh", "机制"), ("visible_information_zh", "能够显露的信息"),
        ("geometry_effect_zh", "几何与坐标"), ("tradeoffs_zh", "代价"),
        ("evaluation_zh", "评价证据"), ("interaction_zh", "交互"),
        ("implementation_zh", "实现与数据要求"), ("verified_claim_zh", "来源核对"),
        ("limitations_zh", "限制")
    ]
    for key, heading in labels:
        value = s.get(key)
        if value:
            body += f"\n\n## {heading}\n\n{value}"
    body += "\n\n## 方法与关联\n\n" + (" · ".join(method_refs) or "见来源索引")
    if related:
        body += "\n\n" + "\n".join("- " + r for r in related)
    page(source_paths[s["id"]], s["title"], body, {
        "type": "research-source", "id": s["id"], "year": s["year"],
        "source_type": s["source_type"], "evidence": s["evidence_status"],
        "methods": s["methods"], "domains": s["domains"], "source_url": s["url"],
        "accessed": DATE, "method_families": [f["id"] for f in families if s["id"] in f["source_ids"]]
    })

for f in families:
    body = f"返回 {home} · {link('02 方法对照矩阵', '方法对照矩阵')}\n\n"
    for key, heading in [("mechanism", "如何显露"), ("visible", "能读什么"), ("tradeoffs", "牺牲什么"),
                         ("geometry", "保留什么"), ("implementation", "需要什么"), ("claim", "证据边界")]:
        body += f"## {heading}\n\n{f[key]}\n\n"
    body += "## 原始资料\n\n" + "\n".join("- " + S(i) for i in f["source_ids"])
    page(family_paths[f["id"]], f["title"], body, {"type": "research-method", "method_id": f["id"]})

counts = Counter(s["evidence_status"] for s in sources)
recent = sorted([s for s in sources if s["year"] and s["year"] >= 2023 and s["source_type"] != "official-doc"],
                key=lambda s: (-s["year"], s["id"]))
dashboard = f"""
你的目标是让内部结构像展开在眼前一样可检查，而不是仅让外壳变淡。本库先研究怎样显露、怎样读懂，以及需要改变什么；尚未按现有技术栈筛选，也没有开始下一轮应用实现。

截至{DATE}收录 **{len(sources)}条去重原始来源**：{counts['full-primary']}条全文级、{counts['abstract-primary']}条摘要或受限索引、{counts['official-doc']}条官方文档。其中{len(recent)}条为2023–2026年的研究论文/综述。官方页面更新年与论文发表年分别解释；访问日期不是发表日期。

## 先读这四项

- {link("01 核心问题与研究结论", "结论：为什么单纯半透明不够，哪些路线更接近高维观看")}
- {link("02 方法对照矩阵", "16类方法：显露方式、原位保真与代价")}
- {link("05 可组合方案与研究假设", "五种大胆方案与组合方式；均未验证为产品实现")}
- {link("06 评价任务与验收标准", "怎样证明看清了，而不只证明画出来了")}

## 参考数据库

- {link("03 来源索引", "全部83条来源，逐条机制、证据和限制")}
- {link("04 近期研究 2023–2026", "近期研究与真实日期")}
- {link("07 检索记录与覆盖缺口", "检索路径、访问失败和没有证据的地方")}
- {link("08 阅读路线与术语", "按目标选阅读路线")}
- {link("来源数据库.base", "可筛选的原生 Bases 表")}

![[{BASE}/来源数据库.base]]

## 方法分类

""" + "\n".join("- " + F(f["id"]) for f in families) + """

## 使用边界

全文级意味着本轮读取了原始正文，不意味着独立复现；摘要级只支持明确可核实的范围。偏好、信心、速度、准确率、PSNR和可见率分开记录。具体建筑没有内部数据时，显示算法无法确认真实墙门位置。

这是一轮跨领域方法覆盖与代表性资料调查，不能宣称互联网所有相关论文已经穷尽。当前缺口与下一步入口见检索记录。所有新笔记位于独立目录，不覆盖既有笔记。
"""
page("00 3D结构透视研究 Dashboard", "3D结构透视研究 Dashboard", dashboard, {"type": "research-dashboard"})

conclusion = f"""
返回 {home}

## 对当前问题的直接回答

以前的讨论已经把遮挡、投影和信息密度列为核心问题，也提出了空间爆炸、局部X-ray、剥壳、深度扫描和空间折叠。上一轮应用主要修透明混合并强调当前层，不能视为这些思路的完整实现。本轮把问题重新放在跨领域的三维内部可视化上。

最接近你设想的并不是一种更通透的材质，而是**为内部结构重新分配可见空间**：删除挡住目标的区域，把部件移开或铺平，给不同区域分配不同观看射线，或者让几何、平面图和连通图共同承担信息。透明、轮廓和深度符号是这些方案的组成部分。

这属于研究综合判断，不是已经完成本项目验证的结论。基准入口为{S('cross-01')}，其2008期刊综述梳理50种遮挡管理方法；2007会议版为25种。

## “四维看三维”的类比，有价值的部分是什么

想象二维世界中的角色被一个闭合轮廓困住，三维观察者可以从平面外看其内部。这个比喻准确指出：沿原来维度内移动视点，和从新的观察通道显露结构，不是同一件事。

软件中可以模拟这类效果，例如弯折观看射线绕过墙角、将不同房间安排到不同画面区域、把楼层和墙体打开。{S('proj-02')}及{S('proj-06')}直接研究把普通相机无法同时看到的区域组合到一张图里。

但模拟出的图最终仍要落到有限二维像素上。普通透视/正投影把同一射线上的多个深度映到同一位置，透明只能混合它们的贡献。允许改变投影、位置、窗口或时间，可以解除特定遮挡；这不自动保证任意复杂模型的所有表面、所有连接和真实距离同屏都清楚。本库没有把这种界限写成已经完成严格数学证明的“不可能性定理”。

## 先区分四层问题

| 层次 | 要回答的问题 | 典型资料 |
|---|---|---|
| 数据存在 | 我们真的知道里面是什么吗？ | 图纸、BIM、实体成像；{F('15')}与{F('16')} |
| 渲染正确 | 透明顺序、深度、裁剪是否算对？ | {F('01')} |
| 结构可见 | 被遮挡的目标能否获得屏幕面积？ | {F('03')}、{F('05')}、{F('07')} |
| 人能理解 | 能否认出层序、邻接、路径和原位？ | {F('11')}、{F('13')} |

物理成像获得未知数据；透明/裁剪处理已有数据；生成补全提出假设。三者不能混称“透视”。

## 为什么全模型半透明经常失败

在前向alpha合成中，多层贡献会逐渐累积。若每层不透明度都是0.2，10层累计约0.893。它说明为何每层看似淡、叠起来仍密；并非对当前白屏故障的独立诊断。即使合成完全正确，墙、楼板和家具颜色也会混到一起。

{S('cross-09')}讨论OIT的正确性与资源取舍；{S('cross-05')}说明颜色和透明度交互影响层序判断。修混合错误只完成了第二层问题，不能代替第三、第四层。

## 最有价值的三条路线

**原位显露**：目标保持原位，挡住目标的外壳局部切掉，剩余上下文变成轮廓或ghosting。适合回答“这个东西在楼内哪里”。代价是当前画面看不到被切部分。见{F('03')}、{F('04')}。

**空间重排**：楼层、翼、墙片或系统像装配件一样展开，保存每个部件回原位的对应。适合回答“每层有什么，如何组成整体”。代价是真实距离、接触或形状。见{F('05')}、{F('06')}、{F('08')}。

**观看重排**：Graph Camera或局部多透视把绕墙角的视线拼成一个画面；联动图册和拓扑图让每个空间有明确位置。适合完整检索与连接理解。代价是统一投影或单一画面。见{F('07')}、{F('09')}、{F('11')}。

## 可以确认的证据，以及不能推广的地方

- {S('proj-06')}有47名参与者；所测迷宫中搜索平均快约28%，计数约91%对42%，方位任务相近。它证明值得认真探索多透视，不保证任意建筑的全部全局关系都易懂。
- {S('cross-05')}主实验192人，但对象为重叠圆盘。其80.72%为预测模型指标，不是建筑理解准确率。
- {S('med-17')}含2名外科医生及20位潜在供体，主要测信心；交互参数有收益，双眼3D相对2D未见显著差异。
- {S('proj-09')}为2026预印本，28人研究立面时间数据；相对另一x-ray条件没有明确时间差异，不能冒充楼内几何全显示方法。

这些证据支持按任务组合方法，不支持一招解决所有尺度、结构和观看条件。

## 对3DMap的研究含义

建筑内部需要准确的层、房间、门、楼梯、电梯及系统连接，单靠漂亮外立面无法验证室内。来源应分为测得/官方资料、可信近似、示意与生成假设。先建立结构语义与原位对应，再研究自动显露，才有办法验证覆盖率和关系正确性。

具体方案推演见{link('05 可组合方案与研究假设', '五种组合方案')}；这是下一步原型的候选集，不是本轮已经实现的功能清单。
"""
page("01 核心问题与研究结论", "核心问题与研究结论", conclusion)

shorts = [
("透明贡献、选择性淡化","保位置和投影","混色、层序；未保证全可辨"),
("隐藏边、光晕、ghosting","保位置","线条拥挤，交叉语义不清"),
("删除遮挡区域","保目标原位","被切部分缺失"),
("局部窗口或排斥场","保焦点对应","窗口外仍隐藏；部分变形"),
("部件/楼层移开","通常保部件形状","失去真实接触和距离"),
("开门、翻页、剥皮","保可追溯对应","可能改形状、曲率和距离"),
("重新分配射线和投影","可保世界几何","屏幕布局非统一相机"),
("沿曲线/薄层铺平","保特定内在关系","不保全部角度/距离"),
("多个方向/楼层面板","各自投影可保真","屏幕面积和跨视图对应"),
("随时间逐层访问","可保原几何","非同时可见、记忆负担"),
("图、层级与几何联动","保显式连接","抽象丢失形状与距离"),
("自动选择切口/布局/相机","依约束定义","代理目标未必等于理解"),
("任务、感知、错误实测","定义验证标准","结果不能跨任务乱用"),
("增加双眼/角向通道","可保几何","设备要求且仍有遮挡"),
("物理测量和反演","真实数据依测量","材料、尺度、信号限制"),
("先验生成缺失结构","产生候选假设","不保证真实内部")
]
matrix = f"返回 {home}\n\n这些族会组合，不是互斥产品模式。保形状、保原位、保拓扑、保度量、保单投影是不同要求。\n\n| 方法 | 显露机制 | 保留什么 | 主要代价 |\n|---|---|---|---|\n"
for f, row in zip(families, shorts):
    matrix += "| " + F(f["id"]) + " | " + " | ".join(row) + " |\n"
matrix += f"""
## 按你要看清的东西选择

| 目标 | 优先考虑 | 需要防止的误读 |
|---|---|---|
| 一个内部目标在哪里 | 局部剖切 + ghosting + 深度符号 | 目标像浮在外壳上 |
| 每层全部房间有哪些 | 楼层图册 + 可展开层 + 联动3D | 图册缺层、缩小后漏读 |
| 门/楼梯如何连接 | 语义连通图 + 平面图 + 三维高亮 | 投影交叉当成真实连接 |
| 内部构件完整表面 | 层级爆炸 + 局部开合 | 展开距离被当成真实距离 |
| 绕墙角的连续空间 | Graph Camera/多透视 | 屏幕方向与世界方向混淆 |
| 连续弯曲管腔/薄层 | CPR、解缠或展开 | 平面距离当成原空间距离 |
| 未知实体内部 | 合适物理成像 + 不确定度 | 把生成猜测当测量 |

本矩阵为文献综合，具体效果需{link('06 评价任务与验收标准', '任务验证')}。
"""
page("02 方法对照矩阵", "方法对照矩阵", matrix)

index = f"返回 {home}\n\n每项链接进入独立来源笔记，包含机制、几何、数据要求、评价与访问限制。共{len(sources)}条；同URL无重复。标题相近但不同研究单列，会议/期刊同一研究的重复版本尽量合并。\n\n"
for d in datasets:
    index += "## " + d["domain"] + "\n\n"
    for s in d["sources"]:
        index += f'- {S(s["id"])} · {evidence_names[s["evidence_status"]]}\n'
    index += "\n"
page("03 来源索引", "来源索引", index)

recent_body = f"返回 {home}\n\n这里单列2023–2026研究论文与综述，共{len(recent)}条。较老论文保留在方法页，作为机制来源。官方页面更新时间不算新论文；预印本与已发表资料以各来源说明为准。\n\n"
for y in range(2026, 2022, -1):
    recent_body += f"## {y}\n\n"
    for s in recent:
        if s["year"] == y:
            recent_body += f'- {S(s["id"])} · {evidence_names[s["evidence_status"]]}。{s["verified_claim_zh"]}\n'
    recent_body += "\n"
page("04 近期研究 2023–2026", "近期研究 2023–2026", recent_body)

brainstorm = f"""
返回 {home}

这些是基于文献的组合假设，尚未建原型或用3DMap验证；先不按当前引擎能力淘汰。共同前提是内部模型足够可靠，且每个房间、门、墙片和连接有稳定ID。

## A. 结构图册：完整检索的基线

同屏放可缩放楼层小图、中央三维结构及楼梯/电梯连通图。点任何房间，其他视图定位同一对象；选择一条竖向连接时，所有相关楼层同步显露。全楼概览可收起家具，只保墙、门、走廊和核心筒。

它最直接满足“所有空间可清点、所有连接可追踪”，但不声称所有墙面同时在三维里无遮挡。候选依据：{F('09')}、{F('11')}、{S('proj-17')}。验收重点为缺层/漏房间、假连接与跨视图定位错误。

## B. 多透视空间：在一张图里绕过墙角

以房间/走廊门户为图，让观看射线向相邻空间分叉或弯折；局部先展示一两个拐角，另有覆盖全翼的模式。地面、门框和边界颜色提示视线何处发生转向，点击后能回到普通原位视图。

这是最直接回应高维观看比喻的激进路线。世界几何可保留，画面统一透视会改变；不该把屏幕上直连的区域当成真实直线。依据{S('proj-02')}、{S('proj-06')}、{F('07')}。验收需同时测检索和方位，不能只看多显示了多少。

## C. 建筑开合：楼层拉开，墙片向外翻

楼层如手风琴展开，外墙和部分隔墙像铰链门翻开，核心筒用连接线保留楼层关系。选中某层时局部再展开；模型过高时按总展开范围自动构图，不把层挤到屏幕外。任意展开件都可动画回原位。

这能让内部获得真实屏幕面积，远强于统一alpha。代价是展开态距离与接触失真，铰链还需明确显示是示意操作。依据{F('05')}、{F('06')}、{S('tech-16')}。验收看完整形状可辨、原位回忆、连接不丢失。

## D. 原位结构透镜：自动切壁，保留外壳参照

选择房间、路径或结构系统后，求出视点前必要的遮挡区域并切掉；外壳剩余部分以淡轮廓保留。楼板保留厚度和切边，目标用清楚的遮挡/深度符号避免浮在外面。透明作为局部过渡，不承担整楼全部显露。

适合定位和保留原始空间，但单个焦点不会让所有对象同时出现。依据{F('03')}、{F('04')}、{F('02')}。验收看目标原位、前后/内外判断、切口稳定性。

## E. 系统展开：按连接摊开而非按外观堆叠

楼层、房间、楼梯、电梯、管线系统各有语义层级；展开以邻接和包含为约束，而非把所有部件均匀推远。对弯曲连续结构使用沿路径展开，对薄墙/薄层用表面图册，对房间网用连通图。

它偏向“所有关系能读清”，不会强行把整栋体积套进一张无失真平面。依据{F('08')}、{F('11')}、{F('12')}。验收看图与几何的一致性、哪些度量仍有效，以及展开是否制造假邻接。

## 组合方向

值得比较的是A作为完整检索参照，B/C作为增加同屏显露的实验，D提供原位核对，E负责关系和系统。任何模式都保存同一个结构身份，避免切换后像在看不同建筑。

这是研究建议，不是为了增加五个新的按钮。下一轮可以固定同一栋楼、同一组任务，比较少数候选；在结果出来前不宣称其中某个方案已经最优。

## 数据层先明确

公开的真实楼层图、可靠BIM或实测内部为高可信来源；按楼高估层、通用房间模板和生成补全应明确标近似或示意。真实Burton层数、夹层/地下层定义、Hatcher翼之间的连接都应单独有来源。视觉通透无法补救这些数据错误。
"""
page("05 可组合方案与研究假设", "可组合方案与研究假设", brainstorm)

evaluation = f"""
返回 {home}

## 五个独立成功标准

1. **可访问覆盖**：真实清单中的每层、房间、门和竖向连接都有能到达的视图；自动记录漏项，不只看截图。
2. **可辨识**：用户能正确数房间、找门、区分隔墙和家具；屏幕中出现一个像素不算看清。
3. **关系正确**：能回答哪些空间相邻/相通、楼梯连接哪层、谁在前、谁包住谁。
4. **原位可追溯**：从展开或多透视状态回到原建筑，仍能指出对应位置；屏幕距离不冒充真实距离。
5. **实际可操作**：任务正确率、时间、误操作与舒适度可接受；帧率、偏好和信心另列。

依据{F('13')}。这些是研究设计，尚未执行用户实验。

## 一组适合建筑的具体题目

| 题目 | 主要测量 | 常见失败 |
|---|---|---|
| 找出指定楼层所有房间并数门 | 漏检/误检、耗时 | 透明重叠、图册太小 |
| 从入口到高层房间指出所有连接 | 路线正确率、漏楼梯 | 图有假连边、层对应不明 |
| 比较上下两层同位置空间 | 跨层定位误差 | 拆层后位置错认 |
| 指定墙后目标相对外立面的位置 | 内外/前后判断、位置误差 | 目标看起来漂浮在表面 |
| 展开后指出某房间原位置 | 回忆误差、恢复耗时 | 爆炸或投影割裂对应 |
| 检查闭环走廊、双翼、夹层和核心筒 | 覆盖、重复对象、关系错误 | 多透视重复/遗漏、拓扑被压扁 |

## 画面和数据核对

先建立真实对象清单及关系真值，再记每对象的有效可见面积、被挡比例和是否能选中。可见率只能做算法指标，要与人工辨识题分开。

固定屏幕大小、缩放和数据，分别比较普通剖切、图册、多透视、展开和组合。交互与立体硬件不能在同一比较里一起变化后全部归因给某一种渲染。先做少量形成性测试找错误，再决定是否开展较大实验；不凭先导样本声称普遍有效。

场景应包括密集隔墙、封闭房间、环形通道、共享墙、重复家具、极高多层、曲面与分叉，以及不完整/示意数据。保留失败截图与解释，避免只发布最清楚的角度。

## 不把这些当作充分证据

- 手势/键盘功能72项通过，只说明操作逻辑，不说明内部可读。
- 高FPS或PSNR，只说明性能/图像相似度。
- 用户更喜欢或更有信心，不等于结构判断更准确。
- 显示所有对象ID，不等于每个对象有足够屏幕面积。
- 某个系统叫occlusion-free，不代表任意对象无条件全部无挡。
"""
page("06 评价任务与验收标准", "评价任务与验收标准", evaluation)

log = f"""
返回 {home}

检索日期：{DATE}。原始提取记录保存在项目docs/research/3d-visibility的四份sources.json中；这里记录可读检索入口与边界。

## 检索方法

从{S('cross-01')}和{S('proj-19')}出发追踪方法名、作者论文与后续研究，再补充2023–2026的原始论文、官方工具文档、物理成像和生成补全。只把作者/机构、出版社、官方文档或代码仓库作为结论依据。搜索引擎和二手聚合仅作为发现入口。

“全量”落实为跨方法族覆盖、来源分层、反例与缺口记录，不把搜索结果数量当穷尽文献证明。尚未对所有50种经典分类逐篇精读，尤其路径规划、虚拟镜面及若干历史子方法只在综述范围内触及。

## 方法覆盖

| 方法族 | 本轮入口数量 | 覆盖状态 |
|---|---:|---|
"""
for f in families:
    log += f"| {F(f['id'])} | {len(f['source_ids'])} | 有代表性原始来源；各项访问与局限见来源卡 |\n"
log += "\n同一来源可以支持多个方法族，以上不能相加为来源总数。\n\n"
for d in datasets:
    log += "## " + d["domain"] + "\n\n### 查询记录\n\n"
    log += "\n".join("- " + str(q) for q in d.get("queries", []))
    log += "\n\n### 本分支覆盖缺口\n\n"
    log += "\n".join("- " + str(g) for g in d.get("coverage_gaps", []))
    log += "\n\n"
log += """
## 统一的未解决问题

- 尚未找到并验证普通单屏对任意多层建筑、全部结构同时可辨、位置和度量均保真的通用方案。
- 需要更深入追踪分子/细胞近期研究、神经纤维束、虚拟内窥镜、自动全覆盖视点、镜面/门户显示、图布局、共享墙与非流形拓扑展开，以及不确定性可视化。
- 物理成像只覆盖机制与代表性实例，未比较完整设备谱系、所有尺度/材料和采集成本。
- 没有本项目的GPU复现、模型覆盖审计或正式用户任务实验。本轮结果是文献与方案数据库。
- 某些全文因403、超时、体积过大、验证码或订阅不可达。笔记保守标摘要级，具体样本和公式未经核实的不补写。
- 学术网页、在线文档和预印本会变化；版本/日期说明保留在每张来源卡，未来更新时应重新核对。

文件结构与链接通过程序核验不等于已在Obsidian完成视觉渲染检查，也不等于Dropbox已完成同步。
"""
page("07 检索记录与覆盖缺口", "检索记录与覆盖缺口", log)

reading = f"""
返回 {home}

## 最短阅读路线

先读{S('cross-01')}理解遮挡管理空间，再读{S('proj-06')}了解多透视的实证，接着看{S('tech-02')}的层级拆解与{S('med-05')}的原位局部显露。最后用{S('cross-05')}和{S('cross-06')}校正“画出来就看懂”的直觉。

如果关注完整楼层和连接，直接读{F('09')}、{F('11')}；关注像高维一样绕过遮挡，读{F('07')}、{F('05')}、{F('08')}；关注未知内部怎么获得，读{F('15')}、{F('16')}。

## 容易混淆的术语

| 术语 | 本库含义 | 不应自动等同 |
|---|---|---|
| X-ray / ghosting | 虚拟淡化、隐藏或局部穿视表达 | 实体X射线采集 |
| OIT | 不依赖提交顺序的透明合成方法族 | 所有层人眼可读 |
| depth peeling | 提取有序表面片元的渲染技术 | 用户逐层理解全部体积 |
| opacity peeling | 按累计不透明贡献等规则探索体层 | 固定物理楼层 |
| cutaway | 显示性切掉遮挡区域 | 完整外壳仍可见 |
| exploded view | 部件位姿被展开 | 真实空间距离 |
| unfolding | 特定表面/薄层/拓扑的展开 | 任意三维体积无损铺平 |
| multiperspective | 一张图组合多个观看射线结构 | 一个真实普通相机 |
| occlusion-free | 针对给定目标和约束的显露 | 任意复杂场景无条件全可读 |
| 4D | 可能指3D加时间、射线参数或组成变量 | 四维观察者已实现 |
| all visible | 每个目标获得某种视觉贡献 | all legible / all relationships understood |
| reconstruction / completion | 测量反演 / 先验推断 | 两者具有相同真实性 |

## 继续阅读时记录什么

记录目标结构、所需数据、是否原位、改变哪些不变量、哪些对象没有显示、任务和样本、失败案例，以及证据是否全文。每个新结论至少链接一条原始资料；生成或示意内容始终标状态。
"""
page("08 阅读路线与术语", "阅读路线与术语", reading)

base = {
    "filters": {"and": [f'file.inFolder("{BASE}/来源")', 'file.ext == "md"']},
    "properties": {
        "file.name": {"displayName": "来源"},
        "note.year": {"displayName": "年份"},
        "note.evidence": {"displayName": "证据层级"},
        "note.source_type": {"displayName": "资料类型"},
        "note.domains": {"displayName": "领域"},
        "note.methods": {"displayName": "方法"},
        "note.source_url": {"displayName": "原始链接"}
    },
    "views": [
        {"type": "table", "name": "全部来源", "order": ["file.name", "note.year", "note.evidence", "note.domains", "note.methods", "note.source_url"]},
        {"type": "table", "name": "2023–2026研究", "filters": {"and": ["note.year >= 2023", 'note.source_type != "official-doc"']},
         "order": ["file.name", "note.year", "note.evidence", "note.source_url"]},
        {"type": "table", "name": "全文级", "filters": 'note.evidence == "full-primary"',
         "order": ["file.name", "note.year", "note.domains", "note.source_url"]},
        {"type": "table", "name": "待取得全文", "filters": 'note.evidence == "abstract-primary"',
         "order": ["file.name", "note.year", "note.source_url"]}
    ]
}
(OUT / "来源数据库.base").write_text(yaml.safe_dump(base, allow_unicode=True, sort_keys=False), encoding="utf-8")
manifest = {
    "date": DATE, "vault_folder": BASE, "sources": len(sources), "evidence_counts": dict(counts),
    "recent_research_2023_2026": len(recent), "method_families": len(families),
    "markdown_notes": len(list(OUT.rglob("*.md"))), "files": len(list(p for p in OUT.rglob("*") if p.is_file())),
    "source_files": source_paths, "status": "research-only; no application changes or local prototype validation"
}
(ROOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: v for k, v in manifest.items() if k != "source_files"}, ensure_ascii=False, indent=2))
