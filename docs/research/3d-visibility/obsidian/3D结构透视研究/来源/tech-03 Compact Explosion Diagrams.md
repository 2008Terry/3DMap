---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: tech-03
year: 2010
source_type: paper
evidence: full-primary
methods:
- representative subassemblies
- compact exploded layout
- visibility optimization
domains:
- CAD
- assembly illustration
source_url: https://markustatzgern.com/papers/2010_npar_compact_explosion_diagrams.pdf
accessed: '2026-10-15'
method_families:
- '05'
- '12'
---

# Compact Explosion Diagrams

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://markustatzgern.com/papers/2010_npar_compact_explosion_diagrams.pdf)

作者/机构：Markus Tatzgern, Denis Kalkofen, Dieter Schmalstieg。年份：2010。证据层级：全文级原始资料。

## 机制

发现重复子装配，只把每组中的一个代表展开，其余维持装配状态；按照展开代表的投影面积、方向、可见性及未展开对象的可见性评分，并优化代表组合。

## 能够显露的信息

以较少屏幕空间说明重复结构的构成，同时保留整机轮廓，避免每个螺钉都飞散。

## 几何与坐标

代表部件移动，重复的非代表保持原位；不缩小全部几何来硬塞进画面。

## 代价

用户必须从代表推断其余实例，不能检查每个实例的差异；优化权重影响焦点与上下文的平衡。

## 评价证据

全文比较不同代表、权重、层次策略的CAD实例；理想权重与不同层次策略的知觉评价明确留待未来。

## 交互

可调质量权重、层次策略与视图；主要面向紧凑说明图的自动布局。

## 实现与数据要求

使用接触关系、频繁子图/同构结构检测，以及threshold-accepting式组合优化。

## 来源核对

已打开作者10页PDF，核对重复组检测、目标评分和无正式知觉验证的限制。

## 限制

为保持子装配整体可能忽略部分阻挡，论文承认爆炸过程不一定完全无碰撞；因此不应当作严格机械拆装仿真。

## 方法与关联

[[3D结构透视研究/方法/05 层级、紧凑与多透视爆炸图|层级、紧凑与多透视爆炸图]] · [[3D结构透视研究/方法/12 可见性度量与自动显露优化|可见性度量与自动显露优化]]

- [[3D结构透视研究/来源/tech-02 Automated Generation of Interactive 3D Exploded View Diagrams|tech-02 · Automated Generation of Interactive 3D Exploded View Diagrams (2008)]]
- [[3D结构透视研究/来源/tech-04 Multi-perspective Compact Explosion Diagrams|tech-04 · Multi-perspective Compact Explosion Diagrams (2011)]]
