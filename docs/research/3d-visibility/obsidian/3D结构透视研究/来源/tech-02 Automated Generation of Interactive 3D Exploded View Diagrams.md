---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: tech-02
year: 2008
source_type: paper
evidence: full-primary
methods:
- explosion graph
- hierarchical explosion
- contextual cutaway plus explosion
- riffling
domains:
- mechanical assembly
- anatomy
- technical illustration
source_url: https://grail.cs.washington.edu/wp-content/uploads/2015/08/li2008ago.pdf
accessed: '2026-10-15'
method_families:
- '05'
- '06'
- '11'
---

# Automated Generation of Interactive 3D Exploded View Diagrams

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://grail.cs.washington.edu/wp-content/uploads/2015/08/li2008ago.pdf)

作者/机构：Wilmot Li, Maneesh Agrawala, Brian Curless, David Salesin。年份：2008。证据层级：全文级原始资料。

## 机制

自动计算接触、阻挡、包含关系，构建有向无环爆炸图；外层先移开，再沿允许方向展开内层。按目标只移动必要部件，也可把局部装配从上下文切口中拉出。

## 能够显露的信息

多个部件的完整形状、装配顺序、相互阻挡与子装配层次；展开与合拢动画帮助把新位置对应回原位置。

## 几何与坐标

通常刚体平移，必要时把容器切为两半；对象形状多数保留，空间布置改变。

## 代价

展开状态失去真实距离和接触，偏移过大会削弱整体关系；全部展开可能制造新的杂乱。

## 评价证据

全文展示涡轮、iPod、手臂等模型及计算结果；作者指出约50个部件的示例能力，不是大规模理解实验。

## 交互

整图展开/收拢、拖动单部件、悬停riffling、按列表选目标；动画遵守图的阻挡顺序。

## 实现与数据要求

需独立实体部件；按26个视向预计算爆炸图以减轻交互延迟。

## 来源核对

已打开作者7页PDF并核对算法、交互、结果和限制。

## 限制

真实螺纹需要旋转，不能仅靠该线性移动算法拆开；噪声接触法线、相互穿插及高部件数会导致错误阻挡或成本增加。

## 方法与关联

[[3D结构透视研究/方法/05 层级、紧凑与多透视爆炸图|层级、紧凑与多透视爆炸图]] · [[3D结构透视研究/方法/06 剥皮、铰链、翻页与非刚性变形|剥皮、铰链、翻页与非刚性变形]] · [[3D结构透视研究/方法/11 拓扑、语义与几何的混合表达|拓扑、语义与几何的混合表达]]

- [[3D结构透视研究/来源/tech-01 Interactive Cutaway Illustrations of Complex 3D Models|tech-01 · Interactive Cutaway Illustrations of Complex 3D Models (2007)]]
- [[3D结构透视研究/来源/tech-03 Compact Explosion Diagrams|tech-03 · Compact Explosion Diagrams (2010)]]
- [[3D结构透视研究/来源/tech-04 Multi-perspective Compact Explosion Diagrams|tech-04 · Multi-perspective Compact Explosion Diagrams (2011)]]
- [[3D结构透视研究/来源/tech-16 Onshape Help- Exploded Views|tech-16 · Onshape Help: Exploded Views (2026)]]
